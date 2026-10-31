#!/usr/bin/env python3
"""check_fabric.py — what a commons took in from its systems of record is a reading, never a record (fabric.md).
Read-only.

Reports each finding as fail (a MUST), should (a SHOULD) or gap (missing or unverifiable, not wrong), and exits with
1 only on a fail. The check ids are those of fabric.md part 6:

  layout  systems  readings

A reading's element is resolved against the CORE's registry; one the registry does not hold yet is a gap. Whether a
reading stayed as it was first committed is read from git; outside git, a gap. A reading may change once, to its
withdrawal, and no other way; it is read against its query as the register held it when the reading was first
committed, a query keeps its meaning once a reading was taken by it, and no reading git ever held is gone. The Fabric is
read where `locations` moves it (CORE R7), a move followed through git; one moved to another repository is checked
there. A CORE without a Fabric is a gap only where git never held a reading of it.

Usage:  check_fabric.py CORE
"""
import glob
import json
import os
import re
import subprocess
import sys

import jsonschema
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check_core import EMAIL, PHONE, Report  # noqa: E402
from check_spec import remote_like  # noqa: E402

SCHEMA = json.load(open(os.path.join(HERE, "..", "schemas", "fabric.schema.json"), encoding="utf-8"))
SPECS = {"fabric": ["layout", "systems", "readings"]}
GRAMMAR = set(json.load(open(os.path.join(HERE, "..", "schemas", "model.schema.json"), encoding="utf-8"))["$defs"]["address"]["properties"]["to"]["properties"]["kind"]["enum"])
SECRET = re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_|AKIA[0-9A-Z]{16}|-----BEGIN|xox[bp]-|password\s*[=:]|[A-Za-z0-9+/_-]{32,})")


