#!/usr/bin/env python3
"""check_core.py — a repository is a well-formed Commons CORE (core.md, core-knowledge.md, core-views.md). Read-only.

Reports each finding as fail (a MUST), should (a SHOULD) or gap (missing, not wrong), and exits with 1 only on a
fail. The check ids are those of the three specifications, part 6:

  core            commons  names  layout  registry  lifecycle  people  world  build  patterns  agent  bill
  core-knowledge  knowledge  sources  claims  ladder  expectations  corrections  register  private
  core-views      sections  views  build-record

The ids are unique across the three, so that each resolves to one specification; --spec reports the findings of one
specification only.

Installed specifications (R26) are read from the generated lock `.commons/lock.yml` (`specs: [{path, origin,
version}]`) and compared with their origin, read from a local checkout at that revision. An installed extract of
patterns (R28, R29) is read from the same lock (`patterns: [{path, origin, record}]`) and checked as a release copy
by check_library.py's `check_copy` against that record digest, the one code of every copy (LIBRARY R8, R9); its origin
is not resolved here.

The bill of materials (R37) is generated, never kept: the lock's installed and served parts, the systems of the
Fabric and the COREs the graph reads, and the archetypes the registry adopted, one line each; --bill prints it.

The structure definition is Commons Essentials' `specs/structure.yml` (part 5): the CORE's installed copy, else the
one beside this tool, where its version is the one the CORE declares; else the reference this tool pins as its
default, from a local checkout of that repository at that revision; or the file given with --structure. Where the one of the CORE's declared version is not at hand, the
layout is reported as a gap, not guessed. A part moved by
`locations` is checked where it was moved to: a folder of the CORE, or owner/repo@rev:path read from a local checkout
at that revision. What cannot be read there is reported as unverified, never passed.

Usage:  check_core.py CORE [--structure structure.yml] [--spec core|core-knowledge|core-views] [--offline] [--bill]
"""
import argparse
import datetime
import glob
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

import jsonschema
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMAS = os.path.join(HERE, "..", "schemas")
STRUCTURE = "Commons-Engineering/workshop@f2baad1eb4:_extensions/cloudsters-commons-essentials/structure/structure.yml"   # the default where no `specs/structure.yml` of the declared version is at hand
AREAS = ["registry", "knowledge", "operations", "lifecycle", "workshop", "views", "specs", "patterns", "offer", "graph", "fabric"]
LOCK = os.path.join(".commons", "lock.yml")   # the generated lock (part 5)
REQUIRED_AREAS = ["registry", "lifecycle"]
EMAIL = re.compile(r"(?<![\w.+/-])[\w.+-]+@[\w-]+(\.[\w-]+)*\.[A-Za-z]{2,}\b")   # never owner/repo@rev, nor an extension@version
PHONE = re.compile(r"\+\d[\d ()-]{7,}\d")
NAME = re.compile(r"^([a-z0-9-]+\.){0,2}[a-z0-9-]+(\.[0-9]+)?\.core$")
RUNG = {"belegt": "evidenced", "established": "evidenced", "Beleg": "evidenced",
        "unbestätigt": "claimed", "unbestaetigt": "claimed", "website": "claimed", "marktreport": "claimed",
        "intern": "claimed", "inferred": "claimed", "abgeleitet": "claimed", "gerechnet": "claimed",
        "Nachweis": "claimed", "Annahme": "assumed", "hypothesis": "assumed",
        "divergent": "contested", "contested": "contested", "contested-strong": "contested"}
KINDS = {"briefing", "lighthouse", "spoken", "portal", "card", "gaps", "curriculum"}
OUTCOMES = {"covered", "not-selected", "missing", "documented-absence", "unsighted"}
DEFINITIONS = ["blueprint", "view", "structure"]
HASH = re.compile(r"^[0-9a-f]{64}$")
AGENT_PARTS = ["1 · Who", "2 · Where", "3 · How it answers", "4 · What it never does", "5 · How a role starts"]
OWN = "## Own guidance"
QID = re.compile(r"^[a-z0-9][a-z0-9.-]*/[A-Za-z0-9_.-]+$")   # a source-qualified pattern id (R30)
RELEASE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9._-]+@[^\s:@]+$")
EXTRACT = ["path", "origin", "record"]
EXPECTATION = re.compile(r"(^|[/:])(\.build|graph/runs)/")   # where expectations and computed edges are kept
SPECS = {"core": ["commons", "names", "layout", "registry", "lifecycle", "people", "world", "build", "patterns", "agent", "bill", "federation"],
         "core-knowledge": ["knowledge", "sources", "claims", "ladder", "expectations", "corrections", "register", "private"],
         "core-views": ["sections", "views", "build-record"]}

sys.path.insert(0, HERE)
import check_model  # noqa: E402
from check_spec import REMOTE, git, local_checkout, remote_like, resolve  # noqa: E402


class Report:
    def __init__(self):
        self.items = []

    def fail(self, check, text):
        self.items.append(("fail", check, text))

    def should(self, check, text):
        self.items.append(("should", check, text))

    def gap(self, check, text):
        self.items.append(("gap", check, text))


def schema(name):
    return json.load(open(os.path.join(SCHEMAS, name), encoding="utf-8"))


def validate(r, check, sch, doc, where, ref=None):
    if ref:
        sch = dict(sch["$defs"][ref], **{"$defs": sch["$defs"], "$schema": sch["$schema"]})
    for e in jsonschema.Draft202012Validator(sch).iter_errors(doc):
        r.fail(check, f"{where}: {'/'.join(map(str, e.absolute_path)) or 'root'}: {e.message[:110]}")


def yml(path):
    return yaml.safe_load(open(path, encoding="utf-8")) if os.path.exists(path) else None


def files(d):
    return [f for f in glob.glob(os.path.join(d, "**", "*"), recursive=True) if os.path.isfile(f)] if os.path.isdir(d) else []


