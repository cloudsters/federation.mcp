#!/usr/bin/env python3
"""check_library.py — a library holds releases that can be relied on (library.md), and its patterns are well formed
(library-patterns.md). Read-only.

Reports each finding as fail (a MUST), should (a SHOULD) or gap (missing or unverifiable, not wrong), and exits with
1 only on a fail. The check ids are those of the two specifications, part 6, and unique across them:

  library           layout  release  immutable  index  private  licence  where-used
  library-patterns  form  anchor  known-uses  ip  relations  lifecycle  extract

One code checks a release copy wherever it lies (`check_copy`): in its library, alone with --release, and at install,
where check_extension.py --core calls it. It reads the copy alone and never the private maker: its record, its parts
and their digests, its licence and its text, its private data, and its profile's mandatory content, the offer's checks
of EXTENSION or the specifications of Commons Essentials for an extension, the checks of library-patterns for an
extract. Whether the copy is the release its pin names is read against the record digest the pin gives (--expect);
whether a record was generated from its source's event, and by whom it was authorised, is not verified by any code yet.

Whether a released version stayed as it was first released, and whether one has left the library, is read from git;
outside git, a gap. The names a release is checked against come from --names, a file kept outside git; without it,
that part of `private` and `known-uses` is a gap. Third-party codes and trademarks come from --terms. A list finds
the names on it; it proves no text anonymous. With --core, the commons reads the library as it does: the lines of
its bill that a withholding touches, each a `should` for the commons to decide on, and nothing written to the library.

Usage:  check_library.py LIBRARY [--names FILE] [--terms FILE] [--today YYYY-MM-DD]
        check_library.py --release FOLDER [--expect sha256:...] [--names FILE] [--terms FILE]
        check_library.py --patterns FOLDER [--names FILE] [--terms FILE]
        check_library.py LIBRARY --core CORE
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

import jsonschema
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = json.load(open(os.path.join(HERE, "..", "schemas", "library.schema.json"), encoding="utf-8"))
PATTERNS = json.load(open(os.path.join(HERE, "..", "schemas", "library-patterns.schema.json"), encoding="utf-8"))
sys.path.insert(0, HERE)
import check_extension  # noqa: E402
import check_model  # noqa: E402
from check_core import PHONE, Report  # noqa: E402
from check_extension import source_terms, term_rx, unbound  # noqa: E402

SPECS = {"library": ["layout", "release", "immutable", "index", "private", "licence", "where-used"],
         "library-patterns": ["form", "anchor", "known-uses", "ip", "relations", "lifecycle", "extract"]}
ROOT = {"library.yml", "index.yml", "patterns", "README.md", "CONTRIBUTING.md",
        "LICENSE", ".github", ".git", ".gitignore", ".gitattributes"}
SEMVER = re.compile(SCHEMA["$defs"]["semver"]["pattern"])
CALVER = re.compile(SCHEMA["$defs"]["extract"]["properties"]["version"]["pattern"])
INSTALLED = {"extension": "essentials", "extract": "patterns"}   # the one part a copy holds, and it is public (R3)
NEVER = ("knowledge", "workshop", "_authoring", "overlays")       # never in a release copy (EXTENSION R27, R29, R36)
ESSENTIALS = "commons-essentials"                                 # the one extension of the profile `specifications`
MAKER = {"carry-over"}   # read against the maker's estate at its own gate; a copy holds no superseded text
TESTS = "tools/tests/"   # the checks' own tests stay with the maker: their fixtures carry contact data by design
SECTIONS = ["Context", "Problem", "Solution", "Implementation", "Consequences", "Known Uses", "Cognitive Era", "Vitality"]
EMAIL = re.compile(r"(?<![\w.+/-])[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}(?![\w-])")   # never `<id>@<version>`
PLACEHOLDER = re.compile(r"\[TODO\]|TODO:|INSERT HERE|\[\.\.\.\]|lorem ipsum", re.I)
CREDENTIAL = re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[bp]-[A-Za-z0-9-]{10,})")
CURATED = ("requires", "complementary", "alternatives")
ACYCLIC = ("requires",)   # a dependency in a circle explains nothing; complementary and alternatives may be mutual
UNBUILT = ("that each record was generated from its source's `release` event, and that this event was authorised, is "
           "unverified: the release tool is not built, and a well-formed `event` with `gate.result: pass` is the "
           "maker's statement, not a proof (R3)")


def defs(name):
    if name == "pattern":
        return PATTERNS
    if name in PATTERNS["$defs"]:
        return {**PATTERNS["$defs"][name], "$defs": PATTERNS["$defs"]}
    return {**SCHEMA["$defs"][name], "$defs": SCHEMA["$defs"]}


def validate(r, check, sch, doc, where):
    for e in sorted(jsonschema.Draft202012Validator(sch).iter_errors(doc), key=lambda e: list(e.path)):
        r.fail(check, f"{where}: {'/'.join(str(p) for p in e.path) or 'root'}: {e.message}")


def yml(p):
    try:
        return yaml.safe_load(open(p, encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return None


def sha(b):
    return hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()


def day(v):
    """an ISO date `YYYY-MM-DD`, or None where it is none"""
    try:
        return datetime.date.fromisoformat(str(v)) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v)) else None
    except ValueError:
        return None


def git(d, *args):
    try:
        out = subprocess.run(["git", "-C", d, *args], capture_output=True)
        return out.stdout if out.returncode == 0 else None
    except OSError:
        return None


def files(d):
    return sorted(os.path.join(top, f) for top, _, fs in os.walk(d) for f in fs)


def rel(p, base):
    return os.path.relpath(p, base).replace(os.sep, "/")


def contained(p, d):
    """whether a path, every link and junction on it resolved, lies inside a copy (R2, R9)"""
    root, real = (os.path.normcase(os.path.realpath(x)) for x in (d, p))
    return real == root or real.startswith(root.rstrip(os.sep) + os.sep)


def inside(d, path):
    """whether a path a record or an index names is one inside the copy: relative, never climbing out, and contained
    once resolved (R2, R9)"""
    s = str(path or "")
    return bool(s) and not os.path.isabs(s) and not re.match(r"^[A-Za-z]:", s) \
        and ".." not in re.split(r"[\\/]", s) and contained(os.path.join(d, s), d)


def wordlist(path):
    if not path:
        return None
    return [w.strip() for w in open(path, encoding="utf-8") if w.strip() and not w.startswith("#")]


def rejected_words():
    p = os.path.join(HERE, "..", "glossary", "rejected.yml")
    doc = yml(p) or {}
    items = doc.get("rejected") or doc.get("terms") or (doc if isinstance(doc, list) else [])
    return [str(x.get("term") if isinstance(x, dict) else x) for x in items if x]


def front(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    if not t.startswith("---"):
        return None, t
    parts = t.split("---", 2)
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None, t
    return (fm if isinstance(fm, dict) else None), (parts[2] if len(parts) > 2 else "")


def sections(body):
    """the body's sections by name: `### Section <n>: <name>`"""
    out, cur = {}, None
    for line in body.splitlines():
        m = re.match(r"^###\s+Section\s+(\d+):\s*(.+?)\s*$", line)
        if m:
            cur = m[2]
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def known_uses(text):
    """the known uses: paragraphs that begin with their place in bold"""
    return [p.strip() for p in re.split(r"\n\s*\n", text) if re.match(r"^\*\*[^*]+\*\*", p.strip())]


