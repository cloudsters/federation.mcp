#!/usr/bin/env python3
"""make_agent.py — generate a CORE's agent file, AGENT.md, in its five parts (core.md R36), with its build record.

The five parts, each generated from the CORE's records:

  ## 1 · Who                  id, name and purpose; kind and truth claim (own commons, observed twin, world); the subject
                              boundary; holder, stewards and advisors; languages; stage; who may read it; the commons
                              definition with its installed pattern id
  ## 2 · Where                each area by structure key: its place, what it holds, when to read it, source or generated;
                              related COREs, what flows and what never crosses; folder notes; installed versions
  ## 3 · How it answers       from the CORE's graph (GRAPH); the load-bearing claims by id with their standing; an empty
                              answer is *not visible to us*; what was searched; what its own MCP serves; where
                              it reads the canon, `federation.mcp`, and its offer per shell (R38)
  ## 4 · What it never does   by requirement id, never restated; nothing of a more restricted class; deleting is not
                              removal; another commons' content only as form; no rejected word of the glossary
  ## 5 · How a role starts    the start line, start files and handover notes, the Bodies and Offices, the board, and
                              that open items are read before anything is treated as decided

Parts 1 to 5 are read from the CORE's own records: `commons.yml` (or `identity.yml` at its earlier place, R4),
`lifecycle/stage.yml`, `access.yml`, the areas as they lie, the installed extract, the MCP declaration and the
start files of its roles. The commons' own guidance, the section `## Own guidance` of an existing AGENT.md, is
kept as it is. The build record `.build/agent/manifest.json` names every input with its hash and the hash of
the generated part, so that check_core.py can tell a hand edit and a stale input from a regeneration.

Usage:  make_agent.py CORE [--own FILE] [--check]
        --own takes the own guidance from FILE where AGENT.md has none yet; --check writes nothing and exits
        with 1 where AGENT.md is not what this tool would generate.
"""
import argparse
import glob
import hashlib
import json
import os
import sys

import yaml

VERSION = "0.3.0"
OWN = "## Own guidance"
AREAS = [  # structure key, default place, earlier places, what it holds, when to read it, source or generated
    ("registry", "registry", ["instance/registry"], "the commons' own model, one record per file", "for what the commons is and does", "source"),
    ("knowledge", "knowledge", ["instance/workshop/evidence", "workshop/evidence"], "sources and claims with their standing", "before stating a fact", "source"),
    ("operations", "operations", ["instance/operations"], "loops and their readings", "for how the commons steers itself", "source"),
    ("lifecycle", "lifecycle", [], "the stage and the events", "before treating anything as decided", "source"),
    ("workshop", "workshop", ["instance/workshop"], "open work, studies, start files and handover notes", "to resume a role", "source"),
    ("views", "views", [], "renderings, never a source of fact", "to read, never to edit", "generated"),
    ("specs", "specs", ["instance/specs"], "the specifications it holds, own and installed", "before changing any record", "source; installed ones read-only"),
    ("extensions", "extensions", [], "the installed essentials of its extension", "for what is offered to adopt", "installed, read-only"),
    ("patterns", "patterns", ["instance/patterns"], "the installed extract and the commons' own patterns", "before inventing a solution", "installed, read-only; own patterns source"),
    ("offer", "offer", [], "what this CORE offers to commons of a kind", "when releasing", "source"),
]


def yml(p):
    return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def digest(path):
    return hashlib.sha256(open(path, "rb").read().replace(b"\r\n", b"\n")).hexdigest()


