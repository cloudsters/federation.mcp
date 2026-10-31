#!/usr/bin/env python3
"""check_extension.py — a [domain].core offers well, and a commons installs and adopts as it should (extension.md).
Read-only.

Reports each finding as fail (a MUST), should (a SHOULD) or gap (missing, not wrong), and exits with 1 only on a
fail. The check ids are those of extension.md, part 6:

  core  offer  contents  start  ip  private  specs  research  binds  release  install  adopt  fit

Usage:  check_extension.py DOMAIN_CORE [DOMAIN_CORE ...] [--core CORE]
        A [domain].core is read with check_core.py first, then its offer in `offer/` and its research in
        `knowledge/`. The same code is the gate of a library (R32): what passes here passes there. --core reads a
        commons that installs a released extension: its pins and libraries, the installed copy under
        `extensions/<library>/<extension>/` with its release record, what it adopted (`adopted_from`) and what it
        did not select (`not-selected` events). Each adopted record is reported as unchanged or adapted, with the
        fields it changes: derived, never stated.
"""
import argparse
import glob
import json
import os
import re
import sys

import jsonschema
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_core  # noqa: E402
import check_model  # noqa: E402

SCHEMA = json.load(open(os.path.join(HERE, "..", "schemas", "extension.schema.json"), encoding="utf-8"))
MODEL_SCHEMA = os.path.join(HERE, "..", "schemas", "model.schema.json")
EARLIER = "commons-library"    # once built in; a commons now names every library it installs from (R12, CORE R1)
BUILDERS = "<library>/extension-builders"
EMAIL = re.compile(r"(?<![\w.+/-])[\w.+-]+@[\w-]+\.[\w.-]+")   # never the <library>/<extension>@<version> of an origin
PHONE = re.compile(r"\+\d[\d ()-]{7,}\d")
ORIGIN = re.compile(r"^(?P<library>[a-z0-9-]+)/(?P<ext>[a-z0-9-]+)@(?P<version>\d+\.\d+\.\d+(-rc\.\d+)?)#(?P<kind>[a-z-]+):(?P<slug>[a-z0-9.-]+(/[a-z0-9.-]+)?)$")
OLD_FORMAT = ["manifest.yml", "MANIFEST.md", "value-model.yml", "entity-model.yml", "element-model.yml",
              "blueprint.template.md", "capability-map.deep.yml"]
RELATIONS = {"derived-from", "adopt", "bind", "mirror", "own"}
RESEARCH = ["edition", "jurisdiction", "area", "relation", "verified", "licence", "class", "informs"]
TEXT = (".yml", ".yaml", ".md", ".json")


class Report(check_core.Report):
    def __init__(self):
        super().__init__()
        self.notes = []


def yml(p):
    return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def valid(r, check, name, data, ref):
    v = jsonschema.Draft202012Validator({"$defs": SCHEMA["$defs"], "$ref": ref} if ref else SCHEMA)
    for e in v.iter_errors(data):
        r.fail(check, f"`{name}`: {'/'.join(map(str, e.absolute_path)) or 'the file'}: {e.message[:110]}")


def records(reg):
    """the records of a registry folder, by `<kind>:<slug>`, steps as `value-stream:<stream>/<step>`"""
    out = {}
    for f in sorted(glob.glob(os.path.join(reg, "*", "*.y*ml"))):
        rec = yml(f) or {}
        if isinstance(rec, dict) and rec.get("kind") and rec.get("slug"):
            out[f"{rec['kind']}:{rec['slug']}"] = (rec, f)
            for st in rec.get("steps") or []:
                if isinstance(st, dict) and st.get("slug"):
                    out[f"value-stream:{rec['slug']}/{st['slug']}"] = (st, f)
    return out


def loops(d):
    return {os.path.basename(f).rsplit(".loop.", 1)[0] for f in glob.glob(os.path.join(d, "*.loop.y*ml"))}


def texts(d, skip=()):
    for p in glob.glob(os.path.join(d, "**", "*"), recursive=True, include_hidden=True):
        if os.path.isfile(p) and p.endswith(TEXT) and os.path.relpath(p, d).split(os.sep)[0] not in skip:
            yield p, open(p, encoding="utf-8", errors="replace").read()