def cycles(edges):
    """the cycles of a directed graph {node: [node]}, each once, from its smallest node"""
    found, state = set(), {}

    def walk(n, path):
        state[n] = 1
        path.append(n)
        for m in edges.get(n, []):
            if state.get(m) == 1:
                c = path[path.index(m):]
                i = c.index(min(c))
                found.add(tuple(c[i:] + c[:i]))
            elif m in edges and state.get(m) is None:
                walk(m, path)
        path.pop()
        state[n] = 2

    for n in sorted(edges):
        if n not in state:
            walk(n, [])
    return sorted(found)


def check_patterns(r, folder, base, names, terms):
    """the checks of library-patterns on every pattern file of a folder; returns {id: (front matter, path)}"""
    pats, slugs = {}, {}
    forms = set()
    for p in files(folder):
        if not p.endswith(".md") or os.path.basename(p) in ("README.md", "LICENSE.md"):
            continue
        w = f"`{rel(p, base)}`"
        fm, body = front(p)
        if fm is None:
            r.fail("form", f"{w}: no front matter (R1)")
            continue
        for e in jsonschema.Draft202012Validator(defs("pattern")).iter_errors(fm):
            r.fail("form", f"{w}: {'/'.join(str(x) for x in e.path) or 'root'}: {e.message} (R1, R2; library R10)")
        pid = fm.get("id")
        if pid in pats:
            r.fail("form", f"{w}: the id `{pid}` is taken by another pattern (R2)")
        pats[pid] = (fm, p)
        slugs[fm.get("slug")] = pid
        forms.add(str((fm.get("lifecycle") or {}).get("form") or fm.get("form") or "1"))
        sec = sections(body)
        for s in SECTIONS:
            text = sec.get(s)
            if text is None:
                r.fail("form", f"{w}: no section `{s}` (R5)")
            elif not text.strip("-* \n>"):
                r.fail("form", f"{w}: the section `{s}` is empty (R5)")
            elif PLACEHOLDER.search(text):
                r.fail("form", f"{w}: the section `{s}` holds a placeholder (R5)")
            elif not re.search(r"[.!?\"')*:”’]\s*$", text.strip().splitlines()[-1].rstrip("-").strip() or "."):
                r.fail("form", f"{w}: the section `{s}` ends mid-sentence (R5)")
        uses = known_uses(sec.get("Known Uses") or "")
        if len(uses) < 2:
            r.fail("known-uses", f"{w}: {len(uses)} known use, fewer than two (R6)")
        for u in uses:
            if EMAIL.search(u) or PHONE.search(u):
                r.fail("known-uses", f"{w}: a known use holds a contact datum (R6)")
        if names is None:
            r.gap("known-uses", f"{w}: no list of names given (--names); the known uses are unchecked for names (R6)")
        else:
            for n in names:
                rx = term_rx(n)
                if any(rx.search(u) for u in uses):
                    r.fail("known-uses", f"{w}: a known use names `{n}`, a person or organisation (R6)")
                elif any(rx.search(sec.get(s) or "") for s in SECTIONS if s != "Known Uses"):
                    r.fail("form", f"{w}: its sections name `{n}`, which only its provenance fields may name (library R10)")
        prose = "\n".join(sec.get(s) or "" for s in SECTIONS)
        for t in (terms or []) + rejected_words():
            if t and term_rx(t).search(prose):
                r.fail("ip", f"{w}: names `{t}` in its sections, which belongs only in its sources (R8)")
        st = (fm.get("lifecycle") or {}).get("status")
        if st not in ("candidate", "stable", "archived", "draft", "observed"):
            r.fail("lifecycle", f"{w}: the status `{st}` is none of R10's (R10)")
        if "graph_garden" in fm or any(k not in CURATED for k in (fm.get("relationships") or {})):
            r.fail("relations", f"{w}: holds a relation outside the curated kinds, or a garden block (R9)")
    if len(forms) > 1:
        r.fail("form", f"`{rel(folder, base)}`: its patterns follow {len(forms)} versions of the form (R1)")
    principles = {fm.get("slug") for fm, _ in pats.values() if fm.get("orbital_layer") == 1} | \
                 {pid for pid, (fm, _) in pats.items() if fm.get("orbital_layer") == 1}
    edges = {k: {} for k in ACYCLIC}
    for pid, (fm, p) in pats.items():
        w = f"`{rel(p, base)}`"
        if fm.get("orbital_layer") in (2, 3, 4):
            hubs = [h.get("hub_id") if isinstance(h, dict) else h for h in fm.get("gravitational_hubs") or []]
            if not hubs:
                r.fail("anchor", f"{w}: orbit {fm['orbital_layer']}, and no principle it rests on (R4)")
            elif principles and not any(h in principles for h in hubs):
                r.fail("anchor", f"{w}: none of its hubs is a principle of orbit 1 here (R4)")
            elif not principles:
                r.gap("anchor", f"{w}: no principle of orbit 1 in this release to resolve its hubs (R4)")
        rels = fm.get("relationships") or {}
        for k in CURATED:
            for t in rels.get(k) or []:
                ref = t.get("id") or t.get("slug") if isinstance(t, dict) else t
                if ref not in pats and ref not in slugs:
                    r.gap("relations", f"{w}: its `{k}` names `{ref}`, which is not in this release (R9)")
                elif k in ACYCLIC:
                    edges[k].setdefault(pid, []).append(ref if ref in pats else slugs[ref])
    for k in ACYCLIC:
        for c in cycles(edges[k]):
            r.fail("relations", f"`{k}` runs in a circle: {' → '.join(c + (c[0],))} (R9)")
    return pats


