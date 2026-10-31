#!/usr/bin/env python3
"""check_workshop.py — check a GitHub project (Projects v2) against a workshop definition; read-only.

Sketch of Body D4 of Commons Engineering, 21 October 2026, for definition 0.8.0 (draft). Reports every difference as a
delta, in the words of the loop contract: missing (the definition asks for it, the project lacks it), extra (the
project has it, the definition does not ask), differs (both have it, unlike), and use (how items are filled).

--kind names what the project is (model-workshop by default, or commons-workshop). For a Commons Workshop,
every item of a type the kind never holds — a Story of the model (W1) — is reported as a use delta.

--plan prints the changes a setup would make: only additions, never a removal, so a second run plans nothing
(idempotent). The sketch performs none of them; applying is a separate step on the Steward's word.

Usage:
    python check_workshop.py <definition.yml> <owner> <project-number> [--kind KIND] [--plan]
Needs: gh, authenticated with read access to the organisation, its project and repositories.
"""
import json
import subprocess
import sys

import yaml

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

Q = """query($o:String!,$n:Int!,$c:String){organization(login:$o){
 issueTypes(first:50){nodes{name isEnabled}}
 projectV2(number:$n){title url
  repositories(first:50){nodes{nameWithOwner}}
  fields(first:50){nodes{... on ProjectV2FieldCommon{name dataType} ... on ProjectV2SingleSelectField{options{name}}}}
  views(first:50){nodes{name layout filter verticalGroupByFields(first:3){nodes{... on ProjectV2FieldCommon{name}}}
   groupByFields(first:3){nodes{... on ProjectV2FieldCommon{name}}}
   sortByFields(first:3){nodes{field{... on ProjectV2FieldCommon{name}}}}
   fields(first:50){nodes{... on ProjectV2FieldCommon{name}}}}}
  workflows(first:30){nodes{name enabled}}
  items(first:100,after:$c){pageInfo{hasNextPage endCursor} nodes{
   stage:fieldValueByName(name:"Stage"){... on ProjectV2ItemFieldSingleSelectValue{name}}
   status:fieldValueByName(name:"Status"){... on ProjectV2ItemFieldSingleSelectValue{name}}
   content{... on Issue{state number updatedAt body repository{nameWithOwner} issueType{name} labels(first:30){nodes{name}}
    assignees(first:10){nodes{login}} parent{number}}}}}}}}"""
LAYOUT = {"board": "BOARD_LAYOUT", "table": "TABLE_LAYOUT", "roadmap": "ROADMAP_LAYOUT"}
TYPE = {"single_select": "SINGLE_SELECT", "date": "DATE", "text": "TEXT", "number": "NUMBER"}


def gh(args):
    out = subprocess.run(["gh"] + args, capture_output=True, text=True, encoding="utf-8")
    if out.returncode:
        sys.exit(f"gh {' '.join(args[:2])} failed: {out.stderr.strip()}")
    return json.loads(out.stdout)


def read(owner, number):
    org, items, cursor = None, [], None
    while True:
        args = ["api", "graphql", "-f", f"query={Q}", "-f", f"o={owner}", "-F", f"n={number}"]
        if cursor:
            args += ["-f", f"c={cursor}"]
        org = gh(args)["data"]["organization"]
        page = org["projectV2"]["items"]
        items += [n for n in page["nodes"] if n.get("content")]
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return org, items


