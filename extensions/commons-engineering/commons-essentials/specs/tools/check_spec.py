#!/usr/bin/env python3
"""check_spec.py — a specification follows the Commons SPECIFICATION. Read-only.

Body D4 of Commons Engineering, for commons.o#87 (deliverable D3). It implements the contract of
`specification.md` part 6: the check ids named in its part 4, each finding reported as

    fail    a MUST is not met                       → exit 1
    should  a SHOULD is not met                     → reported, exit 0
    gap     something is absent and no MUST needs it (R12) → reported, exit 0

The rule itself decides; this file only reads it. The schema of the front matter and of a requirement row is
`schemas/specification.schema.json`, next to this tool's folder.

A text in another repository is named `owner/repo@rev:path` (in `supersedes` and in links). It is resolved in a
checkout of that repository found beside this one, else through the platform's API: found is fine, not there at
that revision is a fail, unreachable is a gap, and a malformed reference is a fail. `--offline` skips the API.

Usage:
    check_spec.py SPEC.md [SPEC.md ...] [--since REVISION] [--glossary DIR] [--offline]
--glossary defaults to the `glossary/terms` folder of the commons the specification lives in.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

import yaml

try:
    import jsonschema
except ImportError:                                            # a check that cannot run must say so
    jsonschema = None

HERE = os.path.dirname(os.path.abspath(__file__))
RULE_SCHEMA = os.path.normpath(os.path.join(HERE, "..", "schemas", "specification.schema.json"))
COLUMNS = ["ID", "Level", "Requirement", "Why", "Check"]
KINDS = {"commissioned", "reviewed", "adopted", "revised"}       # part 8 of specification.md (R15)
SIZE = 400
H2 = re.compile(r"^##\s+(\d+)\s*[·.:\-–]?\s*(.*)$")
FENCE = re.compile(r"^```(\w*)\s*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# The sentence rule of part 6, fixed: a sentence ends at . ! or ? when a space and a capital letter follow, or
# where the cell ends. Text in code spans does not count. Nothing else is an exception.
SENT_END = re.compile(r"[.!?](?=\s+[A-Z])")


class Report:
    def __init__(self):
        self.items = []

    def add(self, outcome, check, text):
        if (outcome, check, text) not in self.items:
            self.items.append((outcome, check, text))

    def fail(self, c, t): self.add("fail", c, t)
    def should(self, c, t): self.add("should", c, t)
    def gap(self, c, t): self.add("gap", c, t)


def split(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return (yaml.safe_load(text[3:end]) or {}), text[end + 4:].splitlines()
    return None, text.splitlines()


def parts_of(lines):
    """{number: (title, [lines])}, in file order, plus the numbers as they appear"""
    parts, order, cur = {}, [], None
    for line in lines:
        m = H2.match(line)
        if m:
            cur = int(m.group(1))
            order.append(cur)
            parts[cur] = (m.group(2).strip(), [])
        elif line.startswith("## "):
            order.append(None)
            cur = None
        elif cur is not None:
            parts[cur][1].append(line)
    return parts, order


def table(lines):
    """the first markdown table in lines: header cells and rows of cells"""
    rows, started = [], False
    for l in lines:                                            # the first contiguous block only
        if l.strip().startswith("|"):
            rows.append(l)
            started = True
        elif started:
            break
    if len(rows) < 2:
        return None, []
    cells = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
    head = cells(rows[0])
    body = [cells(r) for r in rows[2:] if not re.match(r"^\|\s*-", r.strip())]
    return head, body


def sentences(text):
    """the number of sentences in a cell, by the sentence rule of part 6"""
    plain = re.sub(r"`[^`]*`", "x", text).strip()
    if not plain:
        return 0
    return len(SENT_END.findall(plain)) + 1                    # the last sentence ends where the cell ends


def declared_checks(lines):
    """the check ids a specification declares: the backticked first column of the first table in part 6"""
    _, rows = table(lines)
    return {m.group(1) for c in rows if c for m in [re.match(r"^`([^`]+)`$", c[0])] if m}


def blocks(lines, langs):
    out, cur, lang = [], None, None
    for line in lines:
        m = FENCE.match(line)
        if m and cur is None:
            cur, lang = [], m.group(1).lower()
        elif m and cur is not None:
            if lang in langs:
                out.append((lang, "\n".join(cur)))
            cur = None
        elif cur is not None:
            cur.append(line)
    return out


def repo_root(start):
    d = start
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, ".git")):
            return d
        d = os.path.dirname(d)
    return start


def find_up(start, rel):
    d = start
    while d != os.path.dirname(d):
        p = os.path.join(d, rel)
        if os.path.isdir(p):
            return p
        d = os.path.dirname(d)
    return None


REMOTE = re.compile(r"^(?P<owner>[A-Za-z0-9][A-Za-z0-9-]*)/(?P<repo>[A-Za-z0-9._-]+)@(?P<rev>[^\s:@]+):(?P<path>[^\s:@]+)$")


def remote_like(ref):
    """a reference meant for another repository: it carries @ or : and is not a URL"""
    return ("@" in ref or ":" in ref) and "://" not in ref and not ref.startswith("mailto:")


def git(d, *args):
    return subprocess.run(["git", "-C", d, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")


def local_checkout(base, owner, repo):
    """a checkout of owner/repo in the estate: this repository, or a folder of that name up to three levels above"""
    root = repo_root(base)
    seen, d = [root], root
    for _ in range(3):
        d = os.path.dirname(d)
        seen += [os.path.join(d, repo)]
    for c in seen:
        if os.path.isdir(c):
            url = git(c, "remote", "get-url", "origin").stdout.strip().lower()
            if url.rstrip("/").removesuffix(".git").endswith(f"{owner}/{repo}".lower()):
                return c
    return None


def resolve(ref, base, offline):
    """found · missing · unreachable · malformed, and the checkout it was found in"""
    m = REMOTE.match(ref)
    if not m:
        return "malformed", None
    owner, repo, rev, path = m.group("owner", "repo", "rev", "path")
    c = local_checkout(base, owner, repo)
    if c:
        if git(c, "cat-file", "-e", f"{rev}:{path}").returncode == 0 or git(c, "ls-tree", rev, "--", path).stdout.strip():
            return "found", c                                  # a file, a folder, or a gitlink (submodule entry)
        if git(c, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}").returncode == 0:
            return "missing", c
    if offline:
        return "unreachable", None
    gh = lambda u: subprocess.run(["gh", "api", u, "--silent"], capture_output=True, text=True)
    try:
        if gh(f"repos/{owner}/{repo}").returncode != 0:
            return "unreachable", None
        return ("found" if gh(f"repos/{owner}/{repo}/contents/{path}?ref={rev}").returncode == 0 else "missing"), None
    except FileNotFoundError:                                   # no platform client on this machine
        return "unreachable", None


def check(path, since=None, glossary=None, depth=0, offline=False):
    r = Report()
    text = open(path, encoding="utf-8").read()
    base = os.path.dirname(os.path.abspath(path))
    root = repo_root(base)
    fm, lines = split(text)
    if jsonschema is None:
        r.fail("front-matter", "the jsonschema package is required for this check")
        return r
    rule = json.load(open(RULE_SCHEMA, encoding="utf-8"))

    # front-matter (R1)
    if fm is None:
        r.fail("front-matter", "no YAML front matter")
        fm = {}
    else:
        for e in jsonschema.Draft202012Validator({k: v for k, v in rule.items() if k != "$defs"}).iter_errors(fm):
            r.fail("front-matter", f"{'/'.join(map(str, e.path)) or '(root)'}: {e.message}")
    if fm.get("id") and os.path.basename(path) != f"{fm['id']}.md":
        r.fail("front-matter", f"the file is not named {fm['id']}.md")

    # parts (R2)
    parts, order = parts_of(lines)
    if order != list(range(1, 9)):
        r.fail("parts", f"the level-2 headings are numbered {['?' if n is None else n for n in order]}, not 1 to 8 in order")
    body = lambda n: parts.get(n, ("", []))[1]

    # parts: part 1 is one paragraph (R2)
    paras = [p for p in re.split(r"\n\s*\n", "\n".join(body(1)).strip()) if p.strip()]
    if 1 in parts and len(paras) != 1:
        r.fail("parts", f"part 1 has {len(paras)} paragraphs, not one")

    # touches (R4)
    for t in fm.get("touches", []) or []:
        if not os.path.exists(os.path.join(base, f"{t}.md")) and not glob.glob(os.path.join(root, "**", f"{t}.md"), recursive=True):
            r.gap("touches", f"`{t}`: no specification of that id yet")

    # terms (R5)
    gdir = glossary or find_up(base, os.path.join("glossary", "terms"))
    if not gdir:
        r.gap("terms", "no glossary found to resolve the terms against")
    else:
        known = {os.path.splitext(x)[0] for x in os.listdir(gdir)}
        for t in fm.get("terms", []) or []:
            if t not in known:
                r.fail("terms", f"`{t}` does not resolve in the glossary")
    p3 = "\n".join(body(3))
    for t in fm.get("terms", []) or []:
        if re.search(rf"\*\*{re.escape(t)}\*\*\s*(is|are|:|—)|^\s*[-*]\s*`?{re.escape(t)}`?\s*:", p3, re.I | re.M):
            r.fail("terms", f"part 3 defines `{t}`; it belongs in the glossary and part 3 links it")

    # table, ids, levels, two-channels, checks (R6–R10)
    head, rows = table(body(4))
    reqs = []
    if head != COLUMNS:
        r.fail("table", f"part 4's table has the columns {head}, not {COLUMNS}")
    else:
        rowschema = dict(rule["$defs"]["requirement"], **{"$schema": rule["$schema"]})
        for c in rows:
            if len(c) != 5:
                r.fail("table", f"a row has {len(c)} cells, not 5: {' | '.join(c)[:60]}")
                continue
            row = dict(zip(["id", "level", "requirement", "why", "check"], c))
            reqs.append(row)
            for e in jsonschema.Draft202012Validator(rowschema).iter_errors(row):
                r.fail("table", f"{row['id']}: {'/'.join(map(str, e.path)) or 'row'}: {e.message}")
    own = declared_checks(body(6))                             # R10: the subject's own checks, declared in its part 6
    tool = os.path.normpath(os.path.join(base, fm["check"])) if fm.get("check") else None
    seen = set()
    for q in reqs:
        if q["id"] in seen:
            r.fail("ids", f"{q['id']} is used twice")
        seen.add(q["id"])
        if q["level"] not in ("MUST", "SHOULD"):
            r.fail("levels", f"{q['id']}: level {q['level']}")
        if sentences(q["requirement"]) != 1:
            r.fail("two-channels", f"{q['id']}: the Requirement is not one sentence")
        if not 1 <= sentences(q["why"]) <= 2:
            r.fail("two-channels", f"{q['id']}: the Why holds {sentences(q['why'])} sentences, not one or two")
        c = q["check"]
        if c in ("schema", "review"):
            continue
        if c not in own:
            r.fail("checks", f"{q['id']}: check `{c}` is neither schema, review nor a check declared in part 6")
        elif not tool:
            r.fail("checks", f"{q['id']}: check `{c}` is declared, but the front matter names no `check` tool")
        elif os.path.exists(tool) and c not in open(tool, encoding="utf-8", errors="replace").read():
            r.gap("checks", f"{q['id']}: the tool `{fm['check']}` does not name `{c}`; resolving is not running it")
    if since:
        old = subprocess.run(["git", "-C", base, "show", f"{since}:./{os.path.basename(path)}"],
                             capture_output=True, text=True, encoding="utf-8")
        if old.returncode == 0:
            _, oh = split(old.stdout)
            oparts, _ = parts_of(oh)
            _, orows = table(oparts.get(4, ("", []))[1])
            before = {c[0]: c[2] for c in orows if len(c) == 5}
            now = {q["id"]: q["requirement"] for q in reqs}
            for i in sorted(set(before) - set(now)):
                r.should("ids", f"{i} was removed since {since}; it must never return for another requirement")
            for i in sorted(set(before) & set(now)):
                if before[i] != now[i]:
                    r.should("ids", f"{i} changed its text since {since}; is it still the same requirement?")
        else:
            r.gap("ids", f"the file did not exist at {since}")
    if fm.get("check") and not os.path.exists(os.path.normpath(os.path.join(base, fm["check"]))):
        (r.gap if fm.get("status") == "draft" else r.fail)("checks", f"the tool `{fm['check']}` does not exist yet")

    # schema (R11)
    target = None
    if fm.get("schema"):
        p = os.path.normpath(os.path.join(base, fm["schema"]))
        if not os.path.exists(p):
            r.fail("schema", f"the schema `{fm['schema']}` does not exist")
        else:
            try:
                target = json.load(open(p, encoding="utf-8")) if p.endswith(".json") else yaml.safe_load(open(p, encoding="utf-8"))
            except Exception as e:                                # noqa: BLE001 — any parse error is the finding
                r.fail("schema", f"the schema `{fm['schema']}` does not parse: {str(e)[:80]}")
    if target is not None:
        try:
            jsonschema.Draft202012Validator.check_schema(target)
        except jsonschema.SchemaError as e:
            r.fail("schema", f"not a valid JSON Schema: {e.message}")
            target = None

    # gaps (R12) is this report itself: fail · should · gap, exit 1 only on a fail

    # example (R13)
    p7 = "\n".join(body(7))
    linked = [os.path.normpath(os.path.join(base, x)) for x in (fm.get("examples") or [])]
    linked += [os.path.normpath(os.path.join(base, x)) for x in re.findall(r"\]\(([^)#\s]+\.md)\)", p7)]
    linked = list(dict.fromkeys(linked))
    data = blocks(body(7), {"yaml", "yml", "json"})
    minimal_ok = False
    for x in linked:
        if not os.path.exists(x):
            r.fail("example", f"the example `{os.path.relpath(x, base)}` does not exist")
        elif depth == 0:
            sub = check(x, glossary=glossary, depth=1, offline=offline)
            fails = [t for o, _, t in sub.items if o == "fail"]
            if fails:
                r.fail("example", f"the example `{os.path.relpath(x, base)}` does not pass: {fails[0]}")
            else:
                minimal_ok = True
        else:
            minimal_ok = True
    for lang, src in data:
        try:
            doc = json.loads(src) if lang == "json" else yaml.safe_load(src)
        except Exception as e:                                    # noqa: BLE001
            r.fail("example", f"the example in part 7 does not parse: {str(e)[:80]}")
            continue
        if target is not None:
            errs = list(jsonschema.Draft202012Validator(target).iter_errors(doc))
            if errs:
                r.fail("example", f"the example in part 7 does not validate: {errs[0].message}")
                continue
        minimal_ok = True
    if 7 in parts and not minimal_ok:
        r.fail("example", "part 7 holds or links no minimal example that passes")

    # decisions (R15)
    dh, drows = table(body(8))
    col = {h.lower(): i for i, h in enumerate(dh or [])}
    di, ki = col.get("date"), col.get("kind")
    if 8 in parts and (di is None or ki is None):
        r.fail("decisions", "part 8's table has no Date or no Kind column")
    adopted = set()
    for c in drows:
        if di is not None and di < len(c) and not DATE.match(c[di]):
            r.fail("decisions", f"`{c[di]}` is not a date")
        if ki is not None and ki < len(c):
            if c[ki] not in KINDS:
                r.fail("decisions", f"kind `{c[ki]}` is none of {sorted(KINDS)}")
            elif c[ki] == "adopted" and di is not None:
                adopted.add(c[di])
    if fm.get("status") == "decided" and not adopted:
        r.fail("decisions", "status is decided, but part 8 has no row of kind `adopted`")

    # carry-over (R26): the file carry-over/<id>.md beside the specification says what happens to each superseded
    # text and carries or drops its rules; a table still in part 8 is read, and reported as unmigrated
    sup = [w for w in (fm.get("supersedes") or [])]
    cf = os.path.join(base, "carry-over", f"{fm.get('id')}.md")
    if os.path.exists(cf):
        p8l = open(cf, encoding="utf-8").read().splitlines()
    else:
        p8l = body(8)
        if sup:
            r.gap("carry-over", f"the carry-over is still in part 8; it belongs in `carry-over/{fm.get('id')}.md`: unmigrated")
    p8 = "\n".join(p8l)
    for w in sup:
        if remote_like(w):
            st, where = resolve(w, base, offline)
            if st == "malformed":
                r.fail("references", f"`{w}` is not of the form owner/repo@rev:path")
                continue
            if st == "unreachable":
                r.gap("references", f"`{w}`: the repository cannot be reached from here")
            elif st == "missing":
                r.fail("references", f"`{w}` does not exist at that revision")
                continue
            if w not in p8:
                r.fail("carry-over", f"the carry-over does not say what happens to `{w}`")
            if fm.get("status") == "decided" and st == "found":
                current = os.path.join(where, REMOTE.match(w).group("path")) if where else None
                if not current or not os.path.exists(current):
                    r.gap("carry-over", f"`{w}`: the mark in its current version cannot be read from here")
                else:
                    t = open(current, encoding="utf-8", errors="replace").read()
                    if fm.get("id", "") not in t or not re.search(r"retired|superseded|revised", t, re.I):
                        r.fail("carry-over", f"`{w}` carries no mark naming {fm.get('id')}")
            continue
        hits = glob.glob(os.path.join(base, w))
        if not hits:
            r.fail("carry-over", f"the superseded text `{w}` does not exist")
            continue
        if w not in p8:
            r.fail("carry-over", f"the carry-over does not say what happens to `{w}`")
        if fm.get("status") == "decided":
            for h in hits:
                t = open(h, encoding="utf-8", errors="replace").read()
                if fm.get("id", "") not in t or not re.search(r"retired|superseded|revised", t, re.I):
                    r.fail("carry-over", f"`{w}` carries no mark naming {fm.get('id')}")
    if sup:
        k = next((n for n, l in enumerate(p8l) if re.match(r"^\*\*Carry-over\*\*|^#{1,4}\s+Carry-over", l.strip())), None)
        if k is None:
            r.fail("carry-over", "`supersedes` is not empty, but there is no Carry-over table")
        else:
            ch, crows = table(p8l[k + 1:])
            cols = {h.lower(): i for i, h in enumerate(ch or [])}
            need = ["text", "rule", "outcome", "requirement", "reason", "word"]
            if [x for x in need if x not in cols]:
                r.fail("carry-over", f"the Carry-over table lacks the columns {[x for x in need if x not in cols]}")
            else:
                ids = {q["id"] for q in reqs}
                examined = set()
                cell = lambda c, x: c[cols[x]].strip() if cols[x] < len(c) else ""
                for c in crows:
                    named = re.findall(r"`([^`]+)`", cell(c, "text"))
                    hit = [w for w in named if w in sup]
                    if not hit:
                        r.fail("carry-over", f"a row names no text listed in `supersedes`: {cell(c, 'text')[:60]}")
                        continue
                    examined.update(hit)
                    out, rule = cell(c, "outcome"), cell(c, "rule")[:40]
                    if out == "carried":
                        rid = cell(c, "requirement")
                        if not re.fullmatch(r"R[1-9][0-9]*", rid):
                            r.fail("carry-over", f"`{rule}` is carried, but names no requirement id")
                        elif rid not in ids:
                            r.fail("carry-over", f"`{rule}` is carried to {rid}, which is no requirement of part 4")
                    elif out == "dropped":
                        if not cell(c, "reason") or not cell(c, "word"):
                            r.fail("carry-over", f"`{rule}` is dropped without a reason and the accountable human's word")
                    else:
                        r.fail("carry-over", f"`{rule}`: outcome `{out}` is neither carried nor dropped")
                for w in sup:
                    if w not in examined:
                        (r.fail if fm.get("status") == "decided" else r.gap)(
                            "carry-over", f"`{w}` is not examined: no row carries or drops its rules")

    # size: at most SIZE lines, no heading below level 4 (R17)
    n = len(text.splitlines())
    if n > SIZE:
        r.fail("size", f"{n} lines, above {SIZE}")

    # references: relative links resolve, a text in another repository is owner/repo@rev:path (R25)
    for line in lines:
        for ref in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", line):
            if "://" in ref or ref.startswith("mailto:"):
                continue
            if remote_like(ref):
                st, _ = resolve(ref, base, offline)
                if st == "malformed":
                    r.fail("references", f"`{ref}` is not of the form owner/repo@rev:path")
                elif st == "missing":
                    r.fail("references", f"`{ref}` does not exist at that revision")
                elif st == "unreachable":
                    r.gap("references", f"`{ref}`: the repository cannot be reached from here")
            elif not os.path.exists(os.path.normpath(os.path.join(base, ref))):
                r.fail("references", f"`{ref}` does not resolve from the specification's folder")
        m = re.match(r"^(#{5,6})\s", line)
        if m:
            r.fail("size", f"a heading of level {len(m.group(1))}: {line.strip()[:60]}")
    return r


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("specs", nargs="+")
    ap.add_argument("--since", help="a revision: no requirement id is reused (R7)")
    ap.add_argument("--glossary", help="the glossary's terms folder")
    ap.add_argument("--offline", action="store_true", help="resolve owner/repo@rev:path only in local checkouts")
    a = ap.parse_args()
    failed = False
    for s in a.specs:
        rep = check(s, a.since, a.glossary, offline=a.offline)
        c = {o: sum(1 for x in rep.items if x[0] == o) for o in ("fail", "should", "gap")}
        print(f"# {s}: {c['fail']} fail · {c['should']} should · {c['gap']} gap")
        for o, chk, t in rep.items:
            print(f"{o}: {chk}: {t}")
        failed |= c["fail"] > 0
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