def generate(core):
    """the generated part of AGENT.md, and the inputs it was read from"""
    inputs = []

    def read(rel):
        p = os.path.join(core, rel)
        if os.path.exists(p):
            inputs.append(rel)
            return yml(p)
        return None

    cfg = read(".commons/commons.yml")
    earlier = cfg is None
    if earlier:
        idn = read(".commons/identity.yml") or {}
        cfg = {"id": idn.get("slug"), "name": idn.get("name"), "code": idn.get("code"), "language": idn.get("locale"),
               "purpose": idn.get("purpose"), "instance_type": idn.get("instance_type"),
               "stewards": idn.get("stewards") or [], "stage": idn.get("stage")}
    stage = (read("lifecycle/stage.yml") or {}).get("stage") or cfg.get("stage")
    access = read(".commons/access.yml") or read("access.yml")
    conf = read(".commons/config.yml") or {}
    federation = access.get("federation") if isinstance(access, dict) else None   # the canon's MCP (`mcp` R24)
    mcp = cfg.get("mcp") or (conf.get("mcp") or {}).get("commons", {}).get("endpoint")   # the commons' own
    if not mcp and os.path.exists(os.path.join(core, ".mcp.json")):
        inputs.append(".mcp.json")
        servers = (json.load(open(os.path.join(core, ".mcp.json"), encoding="utf-8")).get("mcpServers") or {}).values()
        mcp = [s.get("url") for s in servers if isinstance(s, dict) and s.get("url")]
    mcp = [m for m in ([mcp] if isinstance(mcp, str) else mcp or []) if m != federation]

    kind = {"world": f"a world of `{cfg.get('world_of')}`, *what could be*: it holds no evidence of its own",
            "domain": "an observed twin, *what we observe from public data*: not the subject's own commons",
            "game": "a projected future, *what could be*"}.get(cfg.get("instance_type"),
            "an observed profile, *what we observe*, not the subject's own commons" if cfg.get("perspective") == "observed"
            else "its own commons")
    people = [f"`github:{s.get('handle')}` ({s.get('role')})" for s in cfg.get("stewards") or [] if isinstance(s, dict) and s.get("handle")]
    if cfg.get("holder"):
        people.insert(0, f"held by `{cfg['holder']}`")
    read_by = (access or {}).get("class") if isinstance(access, dict) else None
    definition = None
    for idx in sorted(glob.glob(os.path.join(core, "patterns", "*", "index.jsonl"))):
        for line in open(idx, encoding="utf-8"):
            rec = json.loads(line)
            if rec.get("slug") == "the-commons":
                definition = (rec.get("id"), rec.get("summary"))
                inputs.append(os.path.relpath(idx, core).replace(os.sep, "/"))
                break

    out = [f"# {cfg.get('name') or cfg.get('id')} — agent file", "",
           "<!-- Parts 1 to 5 are generated by make_agent.py from this CORE's records; the build record is .build/agent/manifest.json. Change the records and regenerate; never edit these parts. -->",
           "", "## 1 · Who", ""]
    out.append(f"- **Commons:** `{cfg.get('id')}`, *{cfg.get('name')}*" + (f", code `{cfg.get('code')}`" if cfg.get("code") else "") + f"; {kind}.")
    out.append(f"- **Purpose:** {cfg.get('purpose')}" if cfg.get("purpose") else "- **Purpose:** not yet stated in its record: a gap, never to be filled by an agent (`flow-bodies` R18).")
    out.append(f"- **Who answers:** {', '.join(people)}." if people else "- **Who answers:** no holder or steward recorded: a gap.")
    langs = [cfg.get("language")] + [l for l in cfg.get("languages") or []]
    out.append(f"- **Languages:** {', '.join(f'`{l}`' for l in langs if l)}; identifiers, keys and the terms of MODEL stay English (`core` R23).")
    out.append(f"- **Stage:** {stage or 'not recorded'}.")
    out.append(f"- **Who may read it:** {read_by}; nothing of a more restricted class enters it." if read_by
               else "- **Who may read it:** whoever has read access to this repository; nothing of a more restricted class enters it, issue titles and commit messages included.")
    out.append(f"- **What a commons is:** {definition[1]} (`{definition[0]}`)." if definition
               else "- **What a commons is:** read from the installed definition pattern; it is not installed here yet (`core` R28).")
    if earlier:
        out.append("- **Generation:** read from `.commons/identity.yml`, its earlier place: this CORE is unmigrated (`core` R4).")
    out += ["", "## 2 · Where", "", "| Structure key | Place | Holds | Read it | Kind |", "|---|---|---|---|---|"]
    loc = cfg.get("locations") or {}
    for key, default, prev, holds, when, src in AREAS:
        place = loc.get(key) or next((p for p in [default] + prev if os.path.isdir(os.path.join(core, p))), None)
        if place:
            note = "" if place == default or key in loc else " (earlier place)"
            out.append(f"| `{key}` | `{place}/`{note} | {holds} | {when} | {src} |")
    rel = [f"`{v}` ({k})" for k, v in (cfg.get("related") or {}).items()] if isinstance(cfg.get("related"), dict) else []
    out += ["", f"**Related COREs:** {', '.join(rel)}." if rel else "**Related COREs:** none recorded.",
            "", "## 3 · How it answers", "",
            "From this CORE's graph over all its sources, of which an installed extract is one (`graph` R12): a few candidates, only the files used, and every answer names its source cut, run and method. A source outweighs a synthesis; an empty answer is *not visible to us*, never *does not exist*; say what was searched; a service out of reach is noted once, and the work goes on from the files.",
            "", f"**Served:** this CORE's own MCP at {', '.join(f'`{m}`' for m in mcp)} serves it to those who do not work in its repository (`mcp`)." if mcp else "**Served:** no MCP of its own declared.",
            "", f"**Federation:** `federation.mcp` at `{federation}` (`access.yml`) serves the canon of the Commons, which this CORE does not hold. At the start of each session, ask it for a qualified connection; reached, take a new reading of what it offers each shell into `.commons/federation.yml`; out of reach, work from the last reading and name its age (`core` R38)." if federation
            else "**Federation:** `access.yml` names no `federation.mcp`, so no reading of its offer can be taken: a gap (`core` R38; `mcp` R24).",
            "", "## 4 · What it never does", "",
            "By requirement, never restated: `flow-bodies` R3, R14, R18; `core` R15, R16, R19, R26, R28, R34. Nothing of a more restricted class enters this CORE, issue titles and commit messages included; deleting is not removal, because the history keeps it; another commons' content is used only as a form; no rejected word of the glossary is used.",
            "", "## 5 · How a role starts", ""]
    starts = sorted(glob.glob(os.path.join(core, "**", "bodies", "start", "*.md"), recursive=True))
    starts = [s for s in starts if ".git" not in s.split(os.sep)]
    out.append("`You take part as <handle>; read <start file>.` (`flow-bodies` R24). The start file holds everything else; a new session resumes from its handover note, its mandate and its open items before it writes anything (R11).")
    if starts:
        out += ["", "| Role | Start file |", "|---|---|"]
        code = cfg.get("code") or "XX"
        for s in starts:
            r = os.path.relpath(s, core).replace(os.sep, "/")
            inputs.append(r)
            out.append(f"| `@{os.path.basename(s)[:-3]}-{code}` | `{r}` |")
    out += ["", "The open items of the board are read before anything is treated as decided.", ""]
    return "\n".join(out), sorted(set(inputs))