def scan_persons(r, check, paths, skip):
    for f in paths:
        if os.path.abspath(f) in skip or not f.endswith((".yml", ".yaml", ".md", ".json")):
            continue
        t = open(f, encoding="utf-8", errors="replace").read()
        if EMAIL.search(t) or PHONE.search(t):
            r.fail(check, f"`{f}` holds an e-mail address or a telephone number")


def export(checkout, rev, path, into):
    """the tree of path at rev, written under into, or None"""
    out = subprocess.run(["git", "-C", checkout, "archive", "--format=tar", rev, "--", path], capture_output=True)
    if out.returncode:
        return None
    tarfile.open(fileobj=io.BytesIO(out.stdout)).extractall(into)
    return os.path.normpath(os.path.join(into, path))


def place(r, core, key, ref, offline, tmp):
    """where a part moved by `locations` is read, or None where it cannot be (R7)"""
    if remote_like(ref):
        state, c = resolve(ref, core, offline)
        m = REMOTE.match(ref)
        p = export(c, m["rev"], m["path"], tempfile.mkdtemp(dir=tmp)) if state == "found" and c else None
        if p:
            return p
        if state == "found":
            r.gap("layout", f"`{key}` at `{ref}` exists, but no local checkout holds that revision: its content is unverified")
        elif state == "unreachable":
            r.gap("layout", f"`{key}` at `{ref}` cannot be reached: its content is unverified")
        elif state == "missing":
            r.fail("layout", f"`{key}` is moved to `{ref}`, which does not exist at that revision")
        else:
            r.fail("layout", f"`{key}` is moved to `{ref}`, which is neither a folder nor owner/repo@rev:path")
        return None
    p = os.path.normpath(os.path.join(core, ref))
    if not os.path.exists(p):
        r.fail("layout", f"`{key}` is moved to `{ref}`, which does not exist")
        return None
    return p


def digest(path):
    """the hash of a file as git holds it, whatever the line endings of this checkout"""
    return hashlib.sha256(open(path, "rb").read().replace(b"\r\n", b"\n")).hexdigest()


def front(path):
    """the front matter of a pattern file, or None"""
    t = open(path, encoding="utf-8", errors="replace").read()
    if not t.startswith("---"):
        return None
    try:
        fm = yaml.safe_load(t.split("---", 2)[1])
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def computed(fm):
    """whether a pattern's garden block holds anything (R28, R34)"""
    g = fm.get("graph_garden")
    return any(v for v in g.values()) if isinstance(g, dict) else bool(g)


def extract(r, pd, n, e, installed):
    """one installed extract: its lock entry, and its copy checked by the gate's code of a release copy against the
    record digest its lock took from the library's index (R28, R29; LIBRARY R9)"""
    import check_library   # here, not above: it reads PHONE and Report from this module
    at = f"`{LOCK}` patterns[{n}]"
    missing = [k for k in EXTRACT if not e.get(k)]
    if missing:
        r.fail("patterns", f"{at} records no {', '.join(missing)} (R29)")
    if e.get("origin") and not RELEASE.match(str(e["origin"])):
        r.fail("patterns", f"{at}: the origin `{e['origin']}` is not owner/repo@rev (R29)")
    src = e.get("path")
    d = os.path.join(pd, str(src or ""))
    if not src or not os.path.isdir(d):
        r.fail("patterns", f"{at}: `patterns/{src}/` does not exist (R28)")
        return
    copy = check_library.Report()
    rec = check_library.check_copy(copy, d, pd, f"`patterns/{src}`", expect=e.get("record"))
    for o, c, t in copy.items:
        getattr(r, o)("patterns", f"{c}: {t} (LIBRARY R9)")
    if rec is None:
        return
    if rec.get("library") != src:
        r.fail("patterns", f"`patterns/{src}/` holds a release of `{rec.get('library')}`; it lies under its library (R28)")
    for x in [json.loads(y) for y in open(os.path.join(d, "index.jsonl"), encoding="utf-8") if y.strip()][1:]             if os.path.isfile(os.path.join(d, "index.jsonl")) else []:
        f = os.path.join(d, str(x.get("file") or ""))
        installed[x.get("id")] = {"slug": x.get("slug"), "license": (front(f) or {}).get("license") if os.path.isfile(f) else None}


def patterns(r, pd, lock):
    """the installed extracts and the commons' own patterns (R28-R30, R34)"""
    entries = (lock or {}).get("patterns") or [] if isinstance(lock, dict) else []
    if not entries:
        r.gap("patterns", "the CORE has not installed an extract yet (R28)")
    installed, recorded = {}, set()
    for n, e in enumerate(entries):
        e = e if isinstance(e, dict) else {}
        recorded.add(str(e.get("path")))
        extract(r, pd, n, e, installed)
    if not os.path.isdir(pd):
        return
    for x in sorted(os.listdir(pd)):
        if os.path.isdir(os.path.join(pd, x)) and x not in recorded:
            r.fail("patterns", f"`patterns/{x}/` is installed without a record in the lock (R29)")
    bare = {k.split("/", 1)[1] for k in installed}
    slugs = {v["slug"] for v in installed.values()}
    for f in sorted(glob.glob(os.path.join(pd, "*.md"))):
        name = f"`patterns/{os.path.basename(f)}`"
        fm = front(f)
        if fm is None or not fm.get("id"):
            r.fail("patterns", f"{name}: an own pattern without front matter or `id` (R34)")
            continue
        if fm["id"] in bare or fm.get("slug") in slugs:
            r.fail("patterns", f"{name}: takes the id or slug of an installed pattern; an adaptation names `adopted_from` (R34)")
        if computed(fm):
            r.fail("patterns", f"{name}: holds a computed relation (R34)")
        a = fm.get("adopted_from")
        if a is None:
            continue
        ref = a.get("id") if isinstance(a, dict) else a
        if not isinstance(a, dict) or not a.get("release") or not QID.match(str(ref)):
            r.fail("patterns", f"{name}: `adopted_from` names no source-qualified id and release (R30, R34)")
        elif ref not in installed:
            r.gap("patterns", f"{name}: adopted from `{ref}`, which is not installed here; its origin is unverified")
        elif fm.get("license") != installed[ref]["license"]:
            r.fail("patterns", f"{name}: does not keep the licence `{installed[ref]['license']}` of its origin (R34)")


