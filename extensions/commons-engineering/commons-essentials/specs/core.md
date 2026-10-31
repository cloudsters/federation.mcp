---
id: core
title: Commons CORE
status: decided
lang: en
touches: [specification, model, core-knowledge, core-views, flow, extension, library, graph, mcp, fabric]
terms: [commons, commons-core, commons-code, scaffold, body, post, shell, world, extension, essentials, bill-of-materials, part, usage, configuration]
schema: schemas/core.schema.json
check: tools/check_core.py
supersedes:
  - Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/LOCAL_WORKSPACE_STRUCTURE_SPEC.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/STAKEHOLDER_REGISTER_SPEC.md
  - ../instance/workshop/bodies/D1/element-9-posts.md
  - Commons-Engineering/commons-core@4acce6b:AGENT.md.template
---

# Commons CORE

*What a commons holds of itself: one repository, in the grammar of MODEL, on the near future.*

## 1 · Goal

A commons needs one place where it holds what it is heading for, in words people and agents read alike. That place is its CORE: one repository with its model, the grounding of that model, its path through time and the views it renders from them. The CORE learns from reality at the start and then leads it, giving it orientation; it is a model drawn with as few strokes as needed, never the world and never a system of record. It orients itself on the canon by installing it as extensions, following their versions and departing from them only visibly, in what it owns (`extension`). This specification decides one thing for its reader: **whether a repository is a well-formed CORE of a commons**. How certain its statements are is specified in `core-knowledge`, and what it renders in `core-views`.

## 2 · Boundary

**Belongs here:**
- the identity and settings of a CORE;
- its areas and where every part lives;
- the near future it holds, and its history;
- its lifecycle;
- the party register;
- the patterns it installs, and its own;
- its bill of materials, single-level;
- world COREs.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| the grammar of the records | MODEL |
| how certain a statement is; `knowledge/` | `core-knowledge` |
| the blueprint definition and the views | `core-views` |
| how the commons works on itself: items, Bodies at work, decisions, rhythms, boot as a conversation | FLOW |
| installing extensions, the hull's release | EXTENSION |
| curating patterns, their release, the extract and the full form of the agents' index | LIBRARY |
| connections across COREs and over time; the graph's sources and runs, answers from it, nothing written back, and what a release may disclose; a bill resolved over more levels, and where a part is used | GRAPH |
| machine access | MCP |

**Touches** the specifications named in the front matter.

## 3 · Terms