def from_core(core):
    """G1 (#84): what the CORE supplies — its Bodies, its repository, its lifecycle stage. Read-only.

    `core` is owner/repo[@ref] on the platform. Bodies are the records of kind `body` in element 9's folder
    (`registry/bodies/`, or the structure definition's folder for element 9 when the CORE carries one).
    """
    repo, _, ref = core.partition("@")
    q = f"?ref={ref}" if ref else ""
    def get(path):
        out = subprocess.run(["gh", "api", f"repos/{repo}/contents/{path}{q}"], capture_output=True, text=True, encoding="utf-8")
        return json.loads(out.stdout) if out.returncode == 0 else None
    import base64
    def read(path):
        f = get(path)
        return yaml.safe_load(base64.b64decode(f["content"]).decode("utf-8")) if isinstance(f, dict) and "content" in f else None
    folder = "registry/bodies"
    st = read(".commons/structure.yml") or {}
    for e in st.get("elements", []) or []:
        if e.get("position") == 9 and e.get("folder"):
            folder = e["folder"] if "/" in e["folder"] else f"registry/{e['folder']}"
    bodies = []
    for f in get(folder) or []:
        if f.get("name", "").endswith(".yml"):
            doc = read(f"{folder}/{f['name']}") or {}
            if doc.get("kind") == "body" and doc.get("slug"):
                bodies.append((doc["slug"].upper(), doc.get("title", "")))
    stage = read("lifecycle/stage.yml") or {}
    real = get("")
    return {"repo": repo, "bodies": sorted(bodies), "folder": folder, "stage": stage.get("stage"), "since": stage.get("since"),
            "found": real is not None}