def bill(r, core, where, lock, mark=0):
    """the CORE's single-level bill of materials (R37): one line per part it holds or uses directly, generated from
    what already holds it: the lock's installed and served parts, the systems and COREs it reads, its adopted archetypes;
    withheld only by a finding on what it lists, those from `mark` on: the lock, the installed copies, the adoptions and
    the sources read, while every other finding stands beside it"""
    import check_extension   # here, not above: it reads this module
    lock = lock if isinstance(lock, dict) else {}
    licences, digests = {}, {}
    for f in repository_files(core):
        if f.endswith((".yml", ".yaml", ".json")) and os.path.isfile(f) and governed(core, f) and kept_bill(f):
            r.fail("bill", f"`{os.path.relpath(f, core)}` holds a bill of materials; the bill is generated, never kept (R37)")
    lines = []
    sd = where.get("specs") or os.path.join(core, "specs")
    for e in lock.get("specs") or []:
        e = e if isinstance(e, dict) else {}
        f = os.path.join(sd, str(e.get("path") or ""))
        sid = (front(f) or {}).get("id") if os.path.isfile(f) else None
        lines.append({"part": f"{sid or e.get('path')}@{e.get('version')}", "usage": "installed", "origin": e.get("origin")})
    locked = set()
    for e in lock.get("extensions") or []:
        e = e if isinstance(e, dict) else {}
        ref = str(e.get("id"))
        locked.add(ref)
        rel = yml(os.path.join(core, "extensions", *ref.split("/"), "release.yml")) or {}
        licences[ref], digests[ref] = rel.get("licence"), e.get("record")
        parts = rel.get("parts") if isinstance(rel.get("parts"), dict) else {}
        for usage in ("installed", "served"):
            for p in e.get(usage) or []:
                if not isinstance(parts.get(p), dict):
                    r.fail("bill", f"`{LOCK}`: `{ref}` is {usage} with the part `{p}`, which its release record does not name (LIBRARY R3)")
                lines.append({"part": f"{ref}@{e.get('version')}#{p}", "usage": usage, "origin": e.get("origin"),
                              "record": e.get("record"), "class": (parts.get(p) or {}).get("class"), "licence": rel.get("licence")})
    for d in sorted(glob.glob(os.path.join(core, "extensions", "*", "*", ""))):
        ref = "/".join(os.path.normpath(d).split(os.sep)[-2:])
        if ref not in locked:
            r.fail("bill", f"`extensions/{ref}/` is installed without its entry in the lock (`extension` R12)")
    pins = [x for x in (yml(os.path.join(core, ".commons", "commons.yml")) or {}).get("extensions") or []
            if isinstance(x, dict) and x.get("id")]
    held = [e for e in lock.get("extensions") or [] if isinstance(e, dict) and e.get("id")]
    for x in pins:                                   # the pins against the lock, an unqualified pin read by its extension
        at = [e for e in held if same_extension(e["id"], x["id"])]
        if not at:
            r.gap("bill", f"`{x['id']}` {x.get('version')} is pinned and not installed yet; the lock has no entry for it (`extension` R12)")
        for e in at:
            if str(e.get("version")) != str(x.get("version")):
                r.fail("bill", f"`{LOCK}` holds `{e['id']}` at {e.get('version')}, but `commons.yml` pins {x.get('version')} (`extension` R20)")
    for e in held:
        if not any(same_extension(e["id"], x["id"]) for x in pins):
            r.fail("bill", f"`{LOCK}` holds `{e['id']}`, which `commons.yml` does not pin (`extension` R12)")
    pd = where.get("patterns") or os.path.join(core, "patterns")
    for e in lock.get("patterns") or []:
        e = e if isinstance(e, dict) else {}
        rel = yml(os.path.join(pd, str(e.get("path") or ""), "release.yml")) or {}
        lines.append({"part": f"{rel.get('library') or e.get('path')}/patterns@{rel.get('version')}#patterns", "usage": "installed",
                      "origin": e.get("origin"), "record": e.get("record"), "class": "public", "licence": rel.get("licence")})
    fd = where.get("fabric") or os.path.join(core, "fabric")
    for x in (yml(os.path.join(fd, "systems.yml")) or {}).get("systems") or []:
        if isinstance(x, dict) and not x.get("id"):
            r.fail("bill", "`fabric/systems.yml`: a system read names no `id`, so no line can name it")
        elif isinstance(x, dict):
            lines.append({"part": f"fabric/systems.yml#{x.get('id')}", "usage": "read", "access": x.get("access"),
                          "class": x.get("class"), "holder": x.get("holder")})
    gd = where.get("graph") or os.path.join(core, "graph")
    for x in (yml(os.path.join(gd, "sources.yml")) or {}).get("sources") or []:
        if isinstance(x, dict) and x.get("kind") == "core" and not x.get("ref"):
            r.fail("bill", f"`graph/sources.yml`: the CORE read as `{x.get('id')}` names no `ref`, so no line can name it")
        elif isinstance(x, dict) and x.get("kind") == "core":
            lines.append({"part": str(x.get("ref")), "usage": "read", "access": x.get("grant"), "class": x.get("class")})
    offers = {}
    for k, (rec, f) in sorted(check_extension.records(where.get("registry") or os.path.join(core, "registry")).items()):
        m = check_extension.ORIGIN.match(str(rec.get("adopted_from") or ""))
        if not m:
            continue
        ref = f"{m['library']}/{m['ext']}"
        if ref not in offers:
            offers[ref] = check_extension.records(os.path.join(core, "extensions", m["library"], m["ext"], "registry"))
        src = offers[ref].get(f"{m['kind']}:{m['slug']}")
        line = {"part": rec["adopted_from"], "usage": "adopted", "as": k, "record": digests.get(ref), "licence": licences.get(ref)}
        if src:
            line["adapted"] = bool(check_extension.changed(src[0], rec))
        lines.append(line)
    # the bill says what the CORE is made of only where the checks of what it lists pass: an extension it installs, serves
    # or adopts from is checked by the code of `extension`, as at install (`extension` R12, R13, R23; LIBRARY R9); a pin
    # alone is no line, so a [domain].core that pins Extension-Builders without installing it is not checked here
    if lock.get("extensions") or any(x["usage"] == "adopted" for x in lines):
        ext = check_extension.Report()
        check_extension.fit(core, ext)
        failed = [t for o, _, t in ext.items if o == "fail"]
        if failed:
            r.fail("bill", f"no bill is generated: the checks of `extension` fail on what it would list ({len(failed)}): " + "; ".join(failed))
            return None
    if any(o == "fail" for o, _, _ in r.items[mark:]):
        return None
    return dict(revision(core), lines=[{k: v for k, v in x.items() if v is not None} for x in lines])