def check_extract(r, lid, pd, rec, w):
    """an extract's release: its index against its record and its patterns (library-patterns R17, R18)"""
    ix = os.path.join(pd, "index.jsonl")
    if not os.path.isfile(ix):
        r.fail("extract", f"{w}: no `index.jsonl` (R17)")
        return
    if rec.get("digest") != f"sha256:{sha(open(ix, 'rb').read())}":
        r.fail("extract", f"{w}: `index.jsonl` differs from the digest in its record (R17)")
    lines = [json.loads(x) for x in open(ix, encoding="utf-8") if x.strip()]
    head = lines[0] if lines else {}
    if head.get("kind") != "index":
        r.fail("extract", f"{w}: the index does not begin with its `kind: index` line (R17)")
    for k in ("graph_run", "extractor", "policy", "scope"):
        if head.get(k) != rec.get(k):
            r.fail("extract", f"{w}: the index gives the {k} `{head.get(k)}`, its record `{rec.get(k)}` (R17)")
    ids = {x.get("id") for x in lines[1:]}
    for x in lines[1:]:
        at = f"{w}, index line `{x.get('id')}`"
        for e in jsonschema.Draft202012Validator(defs("index_line")).iter_errors(x):
            r.fail("extract", f"{at}: {'/'.join(str(p) for p in e.path) or 'root'}: {e.message} (R17, R18)")
        if not str(x.get("id", "")).startswith(f"{lid}/"):
            r.fail("extract", f"{at}: not qualified by this library's id `{lid}` (R2)")
        if x.get("file") and not inside(pd, x["file"]):
            r.fail("extract", f"{at}: its file `{x.get('file')}` is no path inside the extract; the pin covers only the copy (R2, R17)")
            continue
        f = os.path.join(pd, str(x.get("file") or ""))
        fm, _ = front(f) if x.get("file") and os.path.isfile(f) else (None, "")
        if fm is None:
            r.fail("extract", f"{at}: its file `{x.get('file')}` is not in the extract (R17)")
            continue
        if f"{lid}/{fm.get('id')}" != x.get("id") or fm.get("orbital_layer") != x.get("orbit"):
            r.fail("extract", f"{at}: its file has another id or orbit (R17)")
        ratified = {f"vsf:{v.get('slug')}" for v in ((fm.get("value_model") or {}).get("vsf") or []) if isinstance(v, dict) and v.get("status") == "ratified"}
        for fam in (x.get("context") or {}).get("families") or []:
            if fam not in ratified:
                r.fail("extract", f"{at}: `{fam}` is no family the pattern is ratified for (R18; model R24)")
        for l in x.get("links") or []:
            if l.get("to") not in ids:
                r.fail("extract", f"{at}: the link to `{l.get('to')}` leads out of the extract (R17)")
    for p in files(pd):
        if p.endswith(".md") and rel(p, pd) not in {x.get("file") for x in lines[1:]}:
            r.fail("extract", f"{w}: `{rel(p, pd)}` is in the extract, but not in its index (R17)")