def main(def_path, owner, number, plan, kind="model-workshop", core=None):
    d = yaml.safe_load(open(def_path, encoding="utf-8"))
    if kind not in d["kinds"]:
        sys.exit(f"unknown kind '{kind}': the definition knows {', '.join(d['kinds'])}")
    org, items = read(owner, int(number))
    p = org["projectV2"]
    deltas, todo, notes = [], [], []

    def delta(kind, what):
        deltas.append((kind, what))

    # issue types — organisation level
    have = {t["name"]: t["isEnabled"] for t in org["issueTypes"]["nodes"]}
    want = [t["name"] for t in d["issue_types"]["required"]]
    for t in want:
        if t not in have:
            delta("missing", f"issue type '{t}' (organisation {owner})"); todo.append(f"create issue type '{t}'")
        elif not have[t]:
            delta("differs", f"issue type '{t}' is disabled"); todo.append(f"enable issue type '{t}'")
    for t in sorted(set(have) - set(want)):
        if have[t]:                                             # a disabled type offers nothing to choose
            delta("extra", f"issue type '{t}'")

    # repositories — linked, and holding items
    linked = {r["nameWithOwner"] for r in p["repositories"]["nodes"]}
    used = {i["content"]["repository"]["nameWithOwner"] for i in items}
    c = from_core(core) if core else None
    if c is not None:
        if not c["found"]:
            sys.exit(f"CORE {core} cannot be read")
        notes.append(f"CORE {c['repo']}: {len(c['bodies'])} Bodies in {c['folder']}; lifecycle stage {c['stage'] or 'not recorded'}"
                     + (f" since {c['since']}" if c.get("since") else "") + " — shown in the project's description, not as Stage options")
        used = used | {c["repo"]}                              # the CORE's own repository is always linked
    for r in sorted(used - linked):
        delta("missing", f"repository {r} holds items but is not linked"); todo.append(f"link repository {r}")

    # labels — repository level, in every repository that holds items
    want_l = {l["name"]: l["description"] for l in d["labels"]["required"]}
    if c is not None and c["bodies"]:
        want_l = {slug: f"Body {slug} — {title}. Work address; grants no authority." for slug, title in c["bodies"]}
    elif c is not None:
        notes.append(f"CORE {c['repo']}: no Bodies found in {c['folder']}; the definition's labels D0–D4 are used")
    for r in sorted(used | linked):
        got = {l["name"]: l.get("description", "") for l in gh(["label", "list", "--repo", r, "--limit", "200", "--json", "name,description"])}
        for name, desc in want_l.items():
            if name not in got:
                delta("missing", f"label '{name}' in {r}"); todo.append(f"create label '{name}' in {r}")
            elif got[name] != desc:
                delta("differs", f"label '{name}' in {r}: description '{got[name]}'")
        rest = set(got) - set(want_l)
        retired = sorted(x for x in rest if (got[x] or "").lower().startswith("retired"))
        extra = sorted(rest - set(retired))
        if extra:
            delta("extra", f"labels in {r}: {', '.join(extra)}")
        if retired:
            notes.append(f"{r}: {len(retired)} retired labels kept for history")

    # fields — project level
    fields = {f["name"]: f for f in p["fields"]["nodes"] if f}
    for f in d["fields"]:
        g = fields.get(f["name"])
        if not g:
            if f["required"]:
                delta("missing", f"field '{f['name']}'"); todo.append(f"create field '{f['name']}' {f.get('options', '')}")
            continue
        if g["dataType"] != TYPE[f["type"]]:
            delta("differs", f"field '{f['name']}' is {g['dataType']}, not {f['type']}")
        if "options" in f:
            opts = [o["name"] for o in g.get("options", [])]
            for o in f["options"]:
                if o not in opts:
                    delta("missing", f"option '{o}' of field '{f['name']}'"); todo.append(f"add option '{o}' to '{f['name']}'")
            common = [o for o in opts if o in f["options"]]
            if common != [o for o in f["options"] if o in opts]:
                delta("differs", f"option order of '{f['name']}': {' · '.join(opts)}")
            for o in opts:
                if o not in f["options"]:
                    delta("extra", f"option '{o}' of field '{f['name']}'")

    # views — checked only; the API cannot create views
    views = {v["name"]: v for v in p["views"]["nodes"]}
    want_v = d["views"] + d["kinds"][kind].get("views", [])
    for v in want_v:
        g = views.get(v["name"])
        if not g:
            delta("missing", f"view '{v['name']}' (to be created by hand)"); continue
        if g["layout"] != LAYOUT[v["layout"]]:
            delta("differs", f"view '{v['name']}' layout {g['layout']}")
        if (g["filter"] or "") != v.get("filter", ""):
            delta("differs", f"view '{v['name']}' filter '{g['filter']}'")
        cols = [n["name"] for n in g["verticalGroupByFields"]["nodes"]]
        if v.get("columns") and cols != [v["columns"]]:
            delta("differs", f"view '{v['name']}' columns {cols}")
        grp = [n["name"] for n in g["groupByFields"]["nodes"] if n]
        if v.get("group") and grp != [v["group"]]:
            delta("differs", f"view '{v['name']}' grouped by {grp or 'nothing'}, not {v['group']}")
        srt = [n["field"]["name"] for n in g["sortByFields"]["nodes"] if n and n.get("field")]
        if v.get("sort") and (not srt or srt[0] != v["sort"]):
            delta("differs", f"view '{v['name']}' sorted by {srt or 'nothing'}, not {v['sort']}")
        shown = {n["name"] for n in g["fields"]["nodes"] if n}
        lacking = [f for f in v.get("fields", []) if f != "Type" and f not in shown]
        if lacking:
            delta("differs", f"view '{v['name']}' does not show {', '.join(lacking)}")
    for name in sorted(set(views) - {v["name"] for v in want_v}):
        delta("extra", f"view '{name}'")
    for name, g in sorted(views.items()):
        bad = {n["name"] for n in g["groupByFields"]["nodes"] if n} & set(d.get("views_never_group_by", []))
        if bad:
            delta("differs", f"view '{name}' is grouped by {', '.join(sorted(bad))}, which makes the project fail to load; use Slice by instead (by hand)")

    # workflows
    wf = {w["name"]: w["enabled"] for w in p["workflows"]["nodes"]}
    for w in d["workflows"]["enabled"]:
        if not wf.get(w):
            delta("differs", f"workflow '{w}' is off"); todo.append(f"switch on workflow '{w}' (by hand)")

    # use — how open items are filled
    open_items = [i for i in items if i["content"]["state"] == "OPEN"]
    no_type = [i for i in open_items if not i["content"]["issueType"]]
    no_body = [i for i in open_items if not {l["name"] for l in i["content"]["labels"]["nodes"]} & {"D0", "D1", "D2", "D3", "D4"}]
    epics_no_stage = [i for i in open_items if (i["content"]["issueType"] or {}).get("name") == "Epic" and not i.get("stage")]
    ref = lambda xs: ", ".join(f"{i['content']['repository']['nameWithOwner'].split('/')[1]}#{i['content']['number']}" for i in xs[:12]) + (" …" if len(xs) > 12 else "")
    if no_type:
        delta("use", f"{len(no_type)} of {len(open_items)} open items without issue type: {ref(no_type)}")
    if no_body:
        delta("use", f"{len(no_body)} of {len(open_items)} open items without a Body label: {ref(no_body)}")
    if epics_no_stage:
        delta("use", f"{len(epics_no_stage)} open Epics without Stage: {ref(epics_no_stage)}")
    # flow — rules 1–3 (Holger, 23 Oct)
    fl = d.get("flow") or {}
    if fl:
        import datetime, re
        now = datetime.datetime.now(datetime.timezone.utc)
        status = lambda i: (i.get("status") or {}).get("name")
        assigned = lambda i: [a["login"] for a in i["content"]["assignees"]["nodes"]]
        closed = [i for i in items if i["content"]["state"] == "CLOSED"]
        still = [i for i in closed if assigned(i)]
        if still:
            delta("use", f"rule 1: {len(still)} closed items still assigned: {ref(still)}")
        days = fl["assignee"].get("validate_unassigned_days", 3)
        def age(i):
            return (now - datetime.datetime.fromisoformat(i["content"]["updatedAt"].replace("Z", "+00:00"))).days
        waiting = [i for i in open_items if status(i) == "Validate" and not assigned(i) and age(i) > days]
        if waiting:
            delta("use", f"rule 1: {len(waiting)} open items in Validate without an assignee for more than {days} days: {ref(waiting)}")
        no_status = [i for i in open_items if not status(i)]
        if no_status:
            delta("use", f"rule 2: {len(no_status)} open items without Status: {ref(no_status)}")
        open_done = [i for i in open_items if status(i) == "Done"]
        if open_done:
            delta("use", f"rule 2: {len(open_done)} open items in Done: {ref(open_done)}")
        closed_not_done = [i for i in closed if status(i) and status(i) != "Done"]
        if closed_not_done:
            delta("use", f"rule 2: {len(closed_not_done)} closed items not in Done: {ref(closed_not_done)}")
        types = set(fl["parent"].get("applies_to", []))
        orphan = [i for i in open_items if (i["content"]["issueType"] or {}).get("name") in types and not i["content"]["parent"]]
        if orphan:
            delta("use", f"rule 3: {len(orphan)} open Stories without a parent issue: {ref(orphan)}")
        named = re.compile(r"(?im)^\W*parent\W*[:=]?\s*\S*#\d+")
        text_only = [i for i in open_items if not i["content"]["parent"] and named.search(i["content"]["body"] or "")]
        if text_only:
            delta("use", f"rule 3: {len(text_only)} open items name a parent in their text but have none linked: {ref(text_only)}")

    for t in d["kinds"][kind].get("never_holds", []):
        held = [i for i in items if (i["content"]["issueType"] or {}).get("name") == t]
        if held:
            delta("use", f"{len(held)} items of type '{t}', which a {kind} never holds: {ref(held)}")

    print(f"# Workshop check — {p['title']} ({p['url']}) as {kind}, against {d['definition']} {d['version']}")
    print(f"items: {len(items)} ({len(open_items)} open) · repositories holding items: {len(used)} · linked: {len(linked)}\n")
    for n in notes:
        print(f"note: {n}")
    if notes:
        print()
    for kind in ("missing", "differs", "extra", "use"):
        sel = [w for k, w in deltas if k == kind]
        print(f"## {kind} — {len(sel)}")
        for w in sel:
            print(f"- {w}")
        print()
    if plan:
        print(f"## plan — {len(todo)} additions, no removals (not performed)")
        for t in todo:
            print(f"- {t}")
    sys.exit(1 if any(k in ("missing", "differs") for k, _ in deltas) else 0)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="check a workshop project against its definition; read-only")
    ap.add_argument("definition"); ap.add_argument("owner"); ap.add_argument("number")
    ap.add_argument("--kind", default="model-workshop")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--core", help="owner/repo[@ref] of the CORE the workshop is generated from (#84): its Bodies give the labels")
    a = ap.parse_args()
    main(a.definition, a.owner, a.number, a.plan, a.kind, a.core)
