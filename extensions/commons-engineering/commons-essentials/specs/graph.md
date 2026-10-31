---
id: graph
title: Commons GRAPH
status: decided
lang: en
touches: [specification, model, core, core-knowledge, core-views, flow-graph, extension, library, mcp, graph-engine]
terms: [commons, graph, commons-core, pattern, orbit, extension, visibility-class, delta, address, mcp, bill-of-materials, part, resolution, where-used]
schema: schemas/graph.schema.json
check: tools/check_graph.py
supersedes:
  - Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_KNOWLEDGE_GRAPH_SPEC_DRAFT.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_KNOWLEDGE_GRAPH_LAYERS_DRAFT.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md
  - Commons-Engineering/commons-graph@main:README.md
---

# Commons GRAPH

*One graph per commons, over the sources it names: stated edges read from them, computed edges only from released runs, and nothing ever written back.*

## 1 · Goal

A commons steers by connections that no single file shows: which value stream a pattern serves, which claim grounds which record, which work changes which element, what changed between two revisions, and how others of its kind do the same thing. Its graph holds those connections over a register of its sources: the CORE's own areas, its installed extension and extract, readings from its Fabric, and any further source it names. Stated edges are the fields its sources already hold, read at the revision asked about; computed edges come only from released runs of the Graph Engine (`graph-engine`) and are candidates, never facts. The structure is the same at every level, for a single commons and for a federation, and the graph never writes into a source. This specification decides two things for its reader: **whether a commons' graph is well formed**, and **whether an answer from it says what it rests on**: its source cut, its runs, its method, and what it could not see.

## 2 · Boundary

**Belongs here:** the source register; nodes and their ids; stated edges per source kind; computed edges as a graph reads them; the area `graph/` and its promotion to a repository; answers; deltas between revisions; graphs across commons.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| how a run is ordered, computed, checked, released and stored; the extract's bounds | `graph-engine` |
| records, bindings and addresses | `model` |
| areas, the lock, installed extracts and the answer duty of an agent (R32) | `core` |
| evidence, its standing, and what a reading inherits from its inputs | `core-knowledge` |
| the edges of work | `flow-graph` |
| what is released for reuse, and when; the agents' index in full | `library` |
| serving, shells, grants as a transport, proposals from outside | `mcp` |
| the entities of an engagement | the model of the commons that holds them |