def recs_of(d):
    """the record ids an extension release offers, `<kind>:<slug>`"""
    out = set()
    for p in glob.glob(os.path.join(d, "registry", "*", "*.y*ml")):
        x = yml(p) or {}
        if isinstance(x, dict) and x.get("kind") and x.get("slug"):
            out.add(f"{x['kind']}:{x['slug']}")
    return out


def part_digest(d):
    """sha256 over every file of a copy but its record, path by path, whatever the line endings (R3)"""
    return digest_of((rel(p, d), lambda p=p: open(p, "rb").read()) for p in files(d))


def digest_of(held):
    """the part digest over `(path inside the copy, read)` pairs, wherever the copy is read from: its folder, or a
    revision of the CORE that installed it (R3; GRAPH and MCP read an installed extract only where it holds)"""
    h = hashlib.sha256()
    for rp, read in sorted(held, key=lambda x: x[0]):
        if rp != "release.yml":
            h.update(f"{rp}\0{sha(read())}\n".encode())
    return "sha256:" + h.hexdigest()


def offered(r, d, w, names):
    """an offer's copy, profile `offer`: EXTENSION's mandatory content, read from the copy alone (EXTENSION R4, R14,
    R25, R31; R10)"""
    off = yml(os.path.join(d, "offer.yml"))
    if off is None:
        r.fail("release", f"{w}: no `offer.yml` (EXTENSION R25)")
    else:
        check_extension.valid(r, "release", f"{w}/offer.yml", off, None)
    attr = yml(os.path.join(d, "sources.yml"))
    if attr is None:
        r.fail("release", f"{w}: no attribution list `sources.yml` (EXTENSION R31)")
    srcs = {s.get("id"): s for s in (attr or {}).get("sources") or [] if isinstance(s, dict)}
    reg = os.path.join(d, "registry")
    recs = check_extension.records(reg)
    if not any(k.startswith("value-stream:") and "/" not in k for k in recs):
        r.fail("release", f"{w}: offers no value stream in `registry/` (EXTENSION R4)")
    else:
        for o, c, t in check_model.check(check_model.load(reg), extension=True).items:
            if o == "fail":
                r.fail("release", f"{w}/registry: {c}: {t}")
    have = check_extension.loops(os.path.join(d, "loops"))
    for fam in sorted({rec.get("family") for k, (rec, _) in recs.items() if k.startswith("value-stream:") and "/" not in k} - {None}):
        if f"_family.{fam}" not in have:
            r.fail("release", f"{w}: offers streams of `{fam}` and no steering loop `loops/_family.{fam}.loop.yml` (EXTENSION R27)")
    for k, f, b in check_extension.binds_of(recs):
        if not isinstance(b, dict) or b.get("source") not in srcs:
            r.fail("release", f"{w}: `{k}` binds `{b}`, which the release does not attribute in `sources.yml` (EXTENSION R31)")
    tl = sorted({x for s in srcs.values() for x in source_terms(s)}, key=len, reverse=True)
    for p in files(d):
        rp = rel(p, d)
        if not rp.startswith(("registry/", "loops/")) or not p.endswith((".yml", ".yaml", ".md")):
            continue
        body = unbound(p, open(p, encoding="utf-8", errors="replace").read(), set(srcs))
        for t in tl:
            if term_rx(t).search(body):
                r.fail("release", f"{w}/{rp} names `{t}`, which belongs only in the attribution list (EXTENSION R14)")
        for n in names or []:
            if term_rx(n).search(body):
                r.fail("private", f"{w}/{rp} names `{n}` outside the attribution list (R10)")


