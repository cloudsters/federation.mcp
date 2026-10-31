#!/usr/bin/env python3
"""take_update.py — a commons takes up a newer release of its extension by a decision of its own (extension.md R20).

Three-way, record by record, for every record that names the older release in `adopted_from`:
- the origin's rename map (R3) renames the origin id; the commons' record follows it where the commons kept the
  origin's slug, and surfaces a conflict where the commons gave the record a slug of its own;
- a reference to a record the commons renames follows it in every record of the registry, adopted or own. Which
  fields refer to which kind is MODEL's binding definition (`check_model.FIELDS`), the step bindings, and the
  `x-refers` a kind's specification declares in its schema: no second grammar;
- a field the origin changed is taken where the commons left it as it was; a field the commons changed is kept;
  a field both changed differently is a conflict, never overwritten;
- `adopted_from` names the newer release, and every archetype it names is offered there;
- a `not-selected` event stays as it is: it names what the commons decided against at that version.

Before anything is written, every resulting identity and path is checked against every record of the registry
and against each other: a rename that would take the place of another record, or two renames that would meet,
is a conflict, and nothing is written. `--keep-local` never licenses an overwrite.

Usage:  take_update.py CORE --from OLD_RELEASE --to NEW_RELEASE [--apply] [--keep-local]
        OLD_RELEASE and NEW_RELEASE are release copies (release.yml, registry/, …). Without --apply it lists what it
        would do. With --apply it writes everything, or nothing while a conflict is open: an update is one act of the
        commons, never half taken. --keep-local is the commons' decision on its conflicts of slug and value: it keeps
        its own, and the record names the newer origin. A retired origin and a collision stay conflicts. Installing
        the new copy, the pin and the decision event are the commons' own steps (FLOW). Exit 2 while a conflict is open.
"""
import argparse
import copy
import glob
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_model  # noqa: E402

STEP = {"capabilities": "capability", "entities": "entity"}   # the bindings of a value stream's steps
SKIP = {"adopted_from", "binds", "start"}


def yml(p):
    return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def records(reg):
    out = {}
    for f in sorted(glob.glob(os.path.join(reg, "*", "*.y*ml"))):
        rec = yml(f) or {}
        if isinstance(rec, dict) and rec.get("kind") and rec.get("slug"):
            out[f"{rec['kind']}:{rec['slug']}"] = (rec, f)
    return out


def declared(*roots):
    """the bindings a kind's specification adds: `x-refers: {field: kind}` per record kind in its schema's $defs"""
    out = {}
    for root in roots:
        for p in glob.glob(os.path.join(root, "**", "*.schema.json"), recursive=True):
            for kind, d in (json.load(open(p, encoding="utf-8")).get("$defs") or {}).items():
                if isinstance(d, dict) and isinstance(d.get("x-refers"), dict):
                    out.setdefault(kind, {}).update(d["x-refers"])
    return out


def bindings(kind, domain):
    b = {f: t for f, t in check_model.FIELDS.get(kind, [])}
    b.update(domain.get(kind, {}))
    return b


def follow(value, target, renames):
    """value with every reference of kind `target` renamed; a step is `stream/step` and follows its stream"""
    if isinstance(value, list):
        return [follow(v, target, renames) for v in value]
    if not isinstance(value, str):
        return value
    if target == "step" and "/" in value:
        stream, step = value.split("/", 1)
        return f"{renames.get('value-stream', {}).get(stream, stream)}/{step}"
    return renames.get(target, {}).get(value, value)