def same_extension(a, b):
    """whether two names are one extension: equal, or, where one is unqualified, equal in the extension (`extension` R1)"""
    a, b = str(a), str(b)
    return a == b or (("/" not in a or "/" not in b) and a.split("/")[-1] == b.split("/")[-1])


def governed(core, f):
    """whether a file is of the CORE's governed state, where a kept bill would stand beside the generated one: every
    file but the copies installed from elsewhere, checked against their records, and a dated event of `lifecycle/events/`
    that passes as one, a record of what happened (the found state that healing keeps among them) (R37)"""
    at = os.path.relpath(f, core).replace(os.sep, "/").split("/")
    if at[0] in ("specs", "patterns", "extensions"):
        return False
    if at[:2] == ["lifecycle", "events"] and len(at) == 3:
        ev, t = yml(f), Report()
        validate(t, "lifecycle", schema("core.schema.json"), ev, "", "event")
        return not (isinstance(ev, dict) and not t.items)
    return True



def federation(r, core):
    """federation (R38): the dated reading of what `federation.mcp` offers each shell, generated, naming no one's access"""
    f = os.path.join(core, ".commons", "federation.yml")
    if not os.path.exists(f):
        r.gap("federation", "there is no reading of what `federation.mcp` offers each shell yet; one is taken at the next contact (R38)")
        return
    try:
        d = yml(f)
    except yaml.YAMLError as e:
        r.fail("federation", f"`.commons/federation.yml` does not parse: {str(e)[:110]}")
        return
    if not isinstance(d, dict):
        r.fail("federation", "`.commons/federation.yml` is no reading: it names whom it was read from, when, by what and each shell's offer (R38)")
        return
    at = d.get("read_at")
    d = {**d, "read_at": at.isoformat() if hasattr(at, "isoformat") else at}   # YAML reads an unquoted date or time as one
    validate(r, "federation", schema("core.schema.json"), d, "`.commons/federation.yml`", "reading")
    if isinstance(d["read_at"], str) and d["read_at"]:
        try:
            datetime.datetime.fromisoformat(d["read_at"].replace("Z", "+00:00"))
        except ValueError:
            r.fail("federation", f"`.commons/federation.yml`: read_at `{d['read_at']}` is no date or time, so the reading's age cannot be named (R38)")
    for sh, o in (d["shells"] if isinstance(d.get("shells"), dict) else {}).items():
        validate(r, "federation", schema("mcp.schema.json"), o, f"`.commons/federation.yml`: shells/{sh}", "offered")
    try:
        acc = yml(os.path.join(core, ".commons", "access.yml")) or yml(os.path.join(core, "access.yml"))
    except yaml.YAMLError:
        acc = None   # `mcp` reads it
    named = acc.get("federation") if isinstance(acc, dict) else None
    if named and d.get("from") and d["from"] != named:
        r.should("federation", f"`.commons/federation.yml` was read from `{d['from']}`, while `access.yml` names `{named}` (R38; `mcp` R24)")
    names = re.findall(r"\b(?:account|key):[^\s,'\"\]}]+", yaml.safe_dump(d, allow_unicode=True))
    held = [k for k in ("users", "accounts", "gets") if k in d]
    if names or held:
        r.fail("federation", f"`.commons/federation.yml` holds someone's access ({', '.join(names[:3] or held)}): the offer is per shell and names no one (R38; `mcp` R7, R28)")


def kept_bill(f):
    """whether a file holds a bill of materials: a `bill`, or lines each naming a part and its usage (R37)"""
    try:
        d = json.load(open(f, encoding="utf-8")) if f.endswith(".json") else yaml.safe_load(open(f, encoding="utf-8"))
    except (ValueError, yaml.YAMLError, UnicodeDecodeError):
        return False
    d = d.get("bill", d) if isinstance(d, dict) else d
    rows = d.get("lines") if isinstance(d, dict) else d
    return isinstance(rows, list) and bool(rows) and all(isinstance(x, dict) and "part" in x and "usage" in x for x in rows)