def specified(r, d, w):
    """the copy of Commons Essentials, profile `specifications`: the discipline's `specs/` and nothing else (EXTENSION
    R16)"""
    import check_spec  # noqa: E402
    for x in sorted(os.listdir(d)):
        if x not in ("release.yml", "LICENSES", "specs"):
            r.fail("release", f"{w}: `{x}` in a release of the profile `specifications`, which holds only `specs/` (EXTENSION R16)")
    if os.path.isdir(os.path.join(d, "specs", *TESTS.split("/"))):
        r.fail("release", f"{w}: `specs/{TESTS}` in a release; the checks' own tests stay with the maker (R10, part 6)")
    own = sorted(glob.glob(os.path.join(d, "specs", "*.md")))
    if not own:
        r.fail("release", f"{w}: no specification in `specs/` (EXTENSION R16)")
    for p in own:
        for o, c, t in check_spec.check(p, offline=True).items:
            if o == "fail" and c not in MAKER and not (c == "references" and t.startswith(f"`{TESTS}")):
                r.fail("release", f"{w}/{rel(p, d)} does not follow SPECIFICATION: {c}: {t}")


def check_copy(r, d, base, w, names=None, terms=None, expect=None, lid=None):
    """one release copy, wherever it lies: in its library, alone, or installed (R3, R8, R9, R10, R11). Returns its
    record, or None where it has none."""
    rp = os.path.join(d, "release.yml")
    rec = yml(rp)
    if rec is None:
        r.fail("release", f"{w}: no `release.yml` (R3)")
        return None
    if expect and f"sha256:{sha(open(rp, 'rb').read())}" != expect:
        r.fail("release", f"{w}: its record is not the one its pin names, `{expect}` (R9)")
    kind = rec.get("kind")
    if kind not in INSTALLED:
        r.fail("release", f"{w}: its record names the kind `{kind}`, neither `extension` nor `extract` (R3)")
        return rec
    validate(r, "release", defs("release" if kind == "extension" else "extract"), rec, f"{w}, `release.yml`")
    for top, dirs, fs in os.walk(d):                 # containment (R2, R9): nothing of a copy leads outside it
        for n in list(dirs) + fs:
            p = os.path.join(top, n)
            if not contained(p, d):
                r.fail("release", f"`{rel(p, base)}` leads outside the copy, through a link or a junction; a release is a copy of its own (R2, R9)")
                if n in dirs:
                    dirs.remove(n)
    if lid and rec.get("library") != lid:
        r.fail("release", f"{w}: its record names the library `{rec.get('library')}`, not `{lid}` (R3)")
    if (rec.get("gate") or {}).get("result") != "pass":
        r.fail("release", f"{w}: its gate did not pass (R3, R8)")
    for x in rec.get("retires") or []:
        if isinstance(x, dict) and day(x.get("from")) is None:
            r.fail("release", f"{w}: retires `{x.get('id')}` from `{x.get('from')}`, which is no date YYYY-MM-DD (R5)")
    # parts (R3, R15): the copy holds its one public part, and its digest is that part's
    parts = rec.get("parts") if isinstance(rec.get("parts"), dict) else {}
    main = INSTALLED[kind]
    held = parts.get(main) if isinstance(parts.get(main), dict) else {}
    if held.get("class") != "public":
        r.fail("release", f"{w}: its part `{main}` has the class `{held.get('class')}`; the installed part is `public` (R3; EXTENSION R27)")
    if held.get("digest") != part_digest(d):
        r.fail("release", f"{w}: its files are not those its record's `parts.{main}.digest` names (R3, R9)")
    for name, p in parts.items():
        if name == main:
            continue
        if isinstance(p, dict) and p.get("class") == "public":
            r.fail("release", f"{w}: its part `{name}` is `public` beside `{main}`; a release has one installed part (R3)")
        if os.path.exists(os.path.join(d, name)):
            r.fail("private", f"{w}: its served part `{name}/` lies in the copy; it is held only where it is served (R15)")
    for x in NEVER:
        if os.path.exists(os.path.join(d, x)):
            r.fail("private", f"{w}: holds `{x}/`, which no release carries (R12)")
    # licence (R11): the text of a licence by reference travels with the copy
    lic = str(rec.get("licence") or "")
    if not lic:
        r.fail("licence", f"{w}: names no licence (R11)")
    elif lic.startswith("LicenseRef-") and not (inside(d, f"LICENSES/{lic}.txt") and os.path.isfile(os.path.join(d, "LICENSES", f"{lic}.txt"))):
        r.fail("licence", f"{w}: names `{lic}`, whose text is not in its `LICENSES/` (R11)")
    # private (R10)
    for p in files(d):
        t = open(p, encoding="utf-8", errors="replace").read()
        if EMAIL.search(t) or PHONE.search(t) or CREDENTIAL.search(t):
            r.fail("private", f"`{rel(p, base)}` holds a contact datum or a credential (R10)")
    # the profile's mandatory content
    if kind == "extension":
        profile = rec.get("profile", "offer")
        if profile == "specifications":
            if rec.get("extension") != ESSENTIALS:
                r.fail("release", f"{w}: the profile `specifications` is Commons Essentials' alone, not `{rec.get('extension')}`'s (EXTENSION R16)")
            specified(r, d, w)
        else:
            offered(r, d, w, names)
    else:
        check_patterns(r, d, base, names, terms)
        check_extract(r, rec.get("library"), d, rec, w)
    return rec