def commons_spec_ids():
    """the ids of the discipline's specifications: those beside this tool"""
    ids = set()
    for f in glob.glob(os.path.join(HERE, "..", "*.md")):
        t = open(f, encoding="utf-8").read()
        if t.startswith("---"):
            ids.add((yaml.safe_load(t.split("---")[1]) or {}).get("id"))
    return ids - {None}


def binds_of(recs):
    for k, (rec, f) in recs.items():
        if isinstance(rec, dict) and "/" not in k:
            for b in rec.get("binds") or []:
                yield k, f, b


def source_terms(s):
    """the words a source is known by: its designation and slug, the designation's leading part (`KHVVG` of `KHVVG,
    BGBl. 2024 I Nr. 400`), a short title in parentheses (`Artificial Intelligence Act`), and any `terms` it lists"""
    out = {s.get("designation"), s.get("slug"), *(s.get("terms") or [])}
    if s.get("designation"):
        out.add(str(s["designation"]).split(",")[0].strip())
    for m in re.findall(r"\(([^()]+)\)", str(s.get("title") or "")):
        if len(m) >= 4 and not re.search(r"\d", m):
            out.add(m.strip())
    return {str(x) for x in out if x and len(str(x)) >= 3}


def term_rx(term):
    """a term with capitals is matched as written, one in lower case in any case (as the workshop's IP check does)"""
    return re.compile(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", 0 if term != term.lower() else re.I)


def unbound(path, text, ids):
    """the text of a file without the source ids its bindings name: `binds[].source`, in a record or an overlay"""
    if not path.endswith((".yml", ".yaml")):
        return text
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        return text
    out = []

    def walk(x, in_binds=False):
        if isinstance(x, dict):
            for k, v in x.items():
                if in_binds and k == "source" and v in ids:
                    continue
                out.append(str(k))
                walk(v, k == "binds")
        elif isinstance(x, list):
            for v in x:
                walk(v, in_binds)
        elif x is not None:
            out.append(str(x))
    walk(data)
    return chr(10).join(out)


def jurisdictional(j):
    """a source of law of one jurisdiction, national or regional (`de`, `se`, `eu`); only `global`, the standards no
    jurisdiction enacts, is jurisdiction-neutral (R36)"""
    return isinstance(j, str) and j.strip() != "" and j != "global"


def jurisdiction_binds(d):
    """(record, binding, file) of every binding in `knowledge/jurisdictions/<j>.yml`: research, never offer (R36)"""
    for p in sorted(glob.glob(os.path.join(d, "knowledge", "jurisdictions", "*.y*ml"))):
        data = yml(p) or {}
        for bd in data.get("bindings") or [] if isinstance(data, dict) else []:
            for b in (bd.get("binds") or []) if isinstance(bd, dict) else []:
                if isinstance(b, dict):
                    yield bd.get("record"), b, p


def check(d, r=None):
    """a [domain].core: a CORE first, then its offer (R4, R29) and its research (R30, R31)"""
    r = r or Report()
    name = os.path.basename(os.path.abspath(d))
    cfg = yml(os.path.join(d, ".commons", "commons.yml"))
    off = os.path.join(d, "offer")

    # core (R7, R29): a well-formed CORE, and an offer in MODEL's grammar on MODEL's families
    earlier = yml(os.path.join(d, ".commons", "identity.yml"))
    if cfg is None and earlier is not None:
        r.gap("core", f"`{name}` is on an earlier layout (`.commons/identity.yml`): read as unmigrated, the CORE checks wait for its migration (CORE R4)")
        cfg = {"holder": earlier.get("founder"), "extensions": [], "unmigrated": True}
    else:
        for o, c, t in check_core.check(d, offline=True).items:
            if o == "fail":
                r.fail("core", f"`{name}`: {c}: {t}")
    if cfg is None:
        r.fail("offer", f"`{name}` has no `.commons/commons.yml`")
        return r
    if not os.path.isdir(off):
        r.fail("offer", f"`{name}` holds no `offer/`: what a [domain].core offers is kept apart from its own model")
        return r
    if os.path.isdir(os.path.join(off, "registry")):
        rep = check_model.check(check_model.load(os.path.join(off, "registry")), extension=True)
        for o, c, t in rep.items:
            if o == "fail":
                r.fail("core", f"`{name}/offer/registry`: {c}: {t}")

    # offer (R1, R25, R29): the offer as data, the licence, the holder, Extension-Builders as primary
    offer = yml(os.path.join(off, "offer.yml"))
    if offer is None:
        r.fail("offer", f"`{name}` has no `offer/offer.yml`")
    else:
        valid(r, "offer", f"{name}/offer/offer.yml", offer, None)
    if not os.path.exists(os.path.join(d, "LICENSE")):
        r.fail("offer", f"`{name}` has no `LICENSE`")
    if not cfg.get("holder"):
        r.fail("offer", f"`{name}` names no `holder`: a [domain].core is maintained by someone")
    prim = [x.get("id") for x in cfg.get("extensions") or [] if isinstance(x, dict) and x.get("primary")]
    if cfg.get("unmigrated"):
        pass
    elif not (len(prim) == 1 and str(prim[0]).endswith("/extension-builders")):
        r.should("offer", f"`{name}` holds {prim or 'no'} primary: a [domain].core installs Extension-Builders (`{BUILDERS}`, or a candidate of it) as its primary")

    # contents (R4, R8, R12): one menu in offer/, nothing of the earlier format
    for f in OLD_FORMAT:
        for where in (d, off):
            if os.path.exists(os.path.join(where, f)):
                r.fail("contents", f"`{os.path.relpath(os.path.join(where, f), os.path.dirname(d))}`: an offer has no format of its own")
    recs = records(os.path.join(off, "registry"))
    if not any(k.startswith("value-stream:") and "/" not in k for k in recs):
        r.fail("contents", f"`{name}` offers no value stream in `offer/registry/`")
    canon = json.load(open(MODEL_SCHEMA, encoding="utf-8"))["x-dimension-of"]
    have = loops(os.path.join(off, "loops"))
    named = {rec.get("family") for k, (rec, _) in recs.items() if k.startswith("value-stream:") and "/" not in k}
    for fam in canon:
        if f"_family.{fam}" in have:
            continue
        if fam in named:
            r.fail("contents", f"`{name}` offers streams of `{fam}` and no steering loop `offer/loops/_family.{fam}.loop.yml`")
        else:
            r.gap("contents", f"`{name}` does not reach the family `{fam}`: no stream, no steering loop")
    if os.path.exists(os.path.join(off, "overlays")):
        r.fail("contents", f"`{name}` holds `offer/overlays/`: an extension is jurisdiction-neutral, national law stays in `knowledge/` (R36)")
    enh = os.path.join(off, "enhanced")
    for p, _ in texts(enh):
        data = yml(p) if p.endswith((".yml", ".yaml")) else None
        for rec in (data or {}).get("records") or [] if isinstance(data, dict) else []:
            if not (isinstance(rec, dict) and rec.get("id")):
                r.fail("contents", f"`{os.path.relpath(p, d)}` holds a record without a stable `id` (R4)")

    # start (R24)
    start = {k: v for k, v in recs.items() if isinstance(v[0], dict) and v[0].get("start") is True}
    if not start:
        r.should("start", f"`{name}` marks no starting set (`start: true`)")
    for k, (rec, _) in start.items():
        for st in rec.get("steps") or []:
            for cap in st.get("capabilities") or []:
                if f"capability:{cap}" not in recs:
                    r.fail("start", f"`{name}`: the starting record `{k}` binds the capability `{cap}`, which it does not offer")

    # research (R30): every source says where it stands and what it informs
    src = yml(os.path.join(d, "knowledge", "sources.yml"))
    sources = {s.get("id"): s for s in (src or {}).get("sources") or [] if isinstance(s, dict)}
    if src is None:
        r.gap("research", f"`{name}` holds no `knowledge/sources.yml`: its research is not at hand")
    for sid, s in sources.items():
        own = s.get("relation") == "own"           # the commons' own synthesis: a design with its derivation, no lenses
        need = [x for x in RESEARCH if not (own and x == "verified")] + (["derivation"] if own else [])
        miss = [x for x in need if not s.get(x)]
        if miss:
            r.fail("research", f"`{name}`: the source `{sid}` lacks {miss}")
        if s.get("relation") and s["relation"] not in RELATIONS:
            r.fail("research", f"`{name}`: the source `{sid}` has the relation `{s['relation']}`, not one of {sorted(RELATIONS)}")
        if own and s.get("standing") != "design":
            r.fail("research", f"`{name}`: the source `{sid}` is the commons' own and states no `standing: design`")
        v = s.get("verified") or {}
        if not own and s.get("verified") and not (isinstance(v, dict) and v.get("confirmation") and v.get("refutation")):
            r.fail("research", f"`{name}`: the source `{sid}` is not verified under both lenses, confirmation and refutation")
        for i in s.get("informs") or []:
            if i not in recs:
                r.fail("research", f"`{name}`: the source `{sid}` informs `{i}`, which the offer does not hold")

    # binds (R31): every binding names a source of the research, with its edition and jurisdiction, and, optionally,
    # the part of the source it rests on; never an edition that is only scheduled
    for k, f, b in binds_of(recs):
        s = sources.get(b.get("source")) if isinstance(b, dict) else None
        where = os.path.relpath(f, d)
        if isinstance(b, dict) and "part" in b and not (isinstance(b["part"], str) and b["part"].strip()):
            r.fail("binds", f"`{where}`: a binding's `part` names no part of `{b.get('source')}`")
        if s is None:
            r.fail("binds", f"`{where}` binds `{b}`, which is no source in `knowledge/sources.yml`")
        elif jurisdictional(s.get("jurisdiction")):
            r.fail("binds", f"`{where}` binds `{b.get('source')}` of the jurisdiction `{s.get('jurisdiction')}`: an extension is jurisdiction-neutral, the law of a jurisdiction stays in `knowledge/jurisdictions/` (R36)")
        elif str(b.get("edition")) in {str(e.get("edition")) for e in s.get("scheduled") or [] if isinstance(e, dict)}:
            r.fail("binds", f"`{where}` binds `{b.get('source')}` at `{b.get('edition')}`, an edition not yet in force (SPECIFICATION R28)")
        elif str(b.get("edition")) != str(s.get("edition")) or b.get("jurisdiction") != s.get("jurisdiction"):
            r.fail("binds", f"`{where}` binds `{b.get('source')}` at {b.get('edition')}/{b.get('jurisdiction')}, and the source is {s.get('edition')}/{s.get('jurisdiction')}")

    # research (R30): coverage. Every offered record is grounded by a source it binds or that informs it, or a claim
    # about it, since what no standard reaches is held as claims; one grounded by none of them
    # is a gap, counted per kind
    if src is not None:
        # a source of the relation `own` is the [domain].core's own word: it grounds a record only through a claim about it
        grounded = {i for s in sources.values() if s.get("relation") != "own" for i in s.get("informs") or []} | {k for k, _, _ in binds_of(recs)}
        grounded |= {k for k, _, _ in jurisdiction_binds(d)}
        slugs = {}
        for k in recs:
            slugs.setdefault(k.split(":", 1)[-1], []).append(k)
        for c in (yml(os.path.join(d, "knowledge", "claims.yml")) or {}).get("claims") or []:
            for a in (c.get("about") or []) if isinstance(c, dict) else []:
                grounded |= {a} if ":" in str(a) else set(slugs.get(str(a), []))
        open_ = {}
        for k in recs:
            if "/" not in k and k not in grounded:
                open_.setdefault(k.split(":", 1)[0], []).append(k)
        for kind, ks in sorted(open_.items()):
            total = sum(1 for k in recs if "/" not in k and k.startswith(kind + ":"))
            r.gap("research", f"`{name}`: {len(ks)} of {total} offered {kind} records are grounded by neither a source nor a claim: "
                              f"{', '.join(sorted(ks)[:5])}{', …' if len(ks) > 5 else ''} (R30)")

    # jurisdictions (R36): the law of one jurisdiction binds offered records only in the research, one file per
    # jurisdiction, at the edition in force
    for p in sorted(glob.glob(os.path.join(d, "knowledge", "jurisdictions", "*.y*ml"))):
        data, where = yml(p) or {}, os.path.relpath(p, d)
        j = os.path.basename(p).rsplit(".", 1)[0]
        if not isinstance(data, dict) or data.get("jurisdiction") != j or not isinstance(data.get("bindings"), list):
            r.fail("research", f"`{where}` is no `{{jurisdiction: {j}, bindings: [...]}}`")
            continue
    for k, b, p in jurisdiction_binds(d):
        where, j = os.path.relpath(p, d), os.path.basename(p).rsplit(".", 1)[0]
        s = sources.get(b.get("source"))
        if k not in recs:
            r.fail("research", f"`{where}` binds `{k}`, which the offer does not hold")
        if s is None:
            r.fail("research", f"`{where}`: `{b.get('source')}` is no source of `knowledge/sources.yml`")
        elif s.get("jurisdiction") != j:
            r.fail("research", f"`{where}`: `{b.get('source')}` is of `{s.get('jurisdiction')}`, not `{j}`")
        elif str(b.get("edition")) != str(s.get("edition")):
            r.fail("research", f"`{where}`: `{b.get('source')}` is bound at `{b.get('edition')}`, and the edition in force is `{s.get('edition')}`")
        if b.get("relation") and b["relation"] not in RELATIONS:
            r.fail("research", f"`{where}`: the relation `{b['relation']}` is not one of {sorted(RELATIONS)}")
        if "part" in b and not (isinstance(b["part"], str) and b["part"].strip()):
            r.fail("research", f"`{where}`: a binding's `part` names no part of `{b.get('source')}`")

    # scheduled (R30): an edition enacted and not yet in force has its place, so that the currency loop raises it before
    # its date; the check reads the form, not the date of reading. With `affects`, it reaches only the bindings that
    # name an affected part, and every binding of the source that names no part
    every = [(k, b) for k, _, b in binds_of(recs) if isinstance(b, dict)] + [(k, b) for k, b, _ in jurisdiction_binds(d)]
    bound_to = {(k, b.get("source")) for k, b in every}
    every += [(i, {"source": sid}) for sid, s in sources.items() for i in s.get("informs") or []
              if (i, sid) not in bound_to]                               # informed and not bound: no part known
    for sid, s in sources.items():
        sch = s.get("scheduled")
        if sch is None:
            continue
        if not isinstance(sch, list):
            r.fail("research", f"`{name}`: the source `{sid}` lists `scheduled` as no list")
            continue
        editions = {str(s.get("edition"))}
        for e in sch:
            e = e if isinstance(e, dict) else {}
            ed, date, aff = str(e.get("edition") or ""), str(e.get("in_force") or ""), e.get("affects")
            if not ed or ed in editions:
                r.fail("research", f"`{name}`: a scheduled edition of `{sid}` names no edition id of its own (`{ed}`)")
            editions.add(ed)
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                r.fail("research", f"`{name}`: the scheduled edition `{ed}` of `{sid}` has no `in_force` date")
            if aff is not None and not (isinstance(aff, list) and all(isinstance(x, str) and x for x in aff)):
                r.fail("research", f"`{name}`: `affects` of the scheduled edition `{ed}` of `{sid}` is no list of parts")
                aff = None
            reached = sorted({k for k, b in every if b.get("source") == sid and (not aff or not b.get("part") or b.get("part") in aff)})
            r.notes.append(f"research: `{sid}` `{ed}`, in force from {date}: the currency loop raises {len(reached)} record(s): {', '.join(reached) or 'none'}")

    # ip (R14): in the offer, a source is never named, under any of its terms: its records, loops and views speak
    # Commons language. The research, the maker's own model and its workshop (candidates and probes included) are not
    # the offer, and a binding refers to a source by its id, which is no naming (R31)
    terms = sorted({x for s in sources.values() for x in source_terms(s)}, key=len, reverse=True)
    for p, t in texts(off):
        rel = os.path.relpath(p, d).replace(os.sep, "/")
        if rel.startswith("offer/specs/"):
            continue
        body = unbound(p, t, set(sources))
        for x in terms:
            if term_rx(x).search(body):
                r.fail("ip", f"`{os.path.relpath(p, d)}` names `{x}`, which belongs only in `knowledge/sources.yml`")

    # private (R15)
    for p, t in texts(off):
        if EMAIL.search(t) or PHONE.search(t):
            r.fail("private", f"`{os.path.relpath(p, d)}` holds an e-mail address or a telephone number")

    # specs (R21): the kind's specifications, released with the essentials, never redefine the discipline's
    own = sorted(glob.glob(os.path.join(off, "specs", "*.md")))
    if own:
        import check_spec  # noqa: E402
        ids = commons_spec_ids()
        for path in own:
            sp = os.path.relpath(path, d)
            for o, c, t in check_spec.check(path).items:
                if o == "fail":
                    r.fail("specs", f"`{name}/{sp}` does not follow SPECIFICATION: {c}: {t}")
            fm = yaml.safe_load(open(path, encoding="utf-8").read().split("---")[1]) or {}
            if fm.get("id") in ids:
                r.fail("specs", f"`{name}/{sp}` takes the id `{fm.get('id')}` of a specification of the discipline: it may extend, never redefine")
            for w in fm.get("supersedes") or []:
                if str(w).split(":")[-1].split("/")[-1].removesuffix(".md") in ids:
                    r.fail("specs", f"`{name}/{sp}` supersedes `{w}`, a specification of the discipline: it may extend, never redefine")
    return r


def released(r, at, ref, version, expect=None):
    """release (R1, R3, R12, R31, R32): an installed copy is a release, its essentials only, checked again by the same
    code as in its library (LIBRARY R9), against the record digest its lock took from the library's index"""
    import check_library  # noqa: E402
    rel = yml(os.path.join(at, "release.yml"))
    if rel is None:
        r.fail("release", f"`{ref}` is installed without its release record `release.yml`: nothing unreleased is installed")
        return {}
    valid(r, "release", f"{ref}/release.yml", rel, "#/$defs/release")
    if f"{rel.get('library')}/{rel.get('extension')}" != ref:
        r.fail("release", f"`{ref}`: the release record names `{rel.get('library')}/{rel.get('extension')}`")
    if str(rel.get("version")) != str(version):
        r.fail("install", f"`{ref}` is pinned at {version}, and the installed copy is the release {rel.get('version')}")
    for part in ("enhanced", "knowledge", "workshop", "overlays"):
        if os.path.exists(os.path.join(at, part)):
            r.fail("install", f"`{ref}` installs `{part}/`: only the essentials are installed, the enhanced part is served and the research stays in the [domain].core")
    check_library.check_copy(r, at, at, f"`{ref}`", expect=expect)
    if not expect:
        r.gap("release", f"`{ref}`: the lock gives no `record` digest from the library's index; the copy agrees with itself, and whether it is the release the library holds is unverified (LIBRARY R9)")
    return records(os.path.join(at, "registry"))


def bound(rec):
    """`<kind>:<slug>` of every record a record binds: MODEL's bindings (check_model.FIELDS) and the step bindings"""
    for field, target in check_model.FIELDS.get(rec.get("kind"), []):
        if target in ("accountable", "step"):
            continue
        for v in rec.get(field) if isinstance(rec.get(field), list) else [rec.get(field)]:
            if isinstance(v, str) and v:
                yield f"{target}:{v}"
    if rec.get("kind") == "value-stream":
        for st in rec.get("steps") or []:
            for field, target in (("capabilities", "capability"), ("entities", "entity")):
                for v in (st.get(field) or []) if isinstance(st, dict) else []:
                    yield f"{target}:{v}"


def changed(src, rec):
    """the fields an adopted record changed against its archetype; a field written as null differs from a field left
    absent (Q-b): presence is part of the difference"""
    skip = {"adopted_from", "start", "binds"}
    return sorted(x for x in set(src) | set(rec) if x not in skip and ((x in src) != (x in rec) or src.get(x) != rec.get(x)))


def fit(core, r):
    """fit (R9), install (R12) and adopt (R13, R20, R23, R28): what a commons pins, installs and adopts"""
    cfg = yml(os.path.join(core, ".commons", "commons.yml")) or {}
    pins = {x.get("id"): x for x in cfg.get("extensions") or [] if isinstance(x, dict)}
    domain = [i for i in pins if "/" in str(i)]
    prim = [i for i, x in pins.items() if x.get("primary")]
    if len(domain) != 1 or prim != domain:
        r.fail("fit", f"the CORE pins {domain or 'no extension'} with {prim or 'no'} primary: exactly one extension of its kind, as its primary")
    libraries = set((cfg.get("libraries") or {}).keys())
    lock = yml(os.path.join(core, ".commons", "lock.yml")) or {}
    locked = {x.get("id"): x for x in lock.get("extensions") or [] if isinstance(x, dict)}

    offers = {}
    for ref in domain:
        lib = ref.split("/")[0]
        if lib not in libraries and lib == EARLIER:
            r.gap("install", f"`{ref}` comes from `{lib}`, which the CORE does not name in `libraries:`: unmigrated, it is no longer built in")
        elif lib not in libraries:
            r.fail("install", f"`{ref}` comes from the library `{lib}`, which the CORE does not name in `libraries:`")
        at = os.path.join(core, "extensions", *ref.split("/"))
        if not os.path.isdir(at):
            r.fail("install", f"`{ref}` is pinned and not installed under `extensions/{ref}/`")
            continue
        offers[ref] = released(r, at, ref, pins[ref].get("version"), locked.get(ref, {}).get("record"))

    seen = {}
    for k, (rec, f) in records(os.path.join(core, "registry")).items():
        o = rec.get("adopted_from") if isinstance(rec, dict) else None
        if not o:
            continue
        where = os.path.relpath(f, core)
        m = ORIGIN.match(str(o))
        if not m:
            r.fail("adopt", f"`{where}`: `adopted_from: {o}` is not `<library>/<extension>@<version>#<kind>:<slug>`")
            continue
        ref = f"{m['library']}/{m['ext']}"
        if ref not in pins:
            r.fail("adopt", f"`{where}` is adopted from `{ref}`, which the CORE does not pin")
            continue
        if m["version"] != str(pins[ref].get("version")):
            r.fail("adopt", f"`{where}` is adopted from `{ref}@{m['version']}`, and the CORE pins {pins[ref].get('version')}")
        seen[o.split("@")[0] + "#" + o.split("#", 1)[1]] = where
        if ref in offers:
            src = offers[ref].get(f"{m['kind']}:{m['slug']}")
            if src is None:
                r.fail("adopt", f"`{where}`: `{ref}` offers no `{m['kind']}:{m['slug']}`")
                continue
            diff = changed(src[0], rec)
            r.notes.append(f"adopt: {where}: {'adapted: ' + ', '.join(diff) if diff else 'unchanged'}")
        if rec.get("kind") == "body":
            if rec.get("mandate") is None:
                r.gap("adopt", f"`{where}`: the Body's mandate is not resolved here; a null or absent mandate creates none (Q-b)")
            if "part_of" not in rec:
                r.gap("adopt", f"`{where}`: where the Body stands in this commons (`part_of`) is not resolved here")
        if rec.get("kind") == "post" and not rec.get("held_by"):
            r.gap("adopt", f"`{where}`: no one serves this Post here; adopting it appoints no one (Q-b)")

    # open (Q-a): what an adopted record binds and the commons does not hold stays visible; left open on purpose when a
    # decision event names it under `open`
    local = records(os.path.join(core, "registry"))
    held = {f"{k.split(':', 1)[0]}:{rec.get('slug')}" for k, (rec, _) in local.items() if "/" not in k}
    decided = set()
    for f in sorted(glob.glob(os.path.join(core, "lifecycle", "events", "*.y*ml"))):
        ev = yml(f) or {}
        if ev.get("kind") == "decision":
            decided |= {str(x) for x in ev.get("open") or []}
    for k, (rec, f) in local.items():
        if "/" in k or not rec.get("adopted_from"):
            continue
        for ref in sorted(set(bound(rec))):
            if ref not in held:
                if ref in decided:
                    r.notes.append(f"adopt: {os.path.relpath(f, core)}: `{ref}` left open by decision")
                else:
                    r.gap("adopt", f"`{os.path.relpath(f, core)}` binds `{ref}`, which this commons does not hold: open (Q-a)")

    # not-selected (R13): an event, never a record; and never both for one archetype
    for f in sorted(glob.glob(os.path.join(core, "lifecycle", "events", "*.y*ml"))):
        ev = yml(f) or {}
        if ev.get("kind") != "not-selected":
            continue
        a = str(ev.get("archetype") or "")
        m = ORIGIN.match(a)
        if not m:
            r.fail("adopt", f"`{os.path.relpath(f, core)}`: a `not-selected` event names no archetype `<library>/<extension>@<version>#<kind>:<slug>`")
            continue
        key = a.split("@")[0] + "#" + a.split("#", 1)[1]
        if key in seen:
            r.fail("adopt", f"`{os.path.relpath(f, core)}` records `{a}` as not selected, and `{seen[key]}` adopts it")
    return r


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("domain_core", nargs="*")
    ap.add_argument("--core")
    a = ap.parse_args()
    bad = 0
    runs = [(p, check(p)) for p in a.domain_core] + ([(a.core, fit(a.core, Report()))] if a.core else [])
    for p, r in runs:
        n = {o: sum(1 for i in r.items if i[0] == o) for o in ("fail", "should", "gap")}
        print(f"# {p}: {n['fail']} fail · {n['should']} should · {n['gap']} gap")
        for o, c, t in r.items:
            print(f"{o}: {c}: {t}")
        for t in r.notes:
            print(f"note: {t}")
        bad += n["fail"]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
