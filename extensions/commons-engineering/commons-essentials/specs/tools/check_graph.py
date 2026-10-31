#!/usr/bin/env python3
"""check_graph.py — a CORE's graph is well formed, and its runs can be relied on (graph.md, graph-engine.md). Read-only.

Reports each finding as fail (a MUST), should (a SHOULD) or gap (missing or unverifiable, not wrong), and exits with
1 only on a fail. The check ids are those of the two specifications, part 6, and unique across them:

  graph         layout  register  untouched  nodes  stated  computed  private  answer  crossing  resolution  where-used
  graph-engine  order  package  states  checked  intact  storage

A run is checked against its own cut, never against today's graph: each source of the cut is read as git held it at
the revision the cut records (outside git, or at a revision git cannot read, from the working files only where they
still have the recorded digest, else unverified). Its classes are taken from the register, never from the run; its
edges' and proposals' classes are recomputed from every input they rest on; its lifecycle follows the transitions of
graph-engine part 5; and its released package is compared with the one first released. The reference answer is run
twice, for every class and for `public` only, and the second must show nothing of a source that is not public. A
`bill` source is resolved and read backwards over this CORE: every line of its bill is found where it is used.

Usage:  check_graph.py CORE [--spec graph|graph-engine] [--question "context and problem"]
"""
import argparse
import hashlib
import json
import os
import re
import sys

import jsonschema
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMAS = os.path.join(HERE, "..", "schemas")
sys.path.insert(0, HERE)
import answer_graph as ag  # noqa: E402
from check_core import EMAIL, PHONE, Report, computed as garden  # noqa: E402

SPECS = {"graph": ["layout", "register", "untouched", "nodes", "stated", "computed", "private", "answer", "crossing", "resolution", "where-used"],
         "graph-engine": ["order", "package", "states", "checked", "intact", "storage"]}
PACKAGE = {"run.yml", "edges.jsonl", "proposals.yml"}
NEXT = {None: {"ordered"}, "ordered": {"computed", "failed"}, "computed": {"released", "failed"},
        "released": {"superseded"}, "superseded": set(), "failed": set()}
EARLIER = {"computing": None, "paused": None, "checked": None, "rejected": "failed"}   # an earlier record, read (R6)
WITH_OUTPUTS = {"computed", "released", "superseded"}
CACHE = re.compile(r"\.(npy|npz|faiss|pkl|pickle|parquet|bin|h5|onnx|safetensors)$", re.I)
PROBE = "how does this commons share what it holds"


def schema(name):
    return json.load(open(os.path.join(SCHEMAS, name), encoding="utf-8"))


def validate(r, check, sch, doc, where):
    for e in sorted(jsonschema.Draft202012Validator(sch).iter_errors(doc), key=lambda e: list(e.path)):
        r.fail(check, f"{where}: {'/'.join(str(p) for p in e.path) or 'root'}: {e.message}")