def check_release(folder, names=None, terms=None, expect=None):
    """one release copy where it lies, as a commons checks it at install (R9)"""
    r = Report()
    rec = check_copy(r, folder, folder, f"`{folder}`", names, terms, expect)
    if rec is not None and not expect:
        r.gap("release", "no record digest from a pin given (--expect): the copy agrees with itself, and whether it is the release its library holds is unverified (R9)")
    if names is None:
        r.gap("private", "no list of names given (--names); the release is unchecked for names (R10)")
    r.gap("release", UNBUILT)
    return r


def state_of(rid, version, records, today):
    """the state a version is in on a day, from the records; None where a retirement's date is no date"""
    if "-rc." in version:
        return "candidate"
    for rec in records:
        for x in rec.get("retires") or []:
            if isinstance(x, dict) and x.get("id") == f"{rid}@{version}":
                f = day(x.get("from"))
                return None if f is None else ("retired" if f <= today else "released")
    return "released"


def check(lib, names=None, terms=None, today=None):
    r = Report()
    today = today or datetime.date.today()
    cfg = yml(os.path.join(lib, "library.yml"))
    if cfg is None:
        r.fail("layout", "no `library.yml` (R1)")
        return r
    validate(r, "layout", SCHEMA, cfg, "`library.yml`")
    lid = cfg.get("id")
    withheld = {str(x.get("release")): x for x in cfg.get("withheld") or [] if isinstance(x, dict)}
    for x in withheld.values():
        if day(x.get("from")) is None:
            r.fail("layout", f"`library.yml` withholds `{x.get('release')}` from `{x.get('from')}`, which is no date YYYY-MM-DD (R5)")
    folders = []                                     # (id, kind, version, folder)
    for x in sorted(os.listdir(lib)):
        p = os.path.join(lib, x)
        if x in ROOT:
            continue
        if not os.path.isdir(p) or not re.match(SCHEMA["$defs"]["id"]["pattern"], x):
            r.fail("layout", f"`{x}` is no entry of a library's root (R1, R2)")
            continue
        for v in sorted(os.listdir(p)):
            if not SEMVER.match(v) or not os.path.isdir(os.path.join(p, v)):
                r.fail("layout", f"`{x}/{v}` is no release folder `<id>/<version>/` (R2)")
            else:
                folders.append((x, "extension", v, os.path.join(p, v)))
    for v in sorted(os.listdir(os.path.join(lib, "patterns"))) if os.path.isdir(os.path.join(lib, "patterns")) else []:
        if not CALVER.match(v):
            r.fail("layout", f"`patterns/{v}` is no extract folder `patterns/<version>/` (R2)")
        else:
            folders.append(("patterns", "extract", v, os.path.join(lib, "patterns", v)))
    releases = []                                    # (id, kind, version, folder, record)
    for rid, kind, v, d in folders:
        w = f"`{rel(d, lib)}`"
        key = f"{rid}@{v}"
        if key in withheld:
            # withheld (R5): its record stays for the lineage, its files leave the library
            rec = yml(os.path.join(d, "release.yml"))
            if rec is None:
                r.fail("release", f"{w}: withheld, and its record `release.yml` is gone; the record stays (R5)")
                continue
            validate(r, "release", defs("release" if kind == "extension" else "extract"), rec, f"{w}, `release.yml`")
            if [p for p in files(d) if rel(p, d) != "release.yml"]:
                r.fail("release", f"{w}: withheld ({withheld[key].get('reason')}), and its files are still distributed (R5)")
        else:
            rec = check_copy(r, d, lib, w, names, terms, lid=lid)
            if rec is None:
                continue
        if rec.get("kind") != kind:
            r.fail("release", f"{w}: its record names the kind `{rec.get('kind')}` (R2, R3)")
        if kind == "extension" and rec.get("extension") != rid:
            r.fail("release", f"{w}: its record names the extension `{rec.get('extension')}` (R3)")
        if rec.get("version") != v:
            r.fail("release", f"{w}: its record names the version `{rec.get('version')}` (R3)")
        releases.append((rid, kind, v, d, rec))
    held = {(rid, v): d for rid, _, v, d, _ in releases}
    for key in sorted(withheld):
        rid, _, v = key.rpartition("@")
        if (rid, v) not in held:
            r.fail("release", f"`library.yml` withholds `{key}`, which this library does not hold (R5)")
    order = lambda v: tuple(int(x) for x in re.findall(r"\d+", v.split("-rc.")[0])) + ((0,) if "-rc." in v else (1,))
    for rid, kind, v, d, rec in releases:
        for x in rec.get("retires") or []:
            what = str(x.get("id") or "") if isinstance(x, dict) else ""
            if "@" in what:
                tid, _, tv = what.partition("@")
                if (tid, tv) not in held:
                    r.fail("release", f"`{rel(d, lib)}` retires `{what}`, which this library does not hold (R5)")
                elif tid == rid and order(tv) >= order(v):
                    r.fail("release", f"`{rel(d, lib)}` retires `{what}`, which is not an earlier version (R5)")
            else:
                earlier = [dd for (i, vv), dd in held.items() if i == rid and order(vv) < order(v)]
                if not any(what in recs_of(dd) for dd in earlier):
                    r.fail("release", f"`{rel(d, lib)}` retires `{what}`, which no earlier version of `{rid}` offered (R5)")
    if names is None:
        r.gap("private", "no list of names given (--names); the releases are unchecked for names (R10)")
    r.gap("release", UNBUILT)
    # index (R6, R7): generated from the records and from what `library.yml` withholds
    records = [rec for *_, rec in releases]
    want = []
    for rid, kind, v, d, rec in releases:
        rp = os.path.join(d, "release.yml")
        e = {"id": rid, "kind": kind, "version": v, "record": rel(rp, lib),
             "digest": f"sha256:{sha(open(rp, 'rb').read())}", "state": state_of(rid, v, records, today)}
        if f"{rid}@{v}" in withheld:
            e["withheld"] = {"from": str(withheld[f"{rid}@{v}"].get("from")), "reason": withheld[f"{rid}@{v}"].get("reason")}
        want.append(e)
    ix = yml(os.path.join(lib, "index.yml"))
    if ix is None:
        r.fail("index", "no `index.yml` (R6)")
    else:
        validate(r, "index", defs("index"), ix, "`index.yml`")
        have = ix.get("releases") or []
        key = lambda e: (e.get("id"), e.get("kind"), e.get("version"))
        hk, wk = {key(e): e for e in have}, {key(e): e for e in want}
        for k in sorted(set(wk) - set(hk), key=str):
            r.fail("index", f"the release `{k[0]}@{k[2]}` is not in `index.yml` (R6)")
        for k in sorted(set(hk) - set(wk), key=str):
            r.fail("index", f"`index.yml` lists `{k[0]}@{k[2]}`, which the library does not hold (R6)")
        for k in set(hk) & set(wk):
            for f in ("record", "digest", "state", "withheld"):
                if wk[k].get(f) is None and f == "state":
                    continue                     # no state where a retirement has no date; `release` fails it
                if hk[k].get(f) != wk[k].get(f):
                    r.fail("index", f"`index.yml` gives `{k[0]}@{k[2]}` the {f} `{hk[k].get(f)}`, its record `{wk[k].get(f)}` (R6, R7)")
    # immutable (R4, R5): in git, every released file is the one first released, and none has left but a withheld
    # release's files
    if git(lib, "rev-parse") is None:
        r.gap("immutable", "the library is not in git; that its releases never changed is unverified (R4, R5)")
    else:
        pre = (git(lib, "rev-parse", "--show-prefix") or b"").decode().strip()
        for rid, kind, v, d, _ in releases:
            rp = rel(d, lib)
            first = (git(lib, "log", "--reverse", "--format=%H", "--", f"{rp}/release.yml") or b"").decode().split()
            if not first:
                continue
            listing = (git(lib, "ls-tree", "-r", "--full-name", "--name-only", first[0], "--", rp) or b"").decode().split()
            now = {rel(p, lib) for p in files(d)}
            was = {x[len(pre):] for x in listing}
            for x in sorted(was | now):
                if x not in now and f"{rid}@{v}" in withheld:
                    continue
                blob = git(lib, "show", f"{first[0]}:{pre}{x}") if x in was else None
                cur = os.path.join(lib, x)
                if x not in now or blob is None or sha(blob) != sha(open(cur, "rb").read()):
                    r.fail("immutable", f"`{x}` is not as `{rid}@{v}` was first released (R4)")
        gone = (git(lib, "log", "--diff-filter=D", "--name-only", "--format=", "--", ".") or b"").decode().split()
        for x in sorted({g for g in gone if g.endswith("/release.yml")}):
            if not os.path.isfile(os.path.join(lib, x[len(pre):])):
                r.fail("immutable", f"`{x[len(pre):]}` was released and has left the library (R5)")
    return r