def yml(p):
    try:
        return yaml.safe_load(open(p, encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return None


def git(core, *args):
    try:
        out = subprocess.run(["git", "-C", core, *args], capture_output=True)
        return out.stdout if out.returncode == 0 else None
    except OSError:
        return None


def elements(core):
    """the elements of the registry a query may be read against: `<kind>:<slug>`, and a stream's steps"""
    out = set()
    for p in glob.glob(os.path.join(core, "registry", "*", "*.y*ml")):
        r = yml(p) or {}
        if isinstance(r, dict) and r.get("kind") and r.get("slug"):
            out.add(f"{r['kind']}:{r['slug']}")
            for st in r.get("steps") or []:
                if isinstance(st, dict) and st.get("slug"):
                    out.add(f"step:{r['slug']}/{st['slug']}")
    return out


def first_of(core, rel):
    """the commit a reading was first taken in and its path then, followed across a move (R1, R5)"""
    out = (git(core, "log", "--follow", "--name-only", "--format=%x00%H", "--", rel) or b"").decode().split("\0")
    seen = [x.split() for x in out if len(x.split()) > 1]
    return (seen[-1][0], seen[-1][1]) if seen else None


def target(to):
    """an address's target as the registry names it: `<kind>:<slug>`, a step as `step:<stream>/<step>`"""
    return f"{to.get('kind')}:{to.get('slug')}"


def query_of(reg, system, query):
    """a query of a register, by its system's id and its own, or None"""
    s = next((x for x in (reg or {}).get("systems") or [] if isinstance(x, dict) and x.get("id") == system), None)
    return next((x for x in (s or {}).get("queries") or [] if isinstance(x, dict) and x.get("id") == query), None)


def people(core):
    doc = yml(os.path.join(core, "people.yml")) or {}
    items = doc.get("people") if isinstance(doc, dict) else doc
    return [str(p.get("name")) for p in items or [] if isinstance(p, dict) and p.get("name")]


def errors(sch, doc):
    return [f"{'/'.join(str(p) for p in e.path) or 'root'}: {e.message}" for e in jsonschema.Draft202012Validator(sch).iter_errors(doc)]


def check(core):
    r = Report()
    moved_to = str(((yml(os.path.join(core, ".commons", "commons.yml")) or {}).get("locations") or {}).get("fabric") or "")
    if moved_to and remote_like(moved_to):
        r.gap("layout", f"the Fabric is moved to `{moved_to}`; it is checked in its own repository (R1; core R7)")
        return r
    fd = os.path.normpath(os.path.join(core, moved_to or "fabric"))
    in_git = git(core, "rev-parse") is not None
    pre = (git(core, "rev-parse", "--show-prefix") or b"").decode().strip() if in_git else ""
    at = sorted({"fabric", moved_to.strip("/")} - {""})                 # every reading git ever held, at its place or where it moved
    added = (git(core, "log", "--format=", "--name-only", "--diff-filter=A", "HEAD", "--", *(f"{d}/readings" for d in at)) or b"").decode() if in_git else ""
    taken = {l.rsplit("/", 1)[-1] for l in added.splitlines() if l.startswith(tuple(f"{pre}{d}/readings/" for d in at))}
    # layout (R1)
    if not os.path.isdir(fd):
        if not taken:
            r.gap("layout", "the CORE has no `fabric/` yet: it reads none of its systems (R1)")
        for name in sorted(taken):                 # an established Fabric never disappears without its move declared (R1, R5)
            r.fail("readings", f"`{name}` was taken and the Fabric that held it is gone, with no move in `locations`; a withdrawn reading leaves its id and reason in its place (R1, R5)")
        return r
    for x in sorted(os.listdir(fd)):
        if x not in ("systems.yml", "readings"):
            r.fail("layout", f"`fabric/{x}` is neither the register nor `readings/` (R1)")
    reg = yml(os.path.join(fd, "systems.yml"))
    if reg is None:
        r.fail("layout", "`fabric/` has no register `systems.yml` (R1)")
        return r
    # systems (R2, R9)
    for e in errors(SCHEMA, reg):
        r.fail("systems", f"`fabric/systems.yml`: {e} (R2)")
    held = elements(core)
    systems = {}
    for s in reg.get("systems") or []:
        if not isinstance(s, dict):
            continue
        if s.get("id") in systems:
            r.fail("systems", f"two systems share the id `{s.get('id')}` (R2)")
        systems[s.get("id")] = s
        if SECRET.search(str(s.get("access") or "")):
            r.fail("systems", f"the system `{s.get('id')}` names its access by what looks like a secret; it names a reference (R2, R9)")
        seen = set()
        for q in s.get("queries") or []:
            if not isinstance(q, dict):
                continue
            if q.get("id") in seen:
                r.fail("systems", f"the system `{s.get('id')}` has two queries `{q.get('id')}` (R2)")
            seen.add(q.get("id"))
            a = q.get("about") if isinstance(q.get("about"), dict) else {}
            to = a.get("to") if isinstance(a.get("to"), dict) else {}
            at = f"the query `{s.get('id')}/{q.get('id')}`"
            if to.get("kind") not in GRAMMAR:                  # MODEL R24: a target the grammar cannot hold fails
                r.fail("systems", f"{at} is read against a `{to.get('kind')}`, which the grammar cannot hold (R2; model R24)")
            elif target(to) not in held:                        # one this model does not hold yet is a gap
                r.gap("systems", f"{at} is read against `{target(to)}`, which the registry does not hold (R2; model R24)")
            if a and a.get("status") != "ratified":            # only a ratified address counts
                r.fail("systems", f"{at}: its address is `{a.get('status')}`; only a ratified one is read (R2; model R24)")
    # readings (R4, R5, R6)
    names = people(core)
    moved = set()
    for p in sorted(glob.glob(os.path.join(fd, "readings", "*"))):
        w = f"`fabric/readings/{os.path.basename(p)}`"
        doc = yml(p)
        if not p.endswith((".yml", ".yaml")) or not isinstance(doc, dict):
            r.fail("readings", f"{w} is no reading (R4)")
            continue
        for e in errors({**SCHEMA["$defs"]["reading"], "$defs": SCHEMA["$defs"]}, doc):
            r.fail("readings", f"{w}: {e} (R4)")
        if str(doc.get("id")) != "reading:" + os.path.basename(p).rsplit(".", 1)[0]:
            r.fail("readings", f"{w}: its id `{doc.get('id')}` is not its file's name (R4)")
        s = systems.get(doc.get("system"))
        q = query_of(reg, doc.get("system"), doc.get("query"))
        rel = os.path.relpath(p, core).replace(os.sep, "/")
        first = first_of(core, rel) if in_git else None
        then = query_of(yaml.safe_load(git(core, "show", f"{first[0]}:{first[1].rsplit('/', 2)[0]}/systems.yml") or b"") or {},
                        doc.get("system"), doc.get("query")) if first else None
        if q is not None and then is not None:          # a reading is read against its query as it was when taken (R2, R5)
            qid = f"{doc.get('system')}/{doc.get('query')}"
            if {k: then.get(k) for k in ("about", "yields")} != {k: q.get(k) for k in ("about", "yields")} and qid not in moved:
                moved.add(qid)
                r.fail("systems", f"the query `{qid}` changed its address or what it yields after a reading was taken by it; a new meaning is a new query (R2, R5)")
            q = then
        if s is None or q is None:
            r.fail("readings", f"{w}: `{doc.get('system')}/{doc.get('query')}` is no query of the register (R2, R4)")
        else:
            want = ((q.get("about") or {}).get("to") or {}) if isinstance(q.get("about"), dict) else {}
            if doc.get("about") != want:
                r.fail("readings", f"{w}: read against `{doc.get('about')}`, while its query's address names `{want}` (R4)")
            res, y = doc.get("result") or {}, q.get("yields") or {}
            if res and ("signal" in y) != ("signal" in res):
                r.fail("readings", f"{w}: its result is not the {'signal' if 'signal' in y else 'value'} its query yields (R4)")
            elif res and "unit" in y and res.get("unit") != y.get("unit"):
                r.fail("readings", f"{w}: its unit `{res.get('unit')}` is not its query's `{y.get('unit')}` (R4)")
        text = open(p, encoding="utf-8", errors="replace").read()
        if EMAIL.search(text) or PHONE.search(text) or any(n and n in text for n in names):
            r.fail("readings", f"{w} names a person or holds a contact datum (R6)")
        if in_git:
            if first:
                was = yaml.safe_load(git(core, "show", f"{first[0]}:{first[1]}") or b"") or {}
                now = dict(doc)
                if now != was and not (now.get("withdrawn") and {k: v for k, v in now.items() if k != "withdrawn"} == {k: v for k, v in was.items() if k != "result"}):
                    r.fail("readings", f"{w} changed after it was first taken, other than by its withdrawal (R5)")
        else:
            r.gap("readings", f"{w}: the CORE is not in git; that the reading never changed is unverified (R5)")
    for name in sorted(taken):
        if not os.path.isfile(os.path.join(fd, "readings", name)):
            r.fail("readings", f"`{name}` was taken and is gone; a withdrawn reading leaves its id and reason in its place (R5)")
    return r


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    r = check(sys.argv[1])
    n = {o: sum(1 for i in r.items if i[0] == o) for o in ("fail", "should", "gap")}
    print(f"# {sys.argv[1]}: {n['fail']} fail · {n['should']} should · {n['gap']} gap")
    for o, c, t in r.items:
        print(f"{o}: {c}: {t}")
    return 1 if n["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