All terms resolve in the glossary. No term is new with this specification.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | A CORE is one repository with `.commons/commons.yml` at its root, which validates against `core.schema.json` and says which commons it is, in which language and structure, which extensions it pins with exactly one primary, and which libraries it installs from. | One file tells people and agents which commons this is and how to read it; without a primary extension and a language, nothing can be built on it. | commons |
| R2 | MUST | The `id` is stable and never reused, and other COREs refer to a CORE by its id, never by its repository or display name. | Names change and repositories move; the id is what a reference can rely on. | review |
| R3 | MUST | A CORE's repository name names who holds it, then its world where it is one, then the commons, then its slice as a segment of digits of its own that equals its `slice`, and holds no year, so that a segment of digits only is always a slice and no id or slug is digits only. | The name says whose CORE it is and which horizon it shows, a horizon is never caught up by the calendar, and it is never mistaken for a commons. | names |
| R4 | MUST | Where every part of a CORE lives is decided by the structure definition of the version it states, and a part found at an earlier location is read and reported as unmigrated, never refused. | Readers find every commons whatever its generation, and migration stays a step, not a break. | layout |
| R5 | MUST | A CORE keeps its model, its grounding, its operations, its path, its work in progress, its views, its specifications, what it installs, what it offers, its graph and its Fabric in separate areas, as its structure definition names them, and a retired area holds nothing. | Each area has one job; work in progress, the model and its grounding never mix. | layout |
| R6 | MUST | The registry holds the commons' own model in MODEL's grammar, one record per file, in one folder per element and one current generation; the record, not the file, is the unit, so depth a CORE only serves may be held densely, each record with a stable, addressable id. | A model held in two generations at once is two models, and what a commons maintains itself it must be able to change record by record. | registry |
| R7 | MUST | A part moved to another location is stated once in `locations`, as a folder or as `owner/repo@rev:path`, and no part lives in two places. | A move is a declaration, not a copy; a copy drifts. | layout |
| R8 | MUST | A CORE moves to a new structure in one run, with the tools that read it, and is never moved back. | Half a migration leaves two layouts beside each other. | review |
| R9 | MUST | The CORE holds the commons' near future as a model through which the commons regulates itself: its records say what the commons is heading for, informed by the evidence in `knowledge/`, and are never predictions, never the world and never a system of record, which is read against it, and completeness is not its aim. | The CORE gives orientation and lags reality only while it learns, and a model that tries to be the world becomes neither. | review |
| R10 | MUST | Every accepted change is a commit, a CORE is the repository of the shell pair of SEED and CORE by the pair rule (`flow-workshops` R12), and the history of `main` is never rewritten and every earlier state stays readable. | Git is the model's history: earlier pictures and intentions, held against later observations in `knowledge/`, and never the past of the commons itself; the model is kept by the innermost pair of shells. | review |
| R11 | MUST | `lifecycle/stage.yml` holds the CORE's stage, since when, and the event that set it, and it changes only through a `stage-change` event. | One source for the stage, and every change of it traceable. | lifecycle |
| R12 | MUST | Every event in `lifecycle/events/` is one dated record of its kind, subject, title and who acted, linked to its work item or naming its source, and it refers to evidence, records and people instead of copying them. | The event stays small; the facts stay where they are kept. | lifecycle |
| R13 | MUST | Events are appended and never edited: a wrong event is named by a later `correction`, and events are read in the order of date, recorded and id. | The path of a commons cannot be rewritten after the fact. | lifecycle |
| R14 | MUST | The party register is the one place in a CORE that names people, and per person it holds only a stable id `P_nnnn`, a name, a role or Post, and one way to reach them. | Who decided and who answers must be visible, and nothing more about a person is needed for that. | people |
| R15 | MUST | Outside the party register and `knowledge/`, a CORE names people only by an identifier, `person:` or `github:`, resolved so that a rename is reported, not lost. | Records stay free of personal data and survive a rename. | people |
| R16 | MUST | What another party keeps of its dealings with the commons is not part of the CORE's model or settings. | The CORE is the commons' own; another party's view of it lives with that party. | layout |
| R17 | MUST | A world CORE has the same hull as the CORE it is projected from, names that CORE, its slice and its date, holds no evidence of its own, and keeps each generation as a tagged commit with a `milestone` event. | A world is a full instance of its time slice; its generations show how the picture of a future shifted. | world |
| R18 | MUST | The build record of everything the CORE generates is committed with it, so that every generated file can be traced to its inputs. | Provenance lost with a working copy cannot be recovered. | build |
| R19 | MUST | Secrets, and material a commons explicitly excludes, stay in an approved store outside the CORE and never enter its records, items, views or logs. | Read access to a repository is read access to all of it. | review |
| R21 | MUST | A CORE is sovereign: founding it needs nobody's approval, whatever it receives from an extension or another CORE it may adopt, adapt or not select with its reasons, and it can leave its host without losing its identity, because its history, records and settings are plain files in git. | A centre of gravity is not a gatekeeper, and a commons that cannot leave its host is not sovereign. | review |
| R23 | MUST | Identifiers, keys, slugs and file names are English, and only what people read is in the commons' languages. | Comparable machinery, and every commons in its own words. | review |
| R26 | MUST | A CORE keeps its specifications in `specs/`, its own and those it installs, and an installed specification is recorded with its origin `owner/repo@rev:path` and version in the generated lock and is never edited in place. | One place for what a commons requires of itself, and what it adopts stays the same text it adopted. | layout |
| R28 | MUST | A CORE installs, read-only under `patterns/<library>/`, the extract of patterns of one release of a library it names, as LIBRARY cuts it, with its release record, the licence, attribution and change notices of each pattern file and the agents' index, and never edits it. | Patterns work offline in every commons while the rest stays served, and a licence travels with what it licenses. | patterns |
| R29 | MUST | The lock records each installed extract by its release and the record digest the library's index gives at the pinned revision, an extract is installed and kept only while the gate's checks of a release copy pass on it against that digest (`library` R9), and a newer extract is taken up by decision. | A commons must see which extract it follows, and a change in place to any of its files, a pattern, the index or the record, must show; one check of a copy, the library's, holds wherever a copy lies. | patterns |
| R30 | MUST | A pattern is referred to by its source-qualified id `<source>/<id>`, where `<source>` is the library or the CORE that holds it and `<id>` the pattern's stable `id`, and its slug is only a label. | Own patterns, renamed patterns and several libraries never collide, in the form GRAPH uses across commons. | patterns |
| R34 | MUST | A commons' own patterns, where it holds any, are single files in the patterns' form directly in `patterns/`, each with its own `id` and no computed relation written into it; an adaptation of an installed pattern is an own pattern whose `adopted_from` names the origin's source-qualified id and release and that keeps the origin's licence, and no own pattern takes an installed pattern's id or slug. | Lineage stays visible and what was installed stays the text that was installed; an adaptation never shadows its origin, and a text a machine rewrites is no longer its authors'. | patterns |
| R35 | MUST | A commons learns from its own Fabric, evidence and observed effects, in `knowledge/` and its graph, and offering a pattern to a library is optional and a person's act, carrying the file, its origin and its licence, never a person, the party register, a served part or anything resting on a source the commons has not released. | Learning is local and real whether or not a commons contributes, and a contribution leaves only with a person and only with what may leave. | review |
| R36 | MUST | A CORE holds one agent-neutral agent file, `AGENT.md` at its root, generated from its records with its build record (R18) and regenerated with any of its inputs, followed by the commons' own guidance, every file meant for one model or tool points to it, in any wording, and a folder note opens by pointing to it and holds only its folder's invariants and steps. | Agents of every lineage must read one and the same commons, and an orientation that is copied or kept by hand drifts the moment its CORE changes. | agent |
| R37 | MUST | A CORE says what it is made of in its bill of materials, single-level and generated, never kept: one line per part it holds or uses directly, by the part's identity and version and its usage, `installed` (a copy held to its digest: a specification, an extension's essentials, an extract), `served` (a part of an installed release delivered and never copied, whose own bill is its provider's), `read` (a system of its Fabric or another CORE its graph reads, under a grant) or `adopted` (an archetype taken into its registry, unchanged or adapted); the installed and served lines are its lock's, the others are generated from the registers and records that hold them, and a bill over more levels is a resolution and never stored (`graph`). | A commons must be able to say in one answer what it is made of now; a bill kept beside what it lists drifts from it, and one stored over several levels is stale the moment a part below it changes. | bill |
| R38 | MUST | A CORE keeps a dated reading of what `federation.mcp` offers each shell, generated at each contact and never kept by hand, naming whom it was read from, when and by what, and no one's access; offline, an agent works from the last reading and names its age, and at the start of each of its sessions the agent file asks for a qualified connection, on the rhythm of work and never on a clock. | A commons aligns itself only with what it knows it can get: the offer is generic and the same for everyone in a shell, a dated reading keeps it at hand offline with its age in view, and an agent learns access only for its own user, so a record of others' access would be kept by no one who could check it (`mcp` R7). | federation |

R22 is merged into R9, R24 into R21, R25 into R3, R33 into R34 and R28; R27 is EXTENSION R12, R31 LIBRARY's and R32 GRAPH's; R20 is cut (part 8). None is reused.

## 5 · Structure

The schema is `schemas/core.schema.json`. Its root is `.commons/commons.yml`; its `$defs` hold `stage`, `event` and `person` (with `people`, the party register).

| Field of `commons.yml` | Holds |
|---|---|
| `id`, `name`, `code` | the stable id; the display name; the commons code of the Body handles |
| `holder` | who holds this CORE, where it is not the commons itself |
| `perspective` | `observed` where the CORE is kept by an outside observer; `own` when absent. Holding a CORE is no mandate to observe |
| `instance_type` | `commons`, or `world` for a world CORE |
| `slice`, `world`, `world_of`, `as_of`, `target` | a world's horizon in years, its name in its set, the id of its CORE, the date of this generation; **`target` = the year of `as_of` + `slice`**, written only for display |
| `language`, `languages` | the commons' own language; further languages of its views |
| `structure` | the version of the structure definition it is on |
| `extensions` | each with `id` and `version`; exactly one `primary`; a domain extension as `<library>/<extension>` |
| `libraries` | `{<id>: <owner>/<repo>}` for every library it installs from |
| `locations` | structure keys moved from their default place |
| `sources`, `mcp` | the repositories it draws on; its MCP endpoints |

**The structure definition** is commons-essentials' `structure.yml`, pinned by version. It gives every structure key its default location and its earlier ones. `access.yml` stays beside `commons.yml` as policy.

**The lock** is `.commons/lock.yml`, generated at install and never edited: `specs` as `{path, origin, version}` (R26), `extensions` as `{id, version, origin, record, installed, served}` (`extension` R12), `patterns` as `{path, origin, record}` (R29).

**The reading of `federation.mcp`** is `.commons/federation.yml` (`$defs/reading`), written at each contact from what `federation.mcp` answers and never edited: `from` (the endpoint, `access.yml`'s `federation`, `mcp` R24), `read_at` (a date or time), `generator` (what took it) and `shells`, all six shells of MODEL (SEED, CORE, PEER, OPEN, DOCK, ROAM), each with the offer every envelope carries (`mcp` R28, `$defs/offered`): `reads`, `writes`, `budget`, each of its limits a number, and `sources` where narrowed. It holds no user, no account and never what one caller `gets`; other metadata is tolerated. Its age is `read_at`, read beside it, never a deadline. The agent file asks `federation.mcp` at the address `access.yml` names for it, apart from the commons' own MCP.

**The bill of materials** is generated by `tools/check_core.py --bill` and never kept as a file. Only a finding on what it lists withholds it: on the lock, the installed copies, the adoptions, among them the checks of `extension` on what it installs and adopts, and the sources read; every other finding stands beside it, whatever a reader filters. It names its `generator` and the `rev` of the CORE it was generated from, and `read_at` where the CORE's files differ from that commit, as a cut of GRAPH names a source. Each line has `part` and `usage` and, where its source gives them, `origin`, `record`, `licence` (that of the release record, `library` R11), `class`, `access`, `holder`, `as` and `adapted`. In a release's part `<library>/<id>@<version>#<part>`, what precedes `#` is the release as the library's index names it, and `record` its digest there; the part's own files are no line of this bill (`library` R3).

| Usage | `part` | Generated from |
|---|---|---|
| `installed` | a specification as `<id>@<version>`; a part of a release as `<library>/<id>@<version>#<part>`, an extract's id being `patterns` (`library` part 5) | the lock |
| `served` | a part of an installed release as `<library>/<id>@<version>#<part>`, named by its release record (`library` R3) | the lock's `served` |
| `read` | a system as `fabric/systems.yml#<id>`; another CORE as `owner/repo@rev` | `fabric/systems.yml`; the graph register's entries of kind `core` |
| `adopted` | the archetype its `adopted_from` names; `as` the commons' own record, and `adapted` whether it differs from the archetype | the registry |

An archetype the commons does not select is no line: its `not-selected` event (`extension` R13) is the other half of the commons' configuration. A commons pins exact releases and takes up a newer one only by decision (R29), so no version range is ever resolved; every revision of `main` is an approved configuration, because `main` changes only by a merge on decision (R10); and there is one bill, read at a revision, whatever it is read for.

**The repository name**, written out: `[holder.][world.][commons][.slice].core`, for example `[commons].core`, `[commons].10.core` and `[world].[commons].20.core`. The holder is omitted where the commons holds its own CORE, and the slice is omitted at 0. A name is displayed as *[commons] CORE +10*; the `+` appears only in the display, because repository names do not allow it.

**Extensions** a CORE installs live in `extensions/<library>/<extension>/` (structure key `extensions`), as `extension` R12 says; their specifications go to `specs/`. What a commons adopts from one is its own record, carrying `adopted_from`, and what it does not select is a `not-selected` event (`extension` R13).

**An offer** is kept in `offer/` (structure key `offer`), apart from the commons' own model: by a `[domain].core` for its domain, and by any CORE that offers what it has learned (`extension` R4).

**Specifications** live in `specs/` at the root (structure key `specs`): `<id>.md`, with `schemas/`, `tools/`, `examples/<id>/` and `glossary/` beside them. At topology tier 1 a CORE installs those of Commons Essentials there; at tier 3 the key may point to a LIBRARY or GRAPH repository of its own (#79 D1), and `<spec>#R<n>` resolves the same way.

**Patterns** live in `patterns/` (structure key `patterns`). An installed extract sits read-only in `patterns/<library>/`: the pattern files at their release paths, and `index.jsonl`, whose first line has `kind: index` and repeats the `release`. LIBRARY specifies the extract and the index. A commons' own patterns are files directly in `patterns/`; an own pattern has `id` and, where it adapts an installed one, `adopted_from: {id, release}`. The extract holds its release record `release.yml` (`library` R3). The generated lock records each extract under `patterns` as `{path, origin, record}`: the folder under `patterns/`, the library release as `owner/repo@rev`, and the record digest the library's index gives for that release. Each installed extract is one entry of the CORE's graph register, pinned by the lock (GRAPH).

**The graph** lives in `graph/` (structure key `graph`): its register `graph/sources.yml`, which the commons writes, and its run packages in `graph/runs/<run>/`, which only the Graph Engine writes (GRAPH R1).

**The party register** is `people.yml` at the root (structure key `people`). It holds `people`, each with `id`, `name`, `role` and an optional `contact`.

**The agent file** is `AGENT.md` at the root. Its generated part ends where the line `## Own guidance` begins, and its build record is `.build/agent/manifest.json`: `definitions`, `inputs` with their hashes, and `output`, the hash of the generated part. What each generated part carries is the generator's, `tools/make_agent.py`, released with Commons Essentials. The own guidance may hold the commons' voice, its domain conventions, research method, quality bar and own practices; it never restates a requirement, carries dated state, names a person outside the register or carries another commons' content. A hand-kept `AGENT.md` is read as unmigrated (R4).

## 6 · Checks

`tools/check_core.py <core>` reads one CORE. It reports **fail**, **should** or **gap**, and exits with 1 only on a fail. It reads the structure definition from a checkout of commons-essentials beside the CORE, and reports a gap where none is at hand. With `--spec core`, `core-knowledge` or `core-views` it runs the checks of that specification only; the check ids are unique across the three, and `review` is the keyword of SPECIFICATION R10, not a check of the tool.

| Check | Tests |
|---|---|
| `commons` | `commons.yml` validates; exactly one primary extension; a written `target` equals the year of `as_of` + `slice` (R1) |
| `names` | a segment of digits only in the folder name equals `slice`, written where `slice` is not 0 and omitted at 0; a folder not named after part 5 is unmigrated, a gap (R3) |
| `layout` | the areas are where the structure definition puts them, earlier locations are reported as unmigrated, retired areas are empty, moved keys are declared once, and no engagement record sits in `.commons/`; a moved area is checked at its declared place like any other, and a remote one that cannot be reached is reported as unverified (R4, R5, R7, R16) |
| `registry` | one folder per element in one generation, and the records pass `check_model.py` (R6) |
| `lifecycle` | `stage.yml` and every event validate; the stage names an existing `stage-change` or `founding` event; a correction names an existing event (R11, R12, R13) |
| `people` | the party register holds only its four fields, and no e-mail address or telephone number appears outside it and `knowledge/` (R14, R15) |
| `world` | a world states its fields, and its `knowledge/` holds nothing (R17) |
| `build` | `.build/` is not ignored by git (R18) |
| `patterns` | an installed extract is recorded in the lock with its path, release and record digest, lies under its library, and passes the gate's checks of a release copy against that digest, the code of `library` and `library-patterns` and no other; no folder under `patterns/` lacks a record; an own pattern has an id of its own and never an installed id or slug, holds no computed relation, and an adaptation names its origin and release and keeps its licence; no extract yet is a gap (R28–R30, R34) |
| `bill` | no file of the CORE's governed state holds a bill, every file but the copies installed from elsewhere and a dated event of `lifecycle/events/` that passes as one; every part of an extension the lock installs or serves is one its release record names; no extension lies under `extensions/` without its entry in the lock; where the CORE installs, serves or adopts from an extension, the checks of `extension` on it pass, the code of `extension` and no other; every system and CORE read names its id; a finding on what the bill lists withholds it, and no other finding does, whatever a reader filters; an adopted line carries the record its pin gives (R37; `extension` R12, R13, R23) |
| `federation` | `.commons/federation.yml` validates against `$defs/reading`, its `read_at` a date or time, each of the six shells an offer of `mcp` `$defs/offered` whose budget holds numbers only, and it holds no user, account, key or `gets`, else a fail; read from another address than `access.yml`'s `federation`, a should naming both; its age is never a fail; without it a gap, taken at the next contact. **Not built yet:** `federation.mcp` does not publish its offer per shell (`mcp`), so no reading can be taken; the gap stays until it does (R38) |
| `agent` | `AGENT.md` exists, else a gap; without its build record a gap (unmigrated); with it, the generator's parts in order, the generated part as recorded and no input changed since; every file of the repository, tracked or new and not ignored, whose first line points to `AGENT.md` is read as a pointer, in any wording, and every folder note opens by pointing to it; a git-ignored local file is the person's and is not read (R36) |
| `review` | a review by the human accountable for this specification's mandate, against the Why of R2, R8, R9, R10, R19, R21, R23 and R35 |

## 7 · Example

**Minimal:** a commons that has just been founded. Its `commons.yml`:

```yaml
id: tool-library
name: Tool library
code: TL
instance_type: commons
language: en
structure: 0.3.0
extensions:
  - {id: commons-essentials, version: 0.1.0, primary: true}
```

**Complete:** [a CORE of a neighbourhood tool library](examples/core/tool-library.core/.commons/commons.yml), with its registry, knowledge, lifecycle, party register and views; `check_core.py` reads it with 0 fail.

**Patterns:** [an installed extract, the library fixture's release copy byte for byte](tools/tests/core/good/patterns.core/patterns/demo-library/release.yml), beside an own adaptation, passes with 0 fail; the same extract with one pattern's text changed after release, its index and lock unchanged (`bad/patterns-body.core`), fails.

**Bill of materials:** [a CORE](tools/tests/core/good/bill.core/.commons/commons.yml) that installs an extension's essentials, is served its enhanced part, reads one system of its Fabric and adopts two archetypes, one of them adapted, has a bill with one line of each usage, which `check_core.py --bill` prints. A served part its release record does not name, an extension installed without its entry in the lock, a bill kept as a file, and an archetype adopted from a version the CORE does not install, each fail, and the last has no bill (`bad/bill-*.core`).

**Agent file:** [a CORE](tools/tests/core/good/agent.core/.commons/commons.yml) whose `AGENT.md`, generated by `make_agent.py`, has its build record, a pointer file and a folder note, each in its own wording, passes with 0 fail; a missing part, a hand edit, an input changed without regeneration and a folder note without the pointer each fail (`bad/agent-*.core`).

**Reading of `federation.mcp`:** [a reading](tools/tests/core/good/bill.core/.commons/federation.yml) of all six shells, as the reference producer emits the offer over [the MCP example's `access.yml`](tools/tests/mcp/access.yml) (`serve_mcp.offer`), passes, and so does one with other metadata or an unquoted time; one that names a user's account, holds what one caller `gets`, has no `read_at` or one that is no date, holds no offer or a shell with users, in it or in its budget, or the old `read`/`write`, or lacks a shell, fails; one read from another address than `access.yml` names is a should naming both. The agent file asks `federation.mcp` at `access.yml`'s address for it with that address alone, with an own MCP beside it and with several client entries, and names the own MCP apart (`tools/tests/core/run_tests.py`).

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | Commons CORE, third of the eight, after MODEL; split along its boundary into `core`, `core-knowledge` and `core-views` | commons.o#89, opened on the word of the human accountable |
| 2026-10-26 | adopted | Adopted after the EA's points (standing from evidence fit for the claim; git as model history; outside observation scoped; locations read, not skipped) and `target` stated; the party register is `people.yml` at the root; the drops rest on the decisions they name; the slice marker stays open (#85) | Holger, commons.o#89, comment 6415733592 |
| 2026-10-26 | revised | the slice is a segment of its own, `[commons].10.core`; a segment of digits only is always a horizon, so no slug is digits only; displayed as *[commons] CORE +10* (R3, R25, part 5) | Holger, commons.o#85, comment 6415790681 |
| 2026-10-26 | revised | the structure key `specs`: specifications in `specs/` at the root of every CORE, own and installed, installed ones in the lock and read-only; a LIBRARY or GRAPH repository is tier 3 (R5, R26, part 5) | Holger, commons.o#89, comment 6418322780 |
| 2026-10-26 | revised | the Goal names how a CORE orients itself on the canon: by installing it as extensions, following their versions and departing only visibly, in what it owns (`extension` R20) | Holger, commons.o#90, comment 6419482445 |
| 2026-10-26 | revised | the structure key `extensions` for installed extensions, read-only, with their resolved identity, origin and version in the lock (R5, R27, part 5) | Holger, commons.o#90, comment 6419928036 |
| 2026-10-26 | revised | **Draft, contingent on the probe of commons.o#90 and not decided:** `instance_type: extension`; only the public parts of an extension installed, as a copy, every other part only ever served (R27); the event kind `not-selected` with `archetype` (part 5, `extension` R13) | Holger, commons.o#90 (the principle, contingent on the probe 6421206970; not yet decided) |
| 2026-10-27 | revised | patterns in the CORE: the structure key `patterns`; every CORE installs the extract of orbits 0–3 with the agents' index, read-only, pinned by release, graph run, extractor and policy; source-qualified ids; links with kind, basis and the meaning of a score, outward ids only and at most five; retrieval, never ingestion; no computed relation in a pattern; the own door with `adopted_from`; learning local, contributing optional; the profiles `lean` and `sovereign` end; the conditions of the EA's read carried (R5, R28–R35, parts 2, 5, 6) | Holger, commons.o#95, comments 6438391848 (H1) and 6438865249 (H2, H3, G1); the EA's read 6439321990 |
| 2026-10-28 | revised | an agent answers from the CORE's graph over all its sources, the extract one of them, naming its source cut, run and method; the extract as an entry of the graph's source register, pinned by the lock; the index's computed links as the federation's run, beside any run of the CORE's own; the CORE installs no part of the federation's graph beyond the index; the reference lookup moves to GRAPH (R28, R32, part 5, part 7) | Holger, commons.o#95, comment 6464307584, on the joint position 6441932744 |
| 2026-10-28 | revised | the agent file: one generated, agent-neutral `AGENT.md` in five parts with its build record, the own guidance below it and bounded, every model or tool file only the pointer line, folder notes; the hull's agent template superseded at its last revision, since the hull removed it on 15 October 2026 (`97e1368`); the lessons of the estate's 95 agent files carried, moved or dropped (R36, parts 5 to 8) | Holger, commons.o#95, comment 6465255055, on 6464550785 |
| 2026-10-28 | revised | the check `agent` reads only the files of the repository: a git-ignored local tool file belongs to the person, not to the CORE, and stays theirs (part 6) | Holger, commons.o#95, comment 6465844553 |
| 2026-10-28 | revised | the area `graph` (R5): the commons' graph in `graph/`, its register `graph/sources.yml` and its runs, as GRAPH places them; the installed extract an entry of that register (R33, part 5) | with GRAPH's adoption, commons.o#93 (merged `fbfdcd5`), as agreed in the R32 decision (commons.o#95, 6464307584) |
| 2026-10-28 | revised | **Draft until E3 of commons.o#90:** the area `offer` (R5); `libraries` (R1); only released extensions installed, their essentials under `extensions/<library>/<extension>/`, the enhanced part served (R27); the record as the unit, dense served depth with stable ids (R6); `instance_type: extension` withdrawn | Holger, commons.o#90, comments 6464648757, 6464676842 and 6464808164 |
| 2026-10-28 | revised | with EXTENSION v2 adopted on its open conditions, the area `offer` (R5), `libraries` (R1), the record as the unit (R6) and the installed essentials under `extensions/<library>/<extension>/` (R27) hold | Holger, commons.o#96, comment 6468782933 (Q-d) |

| 2026-10-28 | commissioned | KISS pass: R25 merged into R3, R22 into R9, R24 into R21, R33 into R34 and R28; R27 is `extension` R12, R31 LIBRARY's and R32 GRAPH's; R29 records release and digest; R1, R5, R15, R17 and R36 slimmed to their goals, the agent file's parts table to its generator; written from a single commons' view: R16 without another party's vocabulary, R20 cut as a workstation practice, R28 and R35 name a library the commons names, no federation's run, the pinned internal path and the estate's reading table removed; the carry-over moves to `carry-over/core.md`. Adopted 29 October 2026 ([commons.o#98, comment 6509202251](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6509202251)) | Holger, commons.o#98 ("Ja, alle") |
| 2026-10-28 | adopted | The KISS revision adopted, R3 as a MUST with a non-`.core` name read as unmigrated | Holger, commons.o#98, comment 6474773388 |
| 2026-10-29 | revised | R10: a CORE is the repository of the shell pair of SEED and CORE, the case of the pair rule that `flow-workshops` R12 sets out for every pair (who merges `main`, who pushes branches and proposes by pull request), which R10 does not restate. Adopted 29 October 2026 ([commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412)) | Holger, commons.o#100 (opening, verbatim: *"ja. main bleibt SEED vorbehalten"*); A6 and H2, comment 6496414850 |
| 2026-10-29 | revised | Part 5: the own guidance no longer holds a choice to work on `main`; with H2 struck, `main` changes only by pull request, in every commons. Adopted 29 October 2026 ([commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412)) | Holger, commons.o#100, comment 6496414850 (H2: *"ja, H2 streichen"*) |
| 2026-10-29 | revised | Part 5: the own guidance holds the commons' *own practices*, no longer its *own disciplines*, so that the word keeps no meaning beside the one A4 retires. Adopted 29 October 2026 ([commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412)) | Holger, commons.o#100, comment 6495768947 (A4: *"'Discipline' -> Commons"*) |
**Rests on:** S1.1, S2, S4, S6, S7, S8 (commons.o#74, 22 and 25 October 2026); the topology tiers (#79 D); the names and rolling time slices (#85 N1, 25 October 2026); the near future (26 October 2026); H6–H8 (#86).
| 2026-10-29 | revised | **Adopted 29 October 2026 ([commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412)).** An installed extract holds its release record, the lock records its record digest instead of its index's, and the extract passes the gate's checks of a release copy against it; CORE's own checks of the extract are retired, so that one check of a copy holds at install (R28, R29, parts 5–7) | the EA, commons.o#98, comment 6501267185; `library` R8, R9 |
| 2026-10-30 | revised | R37 and parts 5–7: the CORE's bill of materials, single-level and generated, never kept, with the usage of each line, `installed`, `served`, `read` or `adopted`, read from the lock, the Fabric's and the graph's registers and the registry; the lock named `.commons/lock.yml`; R5 names the Fabric as an area (`fabric` R1); every line carries its release record's licence, and the bill names its generator and revision; *configuration* no longer means settings (part 2, R16, R21), and R21 says *not select* for the retired *decline*; a bill is generated only from a CORE that passes its checks, and no file holds one. Adopted 30 October 2026 ([commons.o#107, comment 6519835234](https://github.com/Commons-Engineering/commons.o/issues/107#issuecomment-6519835234)) | Holger, commons.o#107 (opening; *"1 ja, 2 ja, 3 ja, wie vorgeschlagen"*; the term review, comment 6516874161: *"ja, wie vorgeschlagen"*, item 5) |
| 2026-10-30 | adopted | R37 adopted, the single-level bill of materials, generated and never kept, with its revision rows of 30 October; the terms *bill of materials*, *part*, *usage* and *configuration* named in `terms` | Holger, commons.o#107, comment 6519835234 (on 6519795859: *"ja, wie vorgeschlagen"*) |
| 2026-10-30 | revised | R36 and parts 6–7: a pointer file and a folder note point to `AGENT.md` in any wording, and the check reads only that; no existing pointer has to change, and the line given for new ones says *settings*. Adopted 30 October 2026 ([commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766)) | Holger, commons.o#98, comment 6524525898 (*"ja, wie vorgeschlagen"*, item 2) |
| 2026-10-30 | revised | Part 6, `bill`: the check reads the governed state, every file but the installed copies, which hold a check's examples, and a dated event that passes as one, among them the found state that healing keeps; only a finding on what the bill lists withholds it, decided where the bill is produced, and every other finding stands beside it, whatever `--spec` filters; an adopted line carries the record its pin gives. Corrections of the EA's reading, no new requirement. Adopted 30 October 2026 ([commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766)) | Holger, commons.o#107, comment 6522699919 (*"A–D ja, wie vorgeschlagen"*, items 2, 3b, 4); commons.o#98, comment 6524525898 (*"ja, wie vorgeschlagen"*, item 3); the EA, comment 6522100364 |
| 2026-10-30 | commissioned | R38: a dated reading of what `federation.mcp` offers each shell, generated at each contact, never kept by hand and naming no one's access; offline work from the last reading with its age named; a qualified connection asked for at the start of each agent session, on the rhythm of work, not a clock. Adopted 30 October 2026 ([commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766)) | Holger, commons.o#98, comment 6524734676 (*"ja, wie vorgeschlagen"*, item 2) |
| 2026-10-30 | adopted | R36 (pointers in any wording), the corrections of `bill` and R38 (the reading of `federation.mcp`) adopted with the robustness set | Holger, commons.o#98, comment 6526694766 (on 6526314655: *"1–6 ja, R24 B, wie vorgeschlagen"*) |
| 2026-10-30 | revised | R38, part 5 and part 6, `federation`: the reading validates against `$defs/reading`, `read_at` a date or time, all six shells each with the offer of `mcp` R28 (`$defs/offered`), its budget numbers only, never `gets` or a user, other metadata tolerated, its age never a fail, another address than `access.yml`'s a should; the agent file asks `federation.mcp` at `access.yml`'s `federation` for it, the commons' own MCP named apart; the example as the producer emits it; no new component. Merged 31 October 2026 (`29e77f4`; Holger, commons.o#98, comment 6542035950: *"beide mergen"*); adopted with the row below | the EA, commons.o#98, comment 6531768044; the Office's check of 0e6163f |
| 2026-10-31 | adopted | R38, parts 5 to 7 and the check `federation`: the reading of `federation.mcp` validated as each shell's offer and the agent file asking `federation.mcp` at `access.yml`'s address, as merged in `29e77f4` | Holger, commons.o#98, comment 6543679246: *"beide annehmen"* |

What this specification supersedes, and what it carries of it, is in [`carry-over/core.md`](carry-over/core.md).