def withheld_in(lib, bill):
    """the lines of a commons' bill whose release this library withholds, each with the release and its withholding
    (R18): computed by the commons from the library's `library.yml` and index, as it reads them; the library computes none"""
    lid = (yml(os.path.join(lib, "library.yml")) or {}).get("id")
    ix = yml(os.path.join(lib, "index.yml")) or {}
    held = {f"{lid}/{x.get('id')}@{x.get('version')}": x["withheld"] for x in ix.get("releases") or []
            if isinstance(x, dict) and isinstance(x.get("withheld"), dict)}
    return [(x, x["part"].split("#", 1)[0], held[x["part"].split("#", 1)[0]]) for x in (bill or {}).get("lines") or []
            if x["part"].split("#", 1)[0] in held]


def where_used(r, lib, core):
    """where-used on withholding (R18): each line of the CORE's bill that a release this library withholds touches"""
    import check_core   # here, not above: the bill is CORE's
    rep = check_core.check(core, offline=True)
    failed = [t for o, _, t in rep.items if o == "fail"]
    if not getattr(rep, "bill", None):
        r.gap("where-used", f"`{core}` has no bill: a finding on what it lists withholds it (core R37); "
                            f"{len(failed)} fail" + (f", first: {failed[0]}" if failed else ""))
        # repair diagnostics: the pins its lock declares, unverified, never a bill and never certified (the EA, commons.o#107)
        lp = os.path.join(core, ".commons", "lock.yml")
        lock = (yml(lp) or {}) if os.path.isfile(lp) else {}
        pins = [str(x.get("id")) + "@" + str(x.get("version")) for x in lock.get("extensions") or [] if isinstance(x, dict)]
        for x in lock.get("patterns") or []:
            rec = yml(os.path.join(core, "patterns", str((x or {}).get("path")), "release.yml")) if isinstance(x, dict) else None
            if rec:
                pins.append(f"{rec.get('library')}/patterns@{rec.get('version')}")
        for x, rel, w in withheld_in(lib, {"lines": [{"part": p, "usage": "declared"} for p in pins]}):
            r.should("where-used", f"`{rel}` is a pin the lock declares, unverified since the CORE has no bill, and is "
                                   f"withheld from {w.get('from')} for {w.get('reason')}; repair the CORE before relying on it (R18, R5)")
        return r
    for x, rel, w in withheld_in(lib, rep.bill):
        r.should("where-used", f"`{x['part']}` ({x['usage']}) belongs to `{rel}`, withheld from {w.get('from')} for "
                               f"{w.get('reason')}; the commons keeps its copy and decides what follows (R18, R5)")
    return r


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("library", nargs="?")
    ap.add_argument("--patterns", help="check a folder of pattern files, as a pattern source does before it releases")
    ap.add_argument("--release", help="check one release copy, as a commons does at install")
    ap.add_argument("--expect", help="with --release: the record digest the pin gives, from the library's index")
    ap.add_argument("--names", help="a file of names of persons and organisations, one per line, kept outside git")
    ap.add_argument("--terms", help="a file of third-party codes and trademarks, one per line")
    ap.add_argument("--today", help="the date states are derived for, YYYY-MM-DD; today when omitted")
    ap.add_argument("--core", help="with a library: the lines of this CORE's bill that a withholding touches (R18)")
    ap.add_argument("--spec", choices=sorted(SPECS))
    a = ap.parse_args()
    names, terms = wordlist(a.names), wordlist(a.terms)
    if a.today and day(a.today) is None:
        ap.error(f"--today {a.today} is no date YYYY-MM-DD")
    if a.release:
        r = check_release(a.release, names, terms, a.expect)
        target = a.release
    elif a.patterns:
        r = Report()
        check_patterns(r, a.patterns, a.patterns, names, terms)
        target = a.patterns
    elif a.core:
        r = where_used(Report(), a.library, a.core)
        target = f"{a.core} against {a.library}"
    else:
        r = check(a.library, names, terms, day(a.today) if a.today else None)
        target = a.library
    items = [i for i in r.items if not a.spec or i[1] in SPECS[a.spec]]
    n = {o: sum(1 for i in items if i[0] == o) for o in ("fail", "should", "gap")}
    print(f"# {target}{' · ' + a.spec if a.spec else ''}: {n['fail']} fail · {n['should']} should · {n['gap']} gap")
    for o, c, t in items:
        print(f"{o}: {c}: {t}")
    return 1 if n["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