def rename_refs(rec, renames, domain):
    """a copy of the record with every reference in it to a renamed record renamed"""
    out = copy.deepcopy(rec)
    for field, target in bindings(rec.get("kind"), domain).items():
        if field in out:
            out[field] = follow(out[field], target, renames)
    if rec.get("kind") == "value-stream":
        for st in out.get("steps") or []:
            for field, target in STEP.items():
                if isinstance(st, dict) and field in st:
                    st[field] = follow(st[field], target, renames)
    return out


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("core")
    ap.add_argument("--from", dest="old", required=True)
    ap.add_argument("--to", dest="new", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--keep-local", action="store_true")
    a = ap.parse_args()
    ro, rn = yml(os.path.join(a.old, "release.yml")), yml(os.path.join(a.new, "release.yml"))
    ref = f"{ro['library']}/{ro['extension']}"
    old_v, new_v = ro["version"], rn["version"]
    renames = {}
    for o, n in (rn.get("renames") or {}).items():
        k, s = o.split(":", 1)
        if n:
            renames.setdefault(k, {})[s] = n.split(":", 1)[1]
    domain = declared(os.path.join(a.core, "specs"), os.path.join(a.new, "specs"))
    base, newer = records(os.path.join(a.old, "registry")), records(os.path.join(a.new, "registry"))
    local = records(os.path.join(a.core, "registry"))
    plan, conflicts, writes, held = [], [], {}, set()

    moved_here = {}   # the renames this commons follows: only its own records that take the origin's new slug
    for key, (rec, f) in local.items():
        o = str(rec.get("adopted_from") or "")
        if o.startswith(f"{ref}@{old_v}#"):
            okind, oslug = o.split("#", 1)[1].split(":", 1)
            nslug = renames.get(okind, {}).get(oslug, oslug)
            if nslug != oslug and rec.get("slug") == oslug:
                moved_here.setdefault(okind, {})[oslug] = nslug

    for key, (rec, f) in local.items():
        where = os.path.relpath(f, a.core)
        out = copy.deepcopy(rec)
        o = str(rec.get("adopted_from") or "")
        if o.startswith(f"{ref}@{old_v}#"):
            okind, oslug = o.split("#", 1)[1].split(":", 1)
            nslug = renames.get(okind, {}).get(oslug, oslug)
            origin_old = (base.get(f"{okind}:{oslug}") or ({}, None))[0]
            origin_new = newer.get(f"{okind}:{nslug}")
            if origin_new is None:
                conflicts.append(f"{where}: `{okind}:{oslug}` is retired in {new_v} and offered no more: the commons decides")
                held.add(f)
                continue
            origin_new = origin_new[0]
            if nslug != oslug:
                if rec.get("slug") == oslug:
                    out["slug"] = nslug
                    plan.append(f"rename: {where}: `{oslug}` → `{nslug}`, as the origin renamed it")
                elif a.keep_local:
                    plan.append(f"kept: {where}: the commons' slug `{rec.get('slug')}`, by its decision; the origin is now `{nslug}`")
                else:
                    conflicts.append(f"{where}: the origin renamed `{oslug}` to `{nslug}`, and the commons calls it `{rec.get('slug')}`: kept, for decision")
                    held.add(f)
            was_rec, mine_rec = rename_refs(origin_old, renames, domain), rename_refs(rec, renames, domain)
            for fld in sorted((set(origin_old) | set(origin_new)) - SKIP - {"slug"}):
                was, now, mine = was_rec.get(fld), origin_new.get(fld), mine_rec.get(fld)
                if now == was or mine == now:
                    continue
                if mine == was:
                    out[fld] = now
                    plan.append(f"take: {where}: `{fld}` as {new_v} has it")
                elif a.keep_local:
                    plan.append(f"kept: {where}: the commons' `{fld}`, by its decision")
                else:
                    conflicts.append(f"{where}: `{fld}` changed in {new_v} and in the commons: kept, for decision")
                    held.add(f)
            out["adopted_from"] = f"{ref}@{new_v}#{okind}:{nslug}"
        moved = rename_refs(rec, moved_here, domain)
        for fld, val in rec.items():
            if fld in SKIP or fld == "slug" or moved.get(fld) == val:
                continue
            if out.get(fld) == val:
                out[fld] = moved[fld]
                plan.append(f"reference: {where}: `{fld}` follows the rename")
        if out != rec and f not in held:
            writes[f] = out

    # preflight: no write takes the place of another record, and no two writes meet
    files = {os.path.normcase(os.path.abspath(p)) for p in glob.glob(os.path.join(a.core, "registry", "*", "*"))}
    targets = {}
    for f, out in writes.items():
        target = os.path.join(os.path.dirname(f), f"{out['slug']}{os.path.splitext(f)[1]}")
        t, src = os.path.normcase(os.path.abspath(target)), os.path.normcase(os.path.abspath(f))
        new_key = f"{out.get('kind')}:{out.get('slug')}"
        where = os.path.relpath(f, a.core)
        if t != src and t in files:
            conflicts.append(f"{where}: becoming `{new_key}` would take the place of `{os.path.relpath(target, a.core)}`, another record: nothing written, for decision")
        elif new_key in local and os.path.normcase(os.path.abspath(local[new_key][1])) != src:
            conflicts.append(f"{where}: becoming `{new_key}` would meet the record `{os.path.relpath(local[new_key][1], a.core)}`: nothing written, for decision")
        if t in targets:
            conflicts.append(f"{where} and {targets[t]}: both would become `{os.path.relpath(target, a.core)}`: nothing written, for decision")
        targets[t] = where

    for line in plan:
        print(line)
    for line in conflicts:
        print(f"conflict: {line}")
    print(f"# {a.core}: {ref} {old_v} → {new_v}: {len(writes)} records to write, {len(conflicts)} conflicts")
    if a.apply and conflicts:
        print("# nothing written: decide the conflicts first (--keep-local keeps the commons' own; it never overwrites)")
    elif a.apply:
        for f, out in writes.items():
            target = os.path.join(os.path.dirname(f), f"{out['slug']}{os.path.splitext(f)[1]}")
            with open(target, "w", encoding="utf-8", newline="\n") as h:
                yaml.safe_dump(out, h, sort_keys=False, allow_unicode=True, width=120)
            if os.path.normcase(target) != os.path.normcase(f):
                os.remove(f)                  # one record, one file, named by its slug
    return 2 if conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
