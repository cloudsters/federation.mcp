#!/usr/bin/env python3
"""read_legacy_body.py — read element 9 of an element model that still calls it `seat`, as Bodies and Posts.

  python read_legacy_body.py <element-model.yml>

Element 9 is the Body, which may contain Bodies and Posts (decided 18 October 2026). Packs written
before that store it as `slug: seat` at `position: 9`. Old names are deprecated input, never
rejected input (H3): this reader accepts them and says that it did. It reads; it writes and
migrates nothing.

The read path is D1's (cloudsters.o `instance/workshop/bodies/D1/mandate.md` §4):

  * kind board, committee                  → Body · governing body
  * kind management, function              → Body · organisational unit
  * kind executive, role                   → Post
    (an executive may read as a Body where an entry names a collective — flagged)
  * sits_in → part_of · holds → holds · sent_by → appointed_by
  * answers_to is kept as a relation; it never establishes accountability (A2)

An unknown or missing kind, a relation that points to no entry, and a Post with no `sits_in`
(its `part_of` stays open; it is never derived from `answers_to`) are reported as gaps and
never guessed (A2, A3).

Prints the reading as YAML. Exit 0 when every entry was read without a gap, 1 with gaps, 2 when
the input holds no element 9.
"""
import sys

import yaml

LEGACY_SLUGS = {"seat"}
CURRENT_SLUG = "body"

FORMS = {
    "board": ("body", "governing-body"),
    "committee": ("body", "governing-body"),
    "executive": ("post", None),
    "management": ("body", "organisational-unit"),
    "function": ("body", "organisational-unit"),
    "role": ("post", None),
}
MAY_READ_AS_BODY = {"executive"}

RENAMED = {"sits_in": "part_of", "holds": "holds", "sent_by": "appointed_by"}
REFERENCES = ("answers_to", "sits_in", "sent_by")


def element_nine(model):
    for e in model.get("elements") or []:
        if e.get("position") == 9 or e.get("slug") in LEGACY_SLUGS | {CURRENT_SLUG}:
            return e
    return None


def read_entry(entry, known, gaps):
    slug = entry.get("slug") or "<no slug>"
    kind = entry.get("kind")
    out = {"slug": slug, "title": entry.get("title")}
    if kind in FORMS:
        record, form = FORMS[kind]
        out["record"] = record
        if form:
            out["form"] = form
        if kind in MAY_READ_AS_BODY:
            out["note"] = "may read as a Body where the entry names a collective"
    else:
        out["record"] = None
        gaps.append(f"{slug}: kind {kind!r} has no reading — left open, not guessed")
    for old, new in RENAMED.items():
        if entry.get(old) not in (None, [], ""):
            out[new] = entry[old]
    if out.get("record") == "post" and "part_of" not in out:
        out["part_of"] = None
        gaps.append(f"{slug}: Post with no sits_in — part_of left open, not derived from answers_to (A2, A3)")
    if entry.get("answers_to"):
        out["answers_to"] = entry["answers_to"]
        out["accountability"] = "not established by answers_to; needs an explicit mandate (A2)"
    for ref in REFERENCES:
        target = entry.get(ref)
        if target and target not in known:
            gaps.append(f"{slug}: {ref} points to {target!r}, which is no entry — an open chain (A3)")
    out["read_from"] = {"kind": kind}
    return out


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    model = yaml.safe_load(open(sys.argv[1], encoding="utf-8")) or {}
    nine = element_nine(model)
    if nine is None:
        print(f"no element 9 in {sys.argv[1]}")
        return 2
    notices = []
    if nine.get("slug") in LEGACY_SLUGS:
        notices.append(f"deprecated input read: element 9 stored as slug {nine['slug']!r}"
                       f" at position {nine.get('position')}; read as {CURRENT_SLUG!r} (H3)")
    library = nine.get("library") or []
    known = {e.get("slug") for e in library}
    gaps = []
    records = [read_entry(e, known, gaps) for e in library]
    count = {}
    for r in records:
        key = r["record"] if r.get("form") is None else f"{r['record']} · {r['form']}"
        count[key or "gap"] = count.get(key or "gap", 0) + 1
    meta = model.get("meta") or {}
    yaml.safe_dump({
        "source": {"file": sys.argv[1], "pack": meta.get("pack"), "model_version": meta.get("version")},
        "notices": notices,
        "summary": {"entries": len(records), **count, "gaps": len(gaps)},
        "gaps": gaps,
        "records": records,
    }, sys.stdout, sort_keys=False, allow_unicode=True, width=110)
    return 1 if gaps else 0


if __name__ == "__main__":
    sys.exit(main())
