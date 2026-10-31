#!/usr/bin/env python3
"""check_glossary.py — the glossary is consistent with itself.

  * every entry matches schemas/glossary.term.schema.json (when the jsonschema package is present;
    otherwise the required fields and the closed vocabularies are checked by hand);
  * the file name is the id, and no id appears twice;
  * every term id named in `relations` exists;
  * every `use:` in rejected.yml names an existing term;
  * a definition is one sentence.

Exit 0 when clean, 1 with a list of findings otherwise.
"""
import glob
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..")
SCHEMA = os.path.join(BASE, "schemas", "glossary.term.schema.json")
TERMS = os.path.join(BASE, "glossary", "terms")
REJECTED = os.path.join(BASE, "glossary", "rejected.yml")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    schema = json.load(open(SCHEMA, encoding="utf-8"))
    try:
        import jsonschema
        validate = jsonschema.Draft202012Validator(schema).iter_errors
    except ImportError:
        validate = None
    findings, entries = [], {}
    for path in sorted(glob.glob(os.path.join(TERMS, "*.yml"))):
        name = os.path.splitext(os.path.basename(path))[0]
        e = yaml.safe_load(open(path, encoding="utf-8"))
        if validate:
            for err in validate(e):
                findings.append(f"{name}: {err.message}")
        else:
            for k in schema["required"]:
                if k not in e:
                    findings.append(f"{name}: missing {k}")
            for k in ("layer", "kind", "statement", "status"):
                allowed = schema["properties"][k]["enum"]
                if k in e and e[k] not in allowed:
                    findings.append(f"{name}: {k} '{e[k]}' not in {allowed}")
        if e.get("id") != name:
            findings.append(f"{name}: id '{e.get('id')}' differs from the file name")
        if e.get("id") in entries:
            findings.append(f"{name}: id appears twice")
        entries[e.get("id")] = e
        d = e.get("definition", "")
        if len(re.findall(r"[.!?](\s|$)", d.strip())) > 1:
            findings.append(f"{name}: definition is more than one sentence")
    for name, e in entries.items():
        for rel, target in (e.get("relations") or {}).items():
            for t in ([target] if isinstance(target, str) else target):
                if t not in entries:
                    findings.append(f"{name}: relation {rel} → '{t}' is not a term")
    for r in (yaml.safe_load(open(REJECTED, encoding="utf-8")) or {}).get("rejected", []):
        if r.get("use") not in entries:
            findings.append(f"rejected '{r.get('term')}': use '{r.get('use')}' is not a term")
    for f in findings:
        print("✗", f)
    print(f"{len(entries)} terms · {len(findings)} findings" + ("" if validate else " (jsonschema not installed — basic checks)"))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