def own_of(text):
    return text.split("\n" + OWN, 1)[1] if text and ("\n" + OWN) in text else None


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("core")
    ap.add_argument("--own")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    path = os.path.join(a.core, "AGENT.md")
    current = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    gen, inputs = generate(a.core)
    own = own_of(current)
    if own is None:
        own = "\n\n" + (open(a.own, encoding="utf-8").read().strip() if a.own else "*Not yet written.*") + "\n"
    text = gen + "\n" + OWN + own
    if a.check:
        same = current.replace("\r\n", "\n") == text
        print("AGENT.md is as generated" if same else "AGENT.md differs from its regeneration")
        return 0 if same else 1
    open(path, "w", encoding="utf-8", newline="\n").write(text)
    os.makedirs(os.path.join(a.core, ".build", "agent"), exist_ok=True)
    man = {"definitions": {"agent": VERSION, "structure": str((yml(os.path.join(a.core, ".commons", "commons.yml")) or {}).get("structure") or "earlier")},
           "inputs": {i: digest(os.path.join(a.core, i)) for i in inputs},
           "output": hashlib.sha256(gen.encode("utf-8")).hexdigest()}
    json.dump(man, open(os.path.join(a.core, ".build", "agent", "manifest.json"), "w", encoding="utf-8", newline="\n"), indent=2)
    print(f"wrote {path} ({len(inputs)} inputs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