def run_key(run):
    """the reuse key of a run (graph-engine R9): every input's digest, the engine that ran it, the method with its
    procedure, parameters, models and tools, and the policy"""
    doc = {"cut": sorted(({"source": c.get("source"), "digest": c.get("digest")} for c in run.get("cut") or []), key=lambda c: str(c["source"])),
           "engine": run.get("engine"), "method": run.get("method"), "policy": run.get("policy")}
    return "sha256:" + hashlib.sha256(json.dumps(doc, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def cut_graph(r, core, name, run, register):
    """the graph of a run's cut, each source read at its recorded revision, the files each source owned there, and
    the sources that could not be verified"""
    snaps, unverified, files = {}, set(), {}
    work = ag.Tree(core)
    for c in run.get("cut") or []:
        e = next((x for x in register if x["id"] == c.get("source")), None)
        if e is None:
            r.gap("nodes", f"run `{name}`: the source `{c.get('source')}` of its cut has left the register since")
            unverified.add(c.get("source"))
            continue
        if e.get("pin") == "lock":
            if (ag.pin_of(ag.Tree(core), ag.lock_of(core), e["ref"])[0] or {}).get("digest") != c.get("digest"):
                r.gap("nodes", f"run `{name}`: the extract `{e['id']}` is no longer the one its cut records")
                unverified.add(e["id"])
            files[e["id"]] = set(work.files(e["ref"]))
            continue
        t = ag.at(core, c.get("rev"))
        if t is not None:
            snaps[e["id"]] = t
        elif ag.digest(work, register, e) != c.get("digest"):
            r.gap("nodes", f"run `{name}`: `{e['id']}` cannot be read at `{c.get('rev') or c.get('read_at')}`, and its files have moved on; its endpoints are unverified")
            unverified.add(e["id"])
            continue
        files[e["id"]] = set(ag.owned(register, e, (t or work).files(e["ref"])))
    g = ag.read(core, snaps, only={c.get("source") for c in run.get("cut") or []})
    return g, unverified, files


def first_release(core, name):
    """the package as first released, from git: its run.yml and outputs, or None"""
    pre = (ag.git(core, "rev-parse", "--show-prefix") or b"").decode().strip()
    pkg = f"{pre}graph/runs/{name}"
    for sha in (ag.git(core, "log", "--reverse", "--format=%H", "--", f":/{pkg}") or b"").decode().split():
        doc = ag.git(core, "show", f"{sha}:{pkg}/run.yml")
        if doc and ag.state(ag.yaml_bytes(doc)) in ("released", "superseded"):
            return ag.yaml_bytes(doc), {f: ag.git(core, "show", f"{sha}:{pkg}/{f}") for f in ("edges.jsonl", "proposals.yml")}
    return None


def corrections(core, path, cid=None):
    """the claims of a file that carry a correction (learn R5), all of them or the one named"""
    p = os.path.join(core, path)
    doc = (yaml.safe_load(open(p, encoding="utf-8")) or {}) if path.endswith((".yml", ".yaml")) and os.path.isfile(p) else {}
    claims = doc.get("claims") if isinstance(doc, dict) else None
    return [c for c in claims or [] if isinstance(c, dict) and c.get("correction") and (cid is None or c.get("id") == cid)]


def check_run(r, core, name, run, edges, props, register, runs, defs):
    w, pd = f"run `{name}`", os.path.join(core, "graph", "runs", name)
    cls = {e["id"]: e["class"] for e in register}
    st = ag.state(run)
    # package (engine R4, R5, R9)
    extra = sorted(set(os.listdir(pd)) - PACKAGE)
    if extra:
        r.fail("package", f"{w}: the package holds more than its three files: {', '.join(extra)} (R4)")
    validate(r, "package", schema("graph-engine.schema.json"), run, f"{w}, `run.yml`")
    if run.get("id") != name:
        r.fail("package", f"{w}: `run.yml` gives the id `{run.get('id')}` (R4)")
    outs = run.get("outputs") or {}
    for f in ("edges.jsonl", "proposals.yml"):
        o, here = outs.get(f), os.path.isfile(os.path.join(pd, f))
        if st in WITH_OUTPUTS and not o:
            r.fail("package", f"{w}: {st}, yet `run.yml` records no `{f}` (R4, R5)")
        elif o and here and o.get("digest") != f"sha256:{ag.filehash(os.path.join(pd, f))}":
            r.fail("package", f"{w}: `{f}` differs from its digest in `run.yml` (R5)")
        elif o and not here and not o.get("location"):
            r.fail("package", f"{w}: `{f}` is neither in the package nor at a recorded location (R5)")
        elif o and not here and st in ("released", "superseded"):
            r.gap("package", f"{w}: `{f}` is only at `{o.get('location')}`; its retrieval and digest are unverified (R5, R15)")
        elif here and not o:
            r.fail("package", f"{w}: `{f}` has no digest in `run.yml` (R5)")
    if st in WITH_OUTPUTS and run.get("key") != run_key(run):
        r.fail("package", f"{w}: its reuse key is not that of its cut, method and policy (R12)")
    # order (engine R1-R3): the register's classes, never the run's
    pol = run.get("policy") or {}
    cut = {c.get("source"): c for c in run.get("cut") or [] if isinstance(c, dict)}
    for s in cut:
        if s in cls and (pol.get("classes") or {}).get(s) != cls[s]:
            r.fail("order", f"{w}: records `{(pol.get('classes') or {}).get(s)}` for `{s}`, the register holds `{cls[s]}` (R3)")
    where = pol.get("where")
    if where and where != "local":
        grant = pol.get("grant") or {}
        restricted = [s for s in cut if ag.restrictions(cls.get(s, "member"))]
        if restricted and (grant.get("recipient") != where or not set(restricted) <= set(grant.get("source") or [])):
            r.fail("order", f"{w}: {', '.join(restricted)} reach `{where}` without a grant naming that recipient and those sources (R3)")
        elif restricted:
            gs = ag.grant_state(core, grant.get("where"), run, cls)
            if gs == "none":
                r.fail("order", f"{w}: its grant is recorded as no decision event of the CORE (R3)")
            elif gs == "outside":
                r.fail("order", f"{w}: the decision `{grant.get('where')}` grants no scope that covers its restricted sources, purpose and recipient (R3)")
            elif gs == "unscoped":
                r.gap("order", f"{w}: the decision `{grant.get('where')}` states no structured `grant`; its scope is unverified and its edges are not served (R3)")
            elif gs == "withdrawn":
                r.should("order", f"{w}: a correction has withdrawn its grant; its edges are no longer served (R3, R9)")
    # states (engine R6, R7): a record of an earlier form is read, never rewritten
    prev = None
    for s in run.get("states") or []:
        cur = s.get("state") if isinstance(s, dict) else None
        if cur in EARLIER:
            if EARLIER[cur] is None:
                continue
            cur = EARLIER[cur]
        if cur not in NEXT.get(prev, set()):
            r.fail("states", f"{w}: `{prev or 'nothing'}` cannot become `{cur}` (R6)")
        if cur == "released" and not (s.get("by") and s.get("where")):
            r.fail("states", f"{w}: released without who gave the word and where it is recorded (R7)")
        if cur == "superseded":
            later = runs.get(str(s.get("by")))
            if not later or later[0].get("parent") != name:
                r.fail("states", f"{w}: superseded by `{s.get('by')}`, which is no run whose parent it is (R7)")
        prev = cur
    if st in ("released", "superseded"):
        first = first_release(core, name)
        if first is None:
            r.gap("states", f"{w}: the package as first released cannot be read from git; that it never changed is unverified (R7)")
        else:
            was, outs = first
            changed = sorted(k for k in set(was) | set(run) if k != "states" and was.get(k) != run.get(k))
            if changed:
                r.fail("states", f"{w}: its record changed after it was first released: {', '.join(changed)} (R7)")
            before, now = was.get("states") or [], run.get("states") or []
            if now[:len(before)] != before or any(not isinstance(s, dict) or s.get("state") != "superseded" for s in now[len(before):]):
                r.fail("states", f"{w}: its states after release were rewritten; only `superseded` may be appended (R7)")
            for f, b in outs.items():
                p = os.path.join(pd, f)
                if b is not None and os.path.isfile(p) and ag.sha(b) != ag.filehash(p):
                    r.fail("states", f"{w}: `{f}` changed after the run was released (R7)")
    # nodes, checked (graph R5, R10; engine R7, R9): against the run's own cut
    cg, unverified, files = cut_graph(r, core, name, run, register)
    verified = not unverified
    for n, x in enumerate(edges, 1):
        at = f"{w}, `edges.jsonl` line {n}"
        for e in jsonschema.Draft202012Validator({**defs["edge"], "$defs": defs}).iter_errors(x):
            r.fail("computed", f"{at}: {'/'.join(str(p) for p in e.path) or 'root'}: {e.message} (R8)")
        if x.get("run") != name:
            r.fail("computed", f"{at}: names the run `{x.get('run')}`, not its own (R8, R9)")
        if x.get("method") != (run.get("method") or {}).get("kind"):
            r.fail("computed", f"{at}: the method `{x.get('method')}` is not the run's (R8)")
        if x.get("by") == "stated":
            r.fail("stated", f"{at}: a stated edge is stored in `graph/` (R6)")
        for end in (x.get("from"), x.get("to")):
            if verified and end not in cg.nodes:
                r.fail("nodes", f"{at}: `{end}` is no node of a source in its cut, such as a grouping of the run (R5)")
        srcs = ag.sources_of(x.get("rests_on"))
        for s in srcs - set(cut):
            r.fail("checked", f"{at}: rests on `{s}`, which is not in its cut (R7)")
        for ref in x.get("rests_on") or []:
            s, _, what = str(ref).partition(":")
            if s not in cut or s in unverified:
                if s in unverified:
                    r.gap("checked", f"{at}: `{ref}` cannot be resolved; the source's snapshot is unverified (R7)")
                continue
            if what not in files.get(s, set()) and (cg.nodes.get(what) or {}).get("source") != s:
                r.fail("checked", f"{at}: `{ref}` is neither a file nor a node of `{s}` in its cut (R7)")
        ends = {cg.nodes[e]["source"] for e in (x.get("from"), x.get("to")) if e in cg.nodes}
        want = ag.restrictions(*[cls.get(s, "member") for s in srcs | ends])
        if st in ("checked", "released", "superseded") and ag.restrictions(x.get("class")) != want:   # checked: an earlier record
            r.fail("checked", f"{at}: the class `{x.get('class')}` is not `{ag.as_class(want)}`, the restrictions of every input it rests on (R7, R9)")
    # checked (engine R13): a run whose output leaves its commons reads no correction its giver did not release for it
    if run.get("aggregates"):
        for n, x in enumerate(edges, 1):
            for ref in x.get("rests_on") or []:
                s, _, what = str(ref).partition(":")
                if what.startswith("claim:"):
                    path, cid = None, what[len("claim:"):]
                else:
                    path, _, cid = what.partition("#")
                found = corrections(core, path or "knowledge/claims.yml", cid or None)
                for c in found:
                    uses = [str(v.get("use")) if isinstance(v, dict) else str(v) for v in (c.get("correction") or {}).get("release") or []]
                    if name not in uses:                     # release: [{use, word}] (core-knowledge)
                        r.fail("checked", f"{w}, `edges.jsonl` line {n}: rests on the correction `{c.get('id')}`, which its giver "
                                          f"did not release for this run's output (R20)")
    for n, p in enumerate(props, 1):
        at = f"{w}, proposal {n}"
        for e in jsonschema.Draft202012Validator({**defs["proposal"], "$defs": defs}).iter_errors(p):
            r.fail("package", f"{at}: {e.message} (R4)")
        m = re.match(r"^edges\.jsonl:(\d+)$", str(p.get("edge")))
        base = edges[int(m[1]) - 1] if m and 0 < int(m[1]) <= len(edges) else None
        if base is None:
            r.fail("checked", f"{at}: rests on `{p.get('edge')}`, no edge of this package (graph R4)")
        elif "class" in p and ag.restrictions(p["class"]) != ag.restrictions(base.get("class"), cls.get(p.get("source"), "member")):
            r.fail("checked", f"{at}: the class `{p['class']}` is not that of its edge and its source (R9)")
    # intact (engine R7; graph R4)
    pre = (ag.git(core, "rev-parse", "--show-prefix") or b"").decode().strip() if ag.git(core, "rev-parse") is not None else None
    if pre is None:
        r.gap("intact", f"{w}: the CORE is not in git; that the run left its sources as they were is unverified")
        return
    whole = True
    for s, c in cut.items():
        e = next((x for x in register if x["id"] == s), None)
        if not e or e.get("pin") == "lock":
            continue
        t = ag.at(core, c.get("rev"))
        if t is None:
            whole = False
            r.gap("intact", f"{w}: `{s}` cannot be read at `{c.get('rev') or c.get('read_at')}`; unverified")
        elif ag.digest(t, register, e) != c.get("digest"):
            r.fail("intact", f"{w}: `{s}` at `{c.get('rev')}` does not have the digest the run recorded (R7)")
    pkg = f"{pre}graph/runs/{name}/"
    for sha in (ag.git(core, "log", "--format=%H", "--", f":/{pkg}") or b"").decode().split() if whole else []:
        touched = (ag.git(core, "show", "--name-only", "--format=", sha) or b"").decode().split()
        others = [t for t in touched if t.startswith(pre) and not t.startswith(pkg)]
        if others:
            r.fail("intact", f"{w}: the commit {sha[:10]} that brought it also changes `{others[0][len(pre):]}` (graph R4)")


def check(core, question=None):
    r = Report()
    gd = os.path.join(core, "graph")
    reg_path = os.path.join(gd, "sources.yml")
    # layout (graph R1, R17)
    if not os.path.isdir(gd):
        r.gap("layout", "the CORE has no graph yet: no `graph/sources.yml` (R1)")
        return r
    if not os.path.isfile(reg_path):
        r.fail("layout", "`graph/` has no register `sources.yml` (R1)")
        return r
    for x in sorted(os.listdir(gd)):
        if x not in ("sources.yml", "runs"):
            r.fail("layout", f"`graph/{x}` is neither the register nor `runs/` (R1)")
    validate(r, "layout", schema("graph.schema.json"), ag.yml(reg_path), "`graph/sources.yml`")
    register, lock = ag.register_of(core), ag.lock_of(core)
    # register (R2, R3, R17)
    seen = set()
    for e in register:
        at = f"source `{e['id']}`"
        if e["id"] in seen:
            r.fail("register", f"{at} is registered twice (R2)")
        seen.add(e["id"])
        if e["kind"] not in ag.READERS:
            r.gap("register", f"{at}: no reader for the kind `{e['kind']}` yet; it is reported as not read, never as read (R3)")
        if e["kind"] == "core" and not e.get("grant"):
            r.fail("register", f"{at}: a source of another commons names no grant (R17)")
        if e.get("pin") == "lock":
            entry = ag.lock_entry(lock, e["ref"])
            pin, why = ag.pin_of(ag.Tree(core), lock, e["ref"])
            ix = os.path.join(core, ag.key_of(e["ref"]), "index.jsonl")
            if entry is None:
                r.fail("register", f"{at}: `pin: lock`, but the lock records no extract at `{e['ref']}` (R2)")
            elif pin is None:
                r.fail("register", f"{at}: {why}; it is not read (R2, R12; core R29)")
            elif not os.path.isfile(ix) or f"sha256:{ag.filehash(ix)}" != pin.get("digest"):
                r.fail("register", f"{at}: its index is not the one its pinned record names; it is not read (R2, R12)")
        elif e["kind"] in ag.READERS and not os.path.exists(os.path.join(core, e["ref"])):
            r.fail("register", f"{at}: `{e['ref']}` does not exist in the CORE (R2)")
    for a, b in ag.overlaps(register):
        r.fail("register", f"sources `{a}` and `{b}` claim the same files; a source owns its own folder (R2)")
    g = ag.read(core)
    runs = ag.runs_of(core)
    # untouched (R4): no source holds a run id of this graph or a garden block
    work = ag.Tree(core)
    for e in register:
        if e["kind"] not in ag.READERS or e.get("pin") == "lock" or not work.exists(e["ref"]):
            continue
        for rel in ag.owned(register, e, work.files(e["ref"])):
            if not rel.endswith((".md", ".yml", ".yaml", ".jsonl")):
                continue
            t = work.read(rel).decode("utf-8", "replace")
            for rid in runs:
                if re.search(rf"(?<![\w.-]){re.escape(rid)}(?![\w.-])", t):
                    r.fail("untouched", f"`{rel}` holds the id of the run `{rid}` (R4)")
            fm = ag.front(work.read(rel)) if rel.endswith(".md") else None
            if fm and garden(fm):
                r.fail("untouched", f"`{rel}` holds a garden block, a computed relation (R4)")
    defs = schema("graph-engine.schema.json")["$defs"]
    for name, (run, edges, props) in runs.items():
        check_run(r, core, name, run, edges, props, register, runs, defs)
    for dirpath, _, fs in os.walk(gd):
        for f in fs:
            if CACHE.search(f):
                r.fail("storage", f"`{os.path.relpath(os.path.join(dirpath, f), core).replace(os.sep, '/')}`: an embedding or cache is committed (R15)")
    for name, (run, edges, _) in runs.items():
        if ag.state(run) not in ("released", "superseded") and edges:
            r.should("storage", f"run `{name}`: not released, yet its edges are committed; an attempt keeps its `run.yml` (R15)")
    # computed: the foreign run an installed extract carries (R8)
    for e in register:
        if e.get("pin") == "lock" and any(x["source"] == e["id"] and x["by"] == "computed" for x in g.edges) \
                and not (ag.pin_of(ag.Tree(core), lock, e["ref"])[0] or {}).get("graph_run"):
            r.fail("computed", f"source `{e['id']}`: its computed links name no run; its pinned record names no `graph_run` (R8)")
    # stated (R6): every stated edge resolves, or its target is not held yet
    unresolved = sorted({x["to"] for x in g.edges if x["by"] == "stated" and x["to"] not in g.nodes and not x["to"].startswith(ag.OUTSIDE)})
    for t in unresolved[:10]:
        r.gap("stated", f"a stated edge points to `{t}`, which no source holds yet (R6)")
    # resolution (R26) and where-used (R27): over the CORE's own bill, read as a source
    for e in [e for e in register if e["kind"] == "bill"]:
        if e["id"] not in g.bills:
            r.gap("resolution", f"source `{e['id']}`: {next(u['reason'] for u in g.unread if u['source'] == e['id'])}; it is not read (R26)")
            continue
        res = ag.resolve(core)
        if not (res.get("rev") or res.get("read_at")) or not res.get("generator"):
            r.fail("resolution", f"source `{e['id']}`: its bill names no generator or revision; a level says what it was read from (R26; core R37)")
        for x in res.get("lines") or []:
            rel = x.get("release") or {}
            if rel.get("why") and rel.get("part"):
                r.fail("resolution", f"`{x['part']}`: {rel['why']}; it does not resolve (R26)")
            for why in {rel.get("why") if not rel.get("part") else None, (rel.get("below") or {}).get("why"), (x.get("below") or {}).get("why")} - {None}:
                r.gap("resolution", f"`{x['part']}`: {why}; the resolution ends there (R26)")
            if not any(u["core"] == g.core_id and u["part"] == x["part"] for u in ag.where_used(x["part"], [core])["used_in"]):
                r.fail("where-used", f"`{x['part']}` is a line of the bill, and where-used does not find this CORE for it (R27)")
        if e["class"] != "public" and res.get("lines"):
            pub = ag.where_used(res["lines"][0]["part"], [core], classes=["public"])
            if pub["used_in"] or not pub["unsighted"]:
                r.fail("where-used", f"a caller of `public` only is shown the bill of class `{e['class']}`, or not told it was withheld (R27)")
    # private (R11)
    pp = os.path.join(core, "people.yml")
    names = {p.get("name") for p in (ag.yml(pp).get("people") or [] if os.path.isfile(pp) else []) if isinstance(p, dict) and p.get("name")}
    for dirpath, _, fs in os.walk(gd):
        for f in fs:
            p = os.path.join(dirpath, f)
            t = open(p, encoding="utf-8", errors="replace").read()
            rel = os.path.relpath(p, core).replace(os.sep, "/")
            if EMAIL.search(t) or PHONE.search(t):
                r.fail("private", f"`{rel}` holds a contact datum (R11)")
            for nm in names:
                if re.search(rf"\b{re.escape(nm)}\b", t):
                    r.fail("private", f"`{rel}` names a person of the party register (R11)")
    # answer (R12-R14, R24): the reference answer validates; for `public` only it shows nothing of another class
    sch = schema("graph.schema.json")
    q = question or PROBE
    full = ag.answer(core, q)
    validate(r, "answer", {**sch["$defs"]["answer"], "$defs": sch["$defs"]}, full, "the reference answer")
    read_ids = {c["source"] for c in full["cut"]} | set(ag.partial(full["silences"], "unread"))
    for e in register:
        if e["id"] not in read_ids:
            r.fail("answer", f"the reference answer neither reads the source `{e['id']}` nor reports it as not read (R12, R13)")
    if not any(ag.state(run) == "released" for run, _, _ in runs.values()) and full["method"] not in ("stated-only", "lexical"):
        r.fail("answer", f"no released run of the commons' own, yet the answer's method is `{full['method']}` (R14)")
    hidden = {e["id"] for e in register if e["class"] != "public"}
    if hidden:
        pub = ag.answer(core, q, classes=["public"])
        secret = {n for n, v in g.nodes.items() if v["source"] in hidden}
        shown = {c["id"] for c in pub["candidates"]} | set(pub["silences"]["not_held"]) | \
                {t for c in pub["candidates"] for v in c["via"] for t in re.findall(r"[\w./:#-]+", v)}
        leaks = sorted((shown & secret) | ({c["source"] for c in pub["cut"]} & hidden) | (set(ag.partial(pub["silences"], "unread")) & hidden))
        if leaks:
            r.fail("answer", f"a caller of `public` only is shown what is not public: {', '.join(leaks[:3])} (R13, R24)")
        if not pub["silences"]["unsighted"]:
            r.fail("answer", "a caller of `public` only is not told that something was withheld (R13)")
    # crossing (R18)
    agg = sch["$defs"]["aggregate"]
    for name, (run, _, _) in runs.items():
        for n, a in enumerate(run.get("aggregates") or [], 1):
            at = f"run `{name}`, aggregate {n}"
            for e in jsonschema.Draft202012Validator({**agg, "$defs": sch["$defs"]}).iter_errors(a):
                r.fail("crossing", f"{at}: {e.message} (R18)")
            if isinstance(a, dict) and a.get("count", 0) < max(5, a.get("threshold", 5)):
                r.fail("crossing", f"{at}: {a.get('count')} commons, below its threshold of at least five (R18)")
    return r


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("core")
    ap.add_argument("--spec", choices=sorted(SPECS), help="report the findings of one specification only")
    ap.add_argument("--question", help="the context and problem the reference answer is asked")
    a = ap.parse_args()
    items = [i for i in check(a.core, a.question).items if not a.spec or i[1] in SPECS[a.spec]]
    n = {o: sum(1 for i in items if i[0] == o) for o in ("fail", "should", "gap")}
    print(f"# {a.core}{' · ' + a.spec if a.spec else ''}: {n['fail']} fail · {n['should']} should · {n['gap']} gap")
    for o, c, t in items:
        print(f"{o}: {c}: {t}")
    return 1 if n["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