**Touches** `specification`, `model`, `core`, `core-knowledge`, `core-views`, `flow-graph`, `extension`, `library`, `mcp` and `graph-engine`. **Rests on** Holger's words of 27 October 2026: one holistic graph over a growing set of sources with a lifecycle of its own, which never writes into patterns (commons.o#93, comment 6438392453); the same at every level, each graph over its own sources (6438662161); a generic source register and an engine that computes in a rhythm, with no model required (6438807424); answers from the commons' own graph (6441896539); and of 28 October 2026: the run package and `graph/` as an area (6464338661), R32 (commons.o#95, comment 6464307584).

## 3 · Terms

All terms resolve in the glossary. This specification adds none: the source register, a source cut, a run, a run package and an extract are structures of part 5 and of `graph-engine`, not terms.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | A commons has one graph, held in the area `graph/` of its CORE beside `knowledge/`, with its register `graph/sources.yml`, which the commons writes, and its run packages in `graph/runs/<run>/`, which only the Graph Engine writes. | The graph reads across every area and is none of them: a computed association is not evidence, and the registry holds the near future, not candidates. | layout |
| R2 | MUST | Every source is one entry of the register with its id, kind, reference and visibility class, every file belongs to exactly one source, so that a source nested in another's folder owns its files for reading and for its digest alike, and an entry pinned by the lock says `pin: lock` and repeats nothing the lock records. | A source is known by its identity, not its location; a file read under one source and hashed under another would let a restricted file pass as public. | register |
| R3 | MUST | The CORE's registry, `knowledge/`, operations and specifications, its installed extension and each installed extract are sources of its graph, and a further source, such as another commons' CORE, a reading of its Fabric by the reading's id, or a signal, is one more entry and never a change of this specification. | Every commons computes over its own sources, and a new kind of source is one row, not a revision. | register |
| R4 | MUST | No source holds a run's id or a computed relation of its graph, a run never commits to a source, and what a run suggests for a source goes to the workshop as a proposal of that run, which only a person takes in or declines. | A graph that writes back can never be computed again from its sources, a text a machine rewrites is no longer its authors', and a re-run must never erase a human decision. | untouched |
| R5 | MUST | A node is a thing a source holds, under the id its own specification gives it, qualified by the CORE's id as `<core>/<id>` across commons, and the graph gives no node an id of its own, so that a computed grouping never becomes a node, an address or a rival of MODEL's families and one that spans two families is reported as a signal. | One identity per thing, stable when its file moves; a graph that invents nodes holds something no source answers for, and given structure that discovered structure can absorb has stopped being given. | nodes |
| R6 | MUST | A stated edge is a field a source holds, typed by that field and pointing the way the field points, read from the source at the revision asked about, never copied into `graph/`, and its inverse is never stored. | What a source states follows every merge and disappears with it; a copy would be a second truth that ages. | stated |
| R7 | MUST | A stated edge carries the standing of what states it, so that a mandate, a proposal and an observation stay three, and agreement of the graph with its sources is never read as agreement with the world. | A graph that agrees with its sources is aligned, not grounded. | review |
| R8 | MUST | A computed edge exists only in a run package, naming its run, its method, its kind or `unclassified`, the inputs it rests on and, with a score, what the score measures, and is never a confidence; a library's released run that a source carries, as an installed extract does, keeps its run's id, and a run of the commons' own adds its edges beside it, never overwriting or hiding them. | A computed association is a candidate with a known origin, not established or causal support, and whose computation an edge is stays known, so that disagreement stays visible. | computed |
| R11 | MUST | The graph holds no body of a source, no person's contact datum, nothing of the party register, no commercial or account datum and no credential, only ids, edges and the references it read. | The graph knows that things exist and how they connect, not what they say; ids and relations can still disclose, which is why R13 and R24 decide what a caller sees of them. | private |
| R12 | MUST | Every answer names its source cut, each source at the commit it was read from or, where its files differ from that commit, at the time it was read with its digest, an installed extract only after its record has the lock's digest, its files the part digest that record names and its index the digest that record names (`core` R29; `library` R3), together with the runs whose computed edges it used and its method, and it names each source that has moved on or left the register since those runs. | One answer may join a commit, a released run and a live reading; a cut that does not describe what was read is a false provenance, and staleness is stated, never hidden. | answer |
| R13 | MUST | An answer tells apart three silences, what its sources do not hold, that something was withheld from its caller, and what it read only partly, a source stale since a run, a permitted source not read with its reason, or what its budget left out, and what was withheld shows in none of its paths, counts, neighbours or findings. | Absence in a permitted view means not observed here; a hidden target reported as missing still discloses it. | answer |
| R14 | MUST | While the commons has no released run of its own, an answer is computed `stated-only` or `lexical`, and it first follows the stated join from the commons' records through their family to the patterns addressed to that family. | The answer path needs no model, and the family join is the commons' own model meeting the library. | answer |
| R15 | MUST | The graph computes reach, dependency, coverage, connected deltas and possible orders, never a priority, and it returns an order as a set of options. | Everything on the way to a decision may be automated, the decision never. | review |
| R16 | MUST | A delta between two revisions is the list of nodes and stated edges added, removed or changed between them, computed from the history of the sources by their stable ids and never kept by hand. | A commit records a state of the model, which holds the near future, so comparing commits shows how the model changed, not how reality drifted, which only observations show. | review |
| R17 | MUST | A commons reads another commons' sources only as an entry of its register that names that commons' grant, anyone may compute a graph over a commons' public sources while only the commons operates its own graph and releases its runs, and a coupling at a shared touchpoint counts as agreed only where both sides state it. | Observation needs no permission, operation is sovereign, and a one-sided claim of a coupling stays visible as a claim. | register |
| R18 | MUST | A graph across commons holds of their observations only aggregates over at least five commons, each by its own opt-in per source, naming its count, its threshold, a digest of the member revisions and the union of its members' withheld findings, never its members, computed from each member at its cut under its grant without copying a member's source, while down-coupling public patterns needs nothing beyond the installed release. | Local detail stays local and only aggregation flows upward; an aggregate that hides a blind member reports health where it means blindness, and a copy would be the second truth at the scale of many commons. | crossing |
| R22 | MUST | When the graph outgrows its CORE, `graph/` becomes the root of a repository of its own, `[commons].graph`, with the same layout, ids and contracts, and the CORE names its location. | Moving from a directory to a repository changes a location, never a record. | layout |
| R24 | MUST | A caller is served a computed edge only where it may see both ends and every restriction of every input the edge rests on, taken from the register as it is now, and never where an input has left the register or the grant of its run has been withdrawn. | Immutable provenance is not perpetual access; what a run was allowed to read decides nothing about who may see its result today. | answer |
| R25 | MUST | A claim that an aggregate, an extract or a service discloses nothing beyond what it intends names the threat it is tested against, such as differencing by overlapping questions, reconstruction of the served graph from accumulated extracts and their outward ids, or a public pair of endpoints carrying a relation derived from restricted evidence, and stays recorded as unqualified until that test has passed. | Thresholds and link limits are conditions, not proofs; an untested promise of non-disclosure is the most dangerous kind. | review |
| R26 | MUST | A resolution is computed from single-level bills and never stored: from a CORE's bill (`core` R37), through a release's record to the bill of the CORE it was made in (`library` R3), and through a line that reads another CORE to that CORE's bill under its grant (R17), each level naming what it was read from and a level not read its reason (R13). | A bill stored over several levels is stale the moment a part below it changes. | resolution |
| R27 | MUST | Where-used is the resolution read backwards over the bills its caller may read: a commons' own bill is a source of the kind `bill` with its class, another commons' only under its grant (R17), and across commons without a grant only an aggregate of R18, which never names its commons; a bill it could not read is named with its reason (R13), never read as not using the part; a library learns where its releases are used only so (`library` R12). | Which commons holds which release is each commons' own knowledge. | where-used |

R9 is folded into R8, R10 into R5, R19, R20 and R21 into R18, and R23 into R17; R25 holds what `graph-engine` R17 said of an extract, and R4 what `graph-engine` R10 said of a run. None of these ids is reused.

## 5 · Structure

The schema is `schemas/graph.schema.json`. Its root is `graph/sources.yml`; its `$defs` hold `source`, `answer` and `aggregate`. The run package has its own schema in `graph-engine`.

```
graph/
  sources.yml          the register; the commons writes it
  runs/<run>/          one run package (graph-engine); only the Graph Engine writes here
```

| Field of a register entry | Holds |
|---|---|
| `id` | the source's id in this graph, unique in the register |
| `kind` | an open word; part 6 says which kinds have a reader, and a permitted source of another kind is reported as not read |
| `ref` | an area or folder of the CORE, `owner/repo@rev[:path]`, or a reading's id |
| `class` | its visibility class (`public`, `member`, or one the commons defines) |
| `pin` | `lock` where the CORE's lock pins it; the run order resolves it there |
| `grant` | for a source of another commons: the decision event in that commons' CORE, withdrawn by no correction, whose `grant` names the source read and this commons as `recipient`; a CORE at hand is followed only so |
| `rhythm` | optional: when runs over it are due |

**Source kinds and what they state.** A node keeps the id of its specification; across commons it is `<core>/<id>`.

| Kind | `ref` | Nodes | Stated edges |
|---|---|---|---|
| `registry` | `registry/` | records as `<kind>:<slug>`, steps as `step:<stream>/<step>` (MODEL) | a record's bindings, each `<kind>:<slug>#<field>:<target>` (MODEL R22); a stream's `family` |
| `knowledge` | `knowledge/` | `source:<id>`, `claim:<id>` | a claim's `about`, `sources` and a derived claim's `inputs` (`core-knowledge`) |
| `operations` | `operations/` | `loop:<id>` | what a loop watches |
| `specs` | `specs/` | `<spec>#R<n>` | none of its own |
| `work` | a board, `owner/repo` | `work:<owner/repo#n>` | the six edges of `flow-graph` |
| `extension` | `extensions/<provider>/<pack>/` | offered records, qualified by provider and pack | an adopted record's origin |
| `patterns` | `patterns/<source>/`, `pin: lock` | `<source>/<id>` (CORE R30) | the index's `stated` links; `context.families`; an own pattern's `adopted_from` |
| `core` | `owner/repo@rev`, with `grant` | `<core>/<id>` | those of its own kinds |
| `fabric` | a reading's id | `reading:<id>` | the element it is read against |
| `bill` | `.commons/lock.yml`; the bill CORE generates, cut at the revision it names | `core:<id>`; each part by its identity (`core` R37); a release `<library>/<id>@<version>` | `uses`, with the line's usage; `part_of` a release; a release's `made_in` |
| `views` | `views/<name>/`, one entry per view with its audience's class (`core-views` R13); `views/blueprint.yml` | `view:<name>`; `section:<id>` (`core-views` part 5) | a view's `sections`; a curriculum's `after` (`learn` R2); a section's `binds` |

**The family join** (R14) is stated on both sides: a value stream's `family` in the registry, and `vsf:<family>` in a pattern's `context.families`. It needs no method.

**Ownership.** A file belongs to the source whose `ref` is the longest that contains it; two entries with the same `ref` are ambiguous and fail. **An answer** (`$defs/answer`) holds `question`, `cut` (each source with `rev`, or `read_at` where its working files differ from that commit, and `digest`), `runs` (the run ids used, foreign ones included), `method`, `candidates` (each with its id, its file and the edges it was reached by), and `silences`: `not_held` (targets no source holds), `unsighted` (whether anything was withheld, never what or how much) and `partial`, each entry `why` it was read only partly: `stale` with its source (moved on, or removed, since a run), `unread` with its source and reason, or `budget` with the count left out.

**An aggregate** (`$defs/aggregate`) holds `count`, `threshold`, `unsighted` (the union of its members' withheld findings) and `digest`, the hash over the member revisions; the members are kept in a protected record of whoever computes it.

## 6 · Checks

`tools/check_graph.py <core>` reads one CORE's graph and runs the checks of `graph` and `graph-engine`; the ids are unique across the two, and `--spec` reports one only. `tools/answer_graph.py <core> "<context and problem>"` is the reference answer path: one reader per source kind of part 5 (today `registry`, `knowledge`, `operations`, `views`, `specs`, `patterns` and `bill`; a kind without a reader is a gap), with `resolve` and `where_used` for R26 and R27, lexical matching across all sources, widened by stated edges, the family join first, and by the computed edges of the runs it names. Its answer validates against `$defs/answer`.

| Check | Tests |
|---|---|
| `layout` | `graph/sources.yml` exists and validates; `graph/` holds only the register and `runs/`; a CORE without `graph/` is a gap (R1, R22) |
| `register` | ids are unique and no two entries claim the same files; every kind with a reader resolves its `ref`, a kind without one is a gap; `pin: lock` names an entry the lock records, whose record has the lock's digest, whose files have the part digest that record names and whose index has the digest that record names, and repeats none of its fields; a `core` source names its grant (R2, R3, R17) |
| `untouched` | no source file holds a `run` id of this graph or a garden block (R4) |
| `nodes` | every endpoint of a run's edges is a node of a source in that run's cut, read at the revision the cut records; where that revision cannot be read and the files have moved on, a gap (R5) |
| `stated` | the stated edges of every source resolve, or are a gap where the target is not held yet; none is stored in `graph/` (R6) |
| `computed` | every computed edge names its run, method, kind and sources, a score its meaning, and no confidence; an edge carried by an installed extract keeps the `graph_run` its pinned record names; no endpoint is a grouping of a run (R5, R8) |
| `private` | `graph/` holds no e-mail address, no telephone number and no name of the party register (R11) |
| `answer` | the reference answer validates, reads or reports as not read every source, and without an own released run uses `stated-only` or `lexical`; asked again for `public` only, it shows no node, cut entry, finding or path of a source that is not public, and says that something was withheld (R12, R13, R14, R24) |
| `crossing` | an aggregate validates, so that it names count, threshold, its members' withheld findings and digest and has no field for its members; below five commons it fails. Differencing is not tested here (R18, R25) |
| `resolution` | a `bill` source is read only where CORE generates the bill; every level names what it was read from, a release's record the lock's digest; a level not at hand is a gap (R26) |
| `where-used` | every line of the bill is found where it is used; for `public` only, a bill of another class shows nothing and says it was withheld; a CORE whose bill is not read is named with its reason, only to a caller who may see it (R27) |
| `review` | a reading by the human accountable, or by an agent that has only this file, of R7, R15, R16, R17, R18 and R25 |

## 7 · Example

**Minimal:** a commons just founded, with no run yet. Its `graph/sources.yml`:

```yaml
sources:
  - {id: registry,  kind: registry,  ref: registry/,  class: member}
  - {id: knowledge, kind: knowledge, ref: knowledge/, class: member}
```

Its answers are `stated-only` or `lexical`, over its registry and its knowledge.

**Complete:** [the tool library's graph](examples/graph/tool-library.core/graph/sources.yml), which `check_graph.py` reads with 0 fail. Its sources are its registry, its knowledge, its own patterns and an installed extract that carries its library's run `federation-2026-11-01`; `graph/runs/` holds one released lexical run of its own. Asked *"tools come back damaged: who takes care of repair, and would a deposit help"*, the reference answer finds the capability `tool-care`, reaches *Sharing Tools Across Households* through the family join (`tool-care`, the step `lending/take-back`, `lending`, `demand-to-fulfillment`), and reaches *Reciprocity Sustains Cooperation* by an edge of the commons' own run, which it names with its cut and its method `lexical`.

**Where-used:** [the garden](tools/tests/core/good/bill.core/.commons/commons.yml) and an orchard that installs the same release and reads the garden under a grant, as `tests/graph` builds them. Where-used of `commons-library/garden@0.1.0` names both; for `public` only it names neither and says something was withheld; once the garden fails its checks, it has no bill, and where-used names it as not read, with the reason. The orchard's resolution reaches the garden's bill.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | The basic structure of any `[commons].graph`; the federation's graph is one instance of it | Holger, cloudsters/cloudsters.o#41, comment 6424270832; commons.o#93 |
| 2026-10-27 | revised | One holistic graph over a growing set of sources, never writing into patterns; fractal; a source register and an engine in a rhythm, no model required; answers from the commons' own graph; outward ids only, at most five | Holger, commons.o#93, comments 6438392453, 6438662161, 6438807424, 6441896539; commons.o#95, comment 6438865831 |
| 2026-10-28 | revised | G3: the run package (`graph-engine`); G4: `graph/` as an area beside `knowledge/`, promotable to `[commons].graph`, under the storage table | Holger, commons.o#93, comment 6464338661 |
| 2026-10-28 | reviewed | R7, R15, R16, R20, R21, R23 and R25, with every other requirement, read at `196f7e2`: they hold; R19's extra numbers recommended for deferral | the EA, commons.o#93, comment 6468528889 |
| 2026-10-28 | adopted | Adopted at `196f7e2`, within the boundary the EA named: the specification, its schema and the fixture-qualified reader and gate; the Graph Engine, `model` and `emulation`, hosted execution, MCP serving and the threats of R25 stay unqualified | Holger, commons.o#93, comment 6468689596 |
| 2026-10-28 | revised | R19: the extra numbers (three independent source families, no commons above half) deferred until their purpose and effect are shown; the union of members' withheld findings kept | Holger, commons.o#93, comment 6468689596 |
| 2026-10-28 | revised | **Adopted 29 October 2026 ([commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412)).** KISS: the aggregation block one requirement with its threshold (R18, from R18–R21); computed edges one rule, a library's run named neutrally (R8, from R8 and R9); R10 into R5; R23 into R17; R25 holding the extract's threats from `graph-engine` R17; `graph-engine` R10 into R4; three silences, `not_held`, `unsighted` and `partial` (R13); a cut read at its time, `read_at` for `observed` (R12; D0, commons.o#99); the ids of folded rules retired, never reused (SPECIFICATION R7) | Holger, commons.o#98 (*"Ja, alle"*) |
| 2026-10-29 | revised | An installed extract is read through its pinned record: the lock entry is `{path, origin, record}`, the record `release.yml` beside the index has the lock's digest, and the index's digest and the released `graph_run` come from that record (R12; the checks `register` and `computed`), as CORE R29 now pins it | D1-CE on the EA's read of commons.o#98 |
| 2026-10-29 | revised | An installed extract is read only where its files have the part digest its pinned record names, the one digest of a copy LIBRARY's check computes, so that a body changed after install is not read and the extract is reported unread, never served as the release (R12; the check `register`; MCP R18) | the EA, commons.o#94, comment 6503716689 |
| 2026-10-29 | adopted | Adopted 29 October 2026 | Holger, [commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412) |
| 2026-10-29 | revised | The source kind `views` (R3, part 5): a view is the node `view:<name>`, a blueprint section `section:<id>`, with the stated edges `sections`, `after` and `binds`, each view its own entry with its audience's class, so that a learner reaches a curriculum's next path through the one read path GRAPH and MCP already have, MCP serving only what GRAPH holds; with commons.o#105, which names the ids in `core-views` part 5. Adopted 29 October 2026 ([commons.o#92, comment 6509201761](https://github.com/Commons-Engineering/commons.o/issues/92#issuecomment-6509201761)) | D2-CE's demonstration, commons.o#92, comment 6505909477; D1-CE on the ids |
| 2026-10-29 | adopted | Adopted 29 October 2026 | Holger, [commons.o#92, comment 6509201761](https://github.com/Commons-Engineering/commons.o/issues/92#issuecomment-6509201761) |
| 2026-10-30 | revised | Step 2 of the bill of materials: resolution from single-level bills (R26); where-used read backwards, a commons' bill one source row, across commons only by grant or aggregate (R27); the checks `resolution` and `where-used`. Adopted 30 October 2026 ([commons.o#107, comment 6521463793](https://github.com/Commons-Engineering/commons.o/issues/107#issuecomment-6521463793)) | Holger, commons.o#107 (step 1 adopted, comment 6519835234; D4-CE's reading, comment 6516687963) |
| 2026-10-30 | revised | Where-used names each CORE whose bill it could not read, with its reason, so that a commons not known, such as one whose checks fail on a doubtful release, is never read as one that does not use the part (R27; the check `where-used`). Adopted 30 October 2026 ([commons.o#107, comment 6521463793](https://github.com/Commons-Engineering/commons.o/issues/107#issuecomment-6521463793)) | the Office, commons.o#107 |
| 2026-10-30 | adopted | Adopted 30 October 2026 | Holger, [commons.o#107, comment 6521463793](https://github.com/Commons-Engineering/commons.o/issues/107#issuecomment-6521463793) |
| 2026-10-30 | revised | The EA's reading of step 2, in the reference code and its tests, no requirement changed: visibility is decided before an unread CORE is named, also where its register names no bill; where-used walks the permitted resolution backwards, through the COREs a commons reads, with the path, the revision of every step, cycles and the levels not read; an adopted line without a record says that its release is not followed (R26, R27). Adopted 30 October 2026 ([commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766)) | the EA, commons.o#107, comment 6522100364; Holger, comment 6522699919 |
| 2026-10-30 | adopted | Adopted 30 October 2026 | Holger, [commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766) |
| 2026-10-30 | revised | The EA's second reading of step 2, no requirement changed: a CORE at hand is followed only under the grant of R17, a decision event of that CORE naming its bill and the reading commons; a grant missing, unresolved, withdrawn or out of scope stops that level with its reason, which shows only where the caller may see the reading commons' bill (R17, R26, R27; the field `grant`). Adopted 31 October 2026 ([commons.o#98, comment 6543679246](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6543679246)) | the EA, commons.o#107, comment 6531759311 |
| 2026-10-31 | adopted | Adopted 31 October 2026 | Holger, [commons.o#98, comment 6543679246](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6543679246) |

What this specification supersedes, and what it carries of it, is in [`carry-over/graph.md`](carry-over/graph.md).