def revision(core):
    """what generated a bill and the revision of the CORE it was generated from, with `read_at` where the CORE's files
    differ from that commit, as a cut of GRAPH names a source (R37)"""
    def out(d, *a):
        p = subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)
        return p.stdout.strip() if p.returncode == 0 else ""
    url = out(HERE, "remote", "get-url", "origin")
    repo = re.sub(r"\.git$", "", url.rstrip("/")).split("github.com")[-1].lstrip("/:") if url else ""
    tool = os.path.relpath(os.path.abspath(__file__), out(HERE, "rev-parse", "--show-toplevel") or HERE).replace(os.sep, "/")
    at = {"generator": f"{repo}@{out(HERE, 'rev-parse', '--short', 'HEAD')}:{tool}" if repo else tool}
    rev = out(core, "rev-parse", "HEAD")
    if rev:
        at["rev"] = rev
        if out(core, "status", "--porcelain", "--", "."):
            at["read_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return at


def repository_files(core):
    """the files of the CORE as its repository holds them: tracked, or new and not ignored; a git-ignored local file
    is the person's, not the CORE's (commons.o#95, 6465844553)"""
    out = subprocess.run(["git", "-C", core, "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                         capture_output=True)
    if out.returncode == 0:
        return [os.path.join(core, f) for f in out.stdout.decode("utf-8").split("\0") if f]
    return glob.glob(os.path.join(core, "**", "*"), recursive=True, include_hidden=True)


def agent(r, core):
    """agent (R36): one agent-neutral AGENT.md, its five parts generated with a build record; a pointer and a folder note
    are read for whether they point to it, in any wording"""
    path = os.path.join(core, "AGENT.md")
    for p in repository_files(core):
        rel = os.path.relpath(p, core).replace(os.sep, "/")
        if not os.path.isfile(p) or rel == "AGENT.md" or rel.startswith((".git/", "specs/", ".build/")):
            continue
        if os.path.basename(p) == "AGENT.md":                       # a folder note
            lines = [l.strip() for l in open(p, encoding="utf-8", errors="replace").read().splitlines()]
            if "AGENT.md" not in next((l for l in lines if l), ""):
                r.fail("agent", f"the folder note `{rel}` does not open by pointing to `AGENT.md`")
    if not os.path.exists(path):
        r.gap("agent", "the CORE holds no `AGENT.md` yet")
        return
    text = open(path, encoding="utf-8").read()
    man = os.path.join(core, ".build", "agent", "manifest.json")
    if not os.path.exists(man):
        r.gap("agent", "`AGENT.md` is kept by hand, without its build record `.build/agent/manifest.json`: unmigrated (R4)")
        return
    gen = text.split("\n" + OWN, 1)[0]
    heads = [l[3:].strip() for l in gen.splitlines() if l.startswith("## ")]
    if heads != AGENT_PARTS:
        r.fail("agent", f"the generated part of `AGENT.md` holds the parts {heads}, not the five {AGENT_PARTS}")
    m = json.load(open(man, encoding="utf-8"))
    if m.get("output") != hashlib.sha256(gen.encode("utf-8")).hexdigest():
        r.fail("agent", "the generated part of `AGENT.md` differs from what its build record says was generated: edited by hand")
    if not m.get("inputs"):
        r.fail("agent", "the build record of `AGENT.md` names no `inputs`: it is no provenance")
    for i, h in (m.get("inputs") or {}).items():
        f = os.path.join(core, i)
        if not HASH.match(str(h)):
            r.fail("agent", f"the build record of `AGENT.md` carries no hash for `{i}`")
        elif not os.path.isfile(f) or digest(f) != h:
            r.fail("agent", f"`{i}` changed and `AGENT.md` was not regenerated in the same commit")


def structure(path, core, version=None):
    """the structure definition: a file given with --structure, else Commons Essentials' `specs/structure.yml` of the
    declared version, the CORE's installed copy or the one beside this tool, else the pinned reference from a local
    checkout"""
    if path:
        return yml(path)
    for f in (os.path.join(core, "specs", "structure.yml"), os.path.join(HERE, "..", "structure.yml")):
        sd = yml(f) if os.path.isfile(f) else None
        if isinstance(sd, dict) and version is not None and str(sd.get("version")) == str(version):
            return sd
    m = REMOTE.match(STRUCTURE)
    for base in (core, HERE):
        c = local_checkout(base, m["owner"], m["repo"])
        out = git(c, "show", f"{m['rev']}:{m['path']}") if c else None
        if out and out.returncode == 0:
            return yaml.safe_load(out.stdout)
    return None


def check(core, structure_path=None, offline=False):
    tmp = tempfile.mkdtemp(prefix="check_core-")
    try:
        return run(core, structure_path, offline, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run(core, structure_path, offline, tmp):
    r = Report()
    rule = schema("core.schema.json")
    cfg = yml(os.path.join(core, ".commons", "commons.yml"))

    # commons (R1)
    if cfg is None:
        r.fail("commons", "there is no `.commons/commons.yml`")
        return r
    validate(r, "commons", rule, cfg, "commons.yml")
    prim = [x for x in cfg.get("extensions") or [] if isinstance(x, dict) and x.get("primary")]
    if len(prim) != 1:
        r.fail("commons", f"{len(prim)} primary extensions, not exactly one")
    if cfg.get("target") and cfg.get("as_of") and cfg.get("slice") is not None:
        if int(str(cfg["as_of"])[:4]) + int(cfg["slice"]) != cfg["target"]:
            r.fail("commons", "`target` disagrees with the year of `as_of` plus `slice`")

    # names (R3)
    folder = os.path.basename(os.path.abspath(core))
    if not NAME.match(folder):
        r.gap("names", f"the folder `{folder}` is not named `[holder.][world.][commons][.slice].core`: unmigrated (R4)")
    segs = folder.removesuffix(".core").split(".")
    digits = [i for i, s in enumerate(segs) if s.isdigit()]
    sl = int(cfg.get("slice") or 0)
    if digits and (digits != [len(segs) - 1] or int(segs[-1]) != sl):
        r.fail("names", f"the folder `{folder}` names the slice {'.'.join(segs[i] for i in digits)}, the CORE states `slice` {sl}")
    elif digits and sl == 0:
        r.fail("names", f"the folder `{folder}` writes the slice 0, which is omitted")
    elif not digits and sl:
        r.fail("names", f"the folder `{folder}` does not name the slice {sl}")

    # layout (R4, R5, R7, R16)
    sd = structure(structure_path, core, cfg.get("structure"))
    if not sd or sd.get("version") != cfg.get("structure"):
        r.gap("layout", f"the structure definition {cfg.get('structure')} is not at hand; the layout is not checked")
        sd = None
    loc = cfg.get("locations") or {}
    where = {}
    if sd:
        areas = dict(sd.get("areas") or {})
        areas.setdefault("knowledge", {"path": "knowledge", "earlier": ["workshop/evidence", "instance/workshop/evidence"]})
        keys = set(areas) | set(sd.get("paths") or {}) | {"people"}
        for k in loc:
            if k not in keys:
                r.fail("layout", f"`locations` moves `{k}`, which is no structure key")
        for k in AREAS:
            a = areas.get(k) or {"path": k}
            p = os.path.join(core, a["path"])
            if k in loc:
                where[k] = place(r, core, k, loc[k], offline, tmp)
                if files(p) and where[k] != os.path.normpath(p):
                    r.fail("layout", f"`{k}` is moved by `locations`, and its default place `{a['path']}` still holds files")
                continue
            if os.path.isdir(p):
                where[k] = p
                continue
            old = next((e for e in a.get("earlier") or [] if os.path.isdir(os.path.join(core, e))), None)
            if old:
                where[k] = os.path.join(core, old)
                r.gap("layout", f"`{k}` is at its earlier place `{old}`: unmigrated")
            elif k in REQUIRED_AREAS:
                r.fail("layout", f"the area `{k}` is missing")
        for ra in sd.get("retired_areas") or []:
            if files(os.path.join(core, ra)):
                r.fail("layout", f"the retired area `{ra}` holds files")
        if os.path.exists(os.path.join(core, ".commons", "account.yml")):
            r.fail("layout", "`.commons/account.yml` is an engagement record inside the CORE")
    else:
        for k in AREAS:
            if k in loc:
                where[k] = place(r, core, k, loc[k], offline, tmp)
            elif os.path.isdir(os.path.join(core, k)):
                where[k] = os.path.join(core, k)

    # registry (R6)
    reg = where.get("registry")
    if reg and sd:
        gens = {}
        for e in sd.get("elements") or []:
            names = [e["folder"]] + [x["folder"] for x in e.get("earlier") or []]
            full = [n for n in names if files(os.path.join(reg, n))]
            if len(full) > 1:
                r.fail("registry", f"element `{e['key']}` is held in {full}: two generations at once")
            gens[e["key"]] = full
        if any(full and full[0] != e["folder"] for e in sd.get("elements") or [] for full in [gens.get(e["key"])]):
            r.gap("registry", "the registry is on an earlier generation of element folders: unmigrated")
    if reg:
        rep = check_model.check(check_model.load(reg), extension=cfg.get("instance_type") == "extension")
        for o, c, t in rep.items:
            if o == "fail":
                r.fail("registry", f"{c}: {t}")
        n = sum(1 for o, _, _ in rep.items if o == "gap")
        if n:
            r.gap("registry", f"the model holds {n} gaps (check_model.py lists them)")

    # lifecycle (R11, R12, R13)
    lc = where.get("lifecycle")
    if lc:
        events = {}
        for f in sorted(glob.glob(os.path.join(lc, "events", "*.y*ml"))):
            ev = yml(f) or {}
            validate(r, "lifecycle", rule, ev, os.path.relpath(f, core), "event")
            if ev.get("id") in events:
                r.fail("lifecycle", f"the event id `{ev.get('id')}` appears twice")
            events[ev.get("id")] = ev
        st = yml(os.path.join(lc, "stage.yml"))
        if st is None:
            r.gap("lifecycle", "there is no `stage.yml` yet")
        else:
            validate(r, "lifecycle", rule, st, "stage.yml", "stage")
            ev = events.get(st.get("event"))
            if not ev or ev.get("kind") not in ("stage-change", "founding"):
                r.fail("lifecycle", f"`stage.yml` names `{st.get('event')}`, which is no stage-change or founding event")
        for i, ev in events.items():
            if ev.get("kind") == "correction" and ev.get("corrects") not in events:
                r.fail("lifecycle", f"the correction `{i}` names `{ev.get('corrects')}`, which is no event")

    # people (R14, R15)
    pp = loc.get("people") or ((((sd or {}).get("paths") or {}).get("people")) or {}).get("path")
    skip = set()
    if not pp:
        r.gap("people", "the place of the party register is not stated")
    else:
        pf = place(r, core, "people", pp, offline, tmp) if "people" in loc else os.path.join(core, pp)
        if pf:
            skip.add(os.path.abspath(pf))
        doc = yml(pf) if pf else None
        if pf is None:
            pass                                                # reported by place
        elif doc is None:
            r.gap("people", f"the party register `{pp}` does not exist yet")
        else:
            validate(r, "people", rule, doc, pp, "people")
    party = {p.get("id") for p in (doc or {}).get("people") or [] if isinstance(p, dict)} if pp and isinstance(doc, dict) else None
    scan_persons(r, "people", [f for k in ("registry", "operations", "lifecycle", "views") for f in files(where.get(k) or "")]
                 + files(os.path.join(core, ".commons")), skip)

    # world (R17)
    if cfg.get("instance_type") == "world" and files(where.get("knowledge") or ""):
        r.fail("world", "a world CORE holds evidence of its own in `knowledge/`")

    # specs (R5, R26): an installed specification is recorded in the lock and is the same text as its origin; from here
    # to the bill, every finding is on what the bill lists
    mark = len(r.items)
    lock = yml(os.path.join(core, LOCK))
    for n, e in enumerate((lock or {}).get("specs") or [] if isinstance(lock, dict) else []):
        where_ = f"`{LOCK}` specs[{n}]"
        origin, path, version = (e or {}).get("origin"), (e or {}).get("path"), (e or {}).get("version")
        if not version:
            r.fail("layout", f"{where_} records no version (R26)")
        m = REMOTE.match(str(origin or ""))
        if not m:
            r.fail("layout", f"{where_}: the origin `{origin}` is not owner/repo@rev:path (R26)")
            continue
        installed = os.path.join(where.get("specs") or os.path.join(core, "specs"), path or os.path.basename(m["path"]))
        if not os.path.isfile(installed):
            r.fail("layout", f"{where_}: the installed specification `{os.path.relpath(installed, core)}` does not exist")
            continue
        state, c = resolve(origin, core, offline)
        if state == "found" and c:
            shown = subprocess.run(["git", "-C", c, "show", f"{m['rev']}:{m['path']}"], capture_output=True)
            same = shown.returncode == 0 and shown.stdout.replace(b"\r\n", b"\n") == \
                open(installed, "rb").read().replace(b"\r\n", b"\n")
            if not same:
                r.fail("layout", f"`{os.path.relpath(installed, core)}` differs from its origin `{origin}`: edited in place (R26)")
        elif state == "found":
            r.gap("layout", f"`{os.path.relpath(installed, core)}`: its origin `{origin}` exists, but no local checkout holds it; unverified")
        elif state == "unreachable":
            r.gap("layout", f"`{os.path.relpath(installed, core)}`: its origin `{origin}` cannot be reached; unverified")
        else:
            r.fail("layout", f"`{os.path.relpath(installed, core)}`: its origin `{origin}` does not exist at that revision")

    # patterns (R28-R30, R34)
    patterns(r, where.get("patterns") or os.path.join(core, "patterns"), lock)

    # bill (R37)
    r.bill = bill(r, core, where, lock, mark)

    # federation (R38)
    federation(r, core)

    # agent (R36)
    agent(r, core)

    # build (R18)
    gi = os.path.join(core, ".gitignore")
    if os.path.exists(gi) and any(re.match(r"^/?\.build/?\s*$", l) for l in open(gi, encoding="utf-8")):
        r.fail("build", "`.gitignore` excludes `.build/`, so the build record is not committed")

    # knowledge, sources, claims, ladder, register, private (core-knowledge)
    kr = schema("core-knowledge.schema.json")
    kd = where.get("knowledge")
    if not kd:
        if "knowledge" not in loc and cfg.get("instance_type") != "world":   # a moved one is reported by place; a world holds none (R17)
            r.gap("knowledge", "the CORE holds no `knowledge/` yet")
    else:
        src = yml(os.path.join(kd, "sources.yml")) or {}
        src = src.get("sources") if isinstance(src, dict) else src
        ids = set()
        for s in src or []:
            validate(r, "sources", kr, s, f"source `{s.get('id')}`", "source")
            ids.add(s.get("id"))
        # a jurisdiction's law binds records in its own file, by sources of that jurisdiction (R20)
        bysrc = {s.get("id"): s for s in src or [] if isinstance(s, dict)}
        for f in sorted(glob.glob(os.path.join(kd, "jurisdictions", "*.y*ml"))):
            jd, where_j = yml(f) or {}, os.path.relpath(f, core)
            validate(r, "sources", kr, jd, where_j, "jurisdiction")
            for bd in (jd.get("bindings") or []) if isinstance(jd, dict) else []:
                for b in (bd.get("binds") or []) if isinstance(bd, dict) else []:
                    s = bysrc.get(b.get("source")) if isinstance(b, dict) else None
                    if s is None:
                        r.fail("sources", f"`{where_j}` binds `{b}`, which is no source of `sources.yml` (R20)")
                    elif s.get("jurisdiction") != jd.get("jurisdiction"):
                        r.fail("sources", f"`{where_j}` binds `{b.get('source')}` of `{s.get('jurisdiction')}`, not of `{jd.get('jurisdiction')}` (R20)")
        # expectations (R7): an expectation is cached with a build record, and a run's computed output lives in its
        # package; a source that points into either, of this CORE or another, would make a guess evidence
        for s in src or []:
            at = [str(s.get("url") or ""), str((s.get("raw") or {}).get("ref") or "") if isinstance(s.get("raw"), dict) else ""]
            if any(EXPECTATION.search(a) for a in at):
                r.fail("expectations", f"source `{s.get('id')}` points at an expectation or a run's output, never evidence: an expected statement does not return as a fact (R7)")
        cl = yml(os.path.join(kd, "claims.yml")) or {}
        cl = cl.get("claims") if isinstance(cl, dict) else cl
        cids = {c.get("id") for c in cl or []}
        for c in cl or []:
            validate(r, "claims", kr, c, f"claim `{c.get('id')}`", "claim")
            if not c.get("sources") and c.get("kind") != "derived":
                r.gap("claims", f"claim `{c.get('id')}` rests on no source yet")
            for s in c.get("sources") or []:
                if s not in ids:
                    r.fail("claims", f"claim `{c.get('id')}` names the source `{s}`, which is not in `sources.yml`")
            for i in c.get("inputs") or []:
                if i not in cids:
                    r.fail("claims", f"claim `{c.get('id')}` is derived from `{i}`, which is no claim")
            w = c.get("confidence")
            if w and w not in RUNG:
                r.fail("ladder", f"claim `{c.get('id')}`: the word `{w}` is not in the mapping of part 5")

        # corrections (R17, R18): a claim that carries a correction is the commons' own word, and names its giver from
        # the party register, the standing they held, the date, what it corrects and any further use with its word
        held = set()
        for f in files(where.get("registry") or ""):
            rec = yml(f) if f.endswith((".yml", ".yaml")) else None
            if isinstance(rec, dict) and rec.get("kind") and rec.get("slug"):
                held |= {f"{rec['kind']}:{rec['slug']}", str(rec["slug"])}
        for c in cl or []:
            if not isinstance(c, dict) or "correction" not in c:
                continue
            cid = c.get("id")
            validate(r, "corrections", kr, c, f"claim `{cid}`", "claim_with_correction")
            k = c.get("correction") if isinstance(c.get("correction"), dict) else {}
            if party is not None and k.get("given_by") not in party:
                r.fail("corrections", f"claim `{cid}`: the correction's giver `{k.get('given_by')}` is not in the party register (R17)")
            if k.get("corrects") and k["corrects"] not in cids and k["corrects"] not in held:
                r.fail("corrections", f"claim `{cid}` corrects `{k['corrects']}`, which is no claim or record of this CORE (R17)")
            if k.get("prompted") and not c.get("sources"):
                r.gap("corrections", f"claim `{cid}` was prompted by `{k['prompted']}` and rests on no source: judged on its own evidence, it corroborates nothing (R17)")
        reg_file = yml(os.path.join(kd, "stakeholders.yml")) or {}
        if cfg.get("perspective") == "observed":                # holding a CORE is no observation mandate
            for p in reg_file.get("parties") or []:
                if p.get("visibility") == "private":
                    r.fail("register", f"a twin observed from outside holds the private entry `{p.get('id')}`")
        scan_persons(r, "private", files(kd), skip)

    # sections, views, build-record (core-views)
    vr = schema("core-views.schema.json")
    vd = where.get("views")
    secs = {}
    bp = yml(os.path.join(vd, "blueprint.yml")) if vd else None
    for s in (bp or {}).get("sections") or []:
        validate(r, "sections", vr, s, f"section `{s.get('id')}`", "section")
        if s.get("id") in secs:
            r.fail("sections", f"the section id `{s.get('id')}` appears twice")
        secs[s.get("id")] = s
        if sd:
            known = set(sd.get("areas") or {}) | set(sd.get("paths") or {}) | {"knowledge", "people"} \
                | {e["key"] for e in sd.get("elements") or []}
            for n in s.get("needs") or []:
                if n not in known:
                    r.fail("sections", f"section `{s.get('id')}` needs `{n}`, which is no structure key")
    for vf in sorted(glob.glob(os.path.join(vd, "*", "view.yml"))) if vd else []:
        name = os.path.basename(os.path.dirname(vf))
        v = yml(vf) or {}
        validate(r, "views", vr, v, f"view `{name}`", "view")
        if v.get("name") and v["name"] != name:
            r.fail("views", f"view `{name}` calls itself `{v['name']}`; a view is known by its folder (R5)")
        if v.get("kind") and v["kind"] not in KINDS:
            r.should("views", f"view `{name}` is of the own kind `{v['kind']}`")
        for k in ("promise", "way_back"):
            if not v.get(k):
                r.fail("views", f"view `{name}` does not state its `{k}`")
        if cfg.get("language") and cfg["language"] not in (v.get("languages") or []):
            r.fail("views", f"view `{name}` is not rendered in the commons' own language `{cfg['language']}`")
        if bp is None:
            r.gap("views", f"view `{name}`: no blueprint definition is at hand to resolve its sections")
        else:
            for s in v.get("sections") or []:
                if s not in secs:
                    r.fail("views", f"view `{name}` names the section `{s}`, which the blueprint definition does not hold")
        for a in v.get("after") or []:
            if a == name or (yml(os.path.join(vd, a, "view.yml")) or {}).get("kind") != "curriculum":
                r.fail("views", f"view `{name}` comes after `{a}`, which is no other curriculum view of this CORE")
        rendered = [f for f in files(os.path.dirname(vf)) if os.path.basename(f) != "view.yml"]
        man = os.path.join(core, ".build", name, "manifest.json")
        if rendered and not os.path.exists(man):
            r.fail("build-record", f"view `{name}` is rendered, but has no build record `.build/{name}/manifest.json`")
        elif os.path.exists(man):
            m = json.load(open(man, encoding="utf-8"))
            for k in ("definitions", "inputs", "outcomes"):
                if not m.get(k):
                    r.fail("build-record", f"the build record of `{name}` names no `{k}`: it is no provenance")
            d = m.get("definitions") or {}
            for k in DEFINITIONS if d else []:
                if not d.get(k):
                    r.fail("build-record", f"the build record of `{name}` names no version of the {k} definition")
            if d.get("view") and d["view"] != name:
                r.fail("build-record", f"the build record of `{name}` was made for the view `{d['view']}`")
            if d.get("structure") and cfg.get("structure") and str(d["structure"]) != str(cfg["structure"]):
                r.gap("build-record", f"view `{name}` was built on structure {d['structure']}, the CORE is on {cfg['structure']}: stale")
            for i, h in (m.get("inputs") or {}).items():
                f = os.path.join(core, i)
                if not HASH.match(str(h)):
                    r.fail("build-record", f"view `{name}`: the input `{i}` carries no hash")
                elif not os.path.isfile(f) or digest(f) != h:
                    r.gap("build-record", f"view `{name}`: the input `{i}` changed since the rendering: stale")
            for s in (v.get("sections") or []) if m.get("outcomes") else []:
                if s not in m["outcomes"]:
                    r.fail("build-record", f"view `{name}`: the section `{s}` has no outcome")
            for s, o in (m.get("outcomes") or {}).items():
                if o not in OUTCOMES:
                    r.fail("build-record", f"view `{name}`, section `{s}`: `{o}` is none of the five outcomes")
                if s not in (v.get("sections") or []):
                    r.fail("build-record", f"view `{name}`: the outcome of `{s}` belongs to no section of the view")
    return r


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("core")
    ap.add_argument("--structure")
    ap.add_argument("--spec", choices=sorted(SPECS), help="report the findings of one specification only")
    ap.add_argument("--offline", action="store_true", help="read moved parts from local checkouts only")
    ap.add_argument("--bill", action="store_true", help="print the CORE's bill of materials (R37) after the findings")
    a = ap.parse_args()
    rep = check(a.core, a.structure, a.offline)
    items = [i for i in rep.items if not a.spec or i[1] in SPECS[a.spec]]
    n = {o: sum(1 for i in items if i[0] == o) for o in ("fail", "should", "gap")}
    print(f"# {a.core}{' · ' + a.spec if a.spec else ''}: {n['fail']} fail · {n['should']} should · {n['gap']} gap")
    for o, c, t in items:
        print(f"{o}: {c}: {t}")
    if a.bill and getattr(rep, "bill", None) is None:
        print("# no bill: a finding on what the bill lists withholds it (R37)")
    elif a.bill:
        print(yaml.safe_dump({"bill": rep.bill}, sort_keys=False, allow_unicode=True), end="")
    return 1 if n["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
