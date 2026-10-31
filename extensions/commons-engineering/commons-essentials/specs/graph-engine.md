---
id: graph-engine
title: Commons GRAPH — the Graph Engine
status: decided
lang: en
touches: [specification, graph, core, core-knowledge, library, library-patterns, mcp]
terms: [commons, graph, pattern, orbit, visibility-class, garden, mcp]
schema: schemas/graph-engine.schema.json
check: tools/check_graph.py
supersedes:
  - Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/PATTERN_PIPELINE_SPEC.md
  - Commons-Engineering/commons-graph@main:README.md
---

# Commons GRAPH — the Graph Engine

*A run order goes in, one run package comes out, and nothing else is written.*

## 1 · Goal

A computed edge is only as good as what it was computed from, and a computation nobody can retrace is a claim nobody can check. A run of the Graph Engine therefore takes a run order that names its source cut, its method and its policy, and delivers one run package into `graph/runs/` of the one CORE it runs for, without writing into any source. Every attempt keeps its record; a run is released only when a deterministic gate passes and the commons gives its word; and what it computed inherits the restrictions of what it read. This specification decides one thing for its reader: **whether a run's result can be released and relied on**: what it read, how, where and under whose grant, and that it changed nothing it read. How the engine is built, hosted, budgeted and tested is its own repository's.

## 2 · Boundary

**Belongs here:** the run order; the run package; the states of a run; the gate of a run; storage of a run's record and outputs.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| the register, nodes, stated edges, answers, graphs across commons, and claims of non-disclosure | `graph` |
| that a run never writes into a source, and its proposals go to the workshop | `graph` (R4) |
| where an installed extract sits and what its lock entry records | `core` |
| what a reading inherits from its inputs, in general | `core-knowledge` |
| the extract, its index and its release | `library`, `library-patterns` |
| serving a run's result to a caller | `mcp` |
| the engine's repository, identity, budget, checkpoints, golden runs and hosting | the Graph Engine's own repository |

**Touches** `specification`, `graph`, `core`, `core-knowledge`, `library`, `library-patterns` and `mcp`. **Rests on** Holger's decision of 28 October 2026 on G3 and G4 (commons.o#93, comment 6464338661), his word that no model is required (6438807424), that a graph never writes into patterns (commons.o#95, comment 6438391848), G1 (6438865831), and the KISS pass (commons.o#98).

## 3 · Terms

All terms resolve in the glossary. This specification adds none.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | A run is computed only from its run order, which names the source cut, each register entry resolved to `ref@rev` or to a reading's id with the time it was read and its digest, the method, the policy and the parent run, and the engine reads nothing outside that cut. | A source's location is not its snapshot, and what was not named cannot be retraced. | order |
| R2 | MUST | The method names its kind, one of `model`, `lexical` and `stated-only`, its procedure and version, its parameters and the versions of every model and tool it uses, and no machine-learning model is required for any graph. | A pinned model alone does not repeat a result, and a small commons computes with words and stated joins. | order |
| R3 | MUST | The policy takes each input's class from the register and never lowers it, names the grant with its source, purpose and recipient and where the run takes place, and an input whose class is not `public` reaches a hosted method only under a decision event of the CORE whose structured `grant` covers that source, purpose and recipient and that no correction has withdrawn, while a decision without that scope verifies nothing. | A hosted method is a further recipient; a run that declares its own classes, or points at any decision, could send anything anywhere. | order |
| R4 | MUST | A run delivers exactly one package in `graph/runs/<run>/` of the one CORE it runs for, made of `run.yml`, `edges.jsonl` with computed edges only and `proposals.yml`, writes nothing else, and from `computed` on records both outputs, which a released run holds or resolves at a recorded location. | One result per run, in one place, is what can be checked, compared and released; a released run with no results releases nothing. | package |
| R5 | MUST | `run.yml` records the order as resolved, every change of state with its time, the findings, the engine's version and the digest of every output, and, for an output not held in git, its durable location. | A run is retraced from its record, whatever happened to its outputs. | package |
| R6 | MUST | A run begins `ordered`, becomes `computed`, then `released` or `failed`, and a released run may become `superseded`, by these transitions only, keeping its `run.yml` in every state; a record of an earlier form is read with `computing` and `paused` as steps before `computed`, `checked` as a step before `released` and `rejected` as `failed`. | Interrupted and rejected attempts are what a commons learns from; a released record never changes, so an older one is read, never rewritten. | states |
| R7 | MUST | A run is `released` only when every endpoint of its edges is a node of a source in its own cut, read at the revision the cut records, every input its edges rest on resolves as a file or a node of its source in that cut, every edge carries the restrictions of all its inputs and every source's digest is the same as before the run, and only on the commons' word, recorded in its `run.yml` with who gave it and where; its record and package never change after it was first released except that `superseded` may be appended, by a later run that names it as its parent. | The gate is deterministic and judges the run by what it read, never by today's graph; a version of the graph is a released run, and a release whose order, method or approval can be rewritten proves nothing. | checked |
| R9 | MUST | A computed edge and a proposal carry every restriction of every input they rest on, as the set of the inputs' classes other than `public`, so that one restriction never stands in for another, and releasing a run makes no input public. | Derivation must not launder what a reader may not see, and classes defined by a commons cannot be ranked by their names. | checked |
| R12 | MUST | A result is reused only where its key, over every input's digest, the engine that runs it, the method with its procedure, version, parameters, models and tools, and the policy, is the same. | A changed implementation, procedure, parameter or policy must never inherit an old result. | package |
| R14 | MUST | A run reproduces its edges from its recorded order. | A result that cannot be repeated from its record is known only by trust. | review |
| R15 | MUST | The register and every `run.yml` are committed, the edges and proposals of a released run are committed at the small tier and, when they grow, kept in a durable store whose location and digest `run.yml` records, and caches are never committed. | Storage grows with scale while the record stays in git. | storage |
| R19 | MUST | An item that takes in or declines a proposal of a run names it in its first line as `run: <run> · proposal: <n>`, and no second item is opened for that proposal. | A released run never changes, so the decision on its proposal lives in the item, and only a named proposal can be joined to its decision, and the model's history held against what followed (`core-knowledge` R16). | review |
| R20 | MUST | A run whose output leaves its commons, as an aggregate or an extract, reads no correction by the commons' own people whose `release` does not name that use, whatever the source's opt-in. | An opt-in covers a whole source, and a correction given in confidence is used for no other picture without its giver's release (`core-knowledge` R18). | checked |

R8 is folded into R7; R10 moved to `graph` R4, R16 to `library-patterns` R17 and R17 to `graph` R25; R11 and R13 belong to the engine's own repository, and R18 is cut. None of these ids is reused.

## 5 · Structure

The schema is `schemas/graph-engine.schema.json`. Its root is `run.yml`; its `$defs` hold `edge`, a line of `edges.jsonl`, and `proposal`, an entry of `proposals.yml`.

| Field of `run.yml` | Holds |
|---|---|
| `id`, `engine`, `key` | the run's id; the engine as `owner/repo@rev`; the reuse key, `sha256:` over the cut's sources and digests, the engine, the method and the policy (R12) |
| `cut` | each source of the register with `rev` (or `read_at`) and `digest`, `pin: lock` resolved; a released run another graph's source carries, as `run` |
| `method` | `kind`, `procedure` (`id@version`), `params`, `models`, `tools` |
| `policy` | `classes` per source, as the register holds them; `grant` (`source`, `purpose`, `recipient`, and `where`: the decision event `lifecycle/events/<id>.yml`, whose own field `grant: {source, purpose, recipient}` states the scope the commons decided); `where` (`local` or the hosted recipient) |
| `parent` | the run it continues or supersedes, or `null` |
| `states` | each `{state, at}`, in order; `released` with `by` and `where`; `superseded` with `by`, the later run |
| `findings` | what the run found |
| `outputs` | per file its `digest` and, where not committed, its `location` |
| `aggregates` | for a run across commons, its aggregates in the form of `graph` part 5 |

| Field of an edge (`edges.jsonl`) | Holds |
|---|---|
| `from`, `to` | two nodes of the cut (`graph` part 5) |
| `kind` | the relation proposed, or `unclassified` |
| `run`, `method` | the run's id; the method's kind |
| `score`, `score_is` | a number and what it measures; never a confidence |
| `rests_on` | `<source>:<path or node id>` for each input it was computed from, each resolving as a file or node of that source in the cut |
| `class` | `public`, one class, or the sorted list of every restriction of its inputs (R9) |

A proposal has `source`, `node`, `field`, `target`, the `edge` it rests on (`edges.jsonl:<line>`), its `class` (that of its edge and its source) and its `state` (`open`, `taken`, `declined`).

## 6 · Checks

`tools/check_graph.py <core>` runs these checks together with those of `graph`, on every package in `graph/runs/`.

| Check | Tests |
|---|---|
| `order` | `run.yml` validates; its classes are the register's; an input not `public`, with a place other than `local`, needs a decision event of the CORE whose `grant` covers its restricted sources, purpose and recipient: no event or a scope that does not cover the run fails, a decision without a structured `grant` is a gap whose edges are not served, and a grant a correction has withdrawn is a should (R1, R2, R3) |
| `package` | the package holds its three files and nothing else; from `computed` on both outputs are recorded, each present with its digest or at a location, which is a gap for a released run until restored; its key is that of its cut, method and policy; every proposal validates (R4, R5, R12) |
| `states` | every transition is one of R6's, an earlier record read as R6 says; `released` names who gave the word and where it is recorded; `superseded` names a run whose parent it is; in git, the record is the one first released in every field but `states`, its states only gain `superseded`, and its outputs are those first released (R6, R7) |
| `checked` | every input an edge rests on resolves as a file or node of its source in the cut, unverified where that snapshot is; a released run's every edge carries the restrictions of all its inputs and ends, and every proposal those of its edge and source; a run with aggregates rests on no correction whose `release` does not name the run, while an extract's extractor is not built to check the same (R7, R9, R20) |
| `intact` | in git: every source of the cut has, at its recorded revision, the digest the run recorded, and the commits that brought the package change nothing else in the CORE; outside git, or at a revision that cannot be read, unverified (R7; `graph` R4) |
| `storage` | no embedding or cache is committed in `graph/`; an attempt not released that keeps its edges is a should (R15) |
| `review` | a reading by the human accountable, or by an agent that has only this file, of R14 and R19 |

## 7 · Example

**Minimal:** a run just ordered, over a commons' registry alone. Its `run.yml`:

```yaml
id: tool-library-2026-11-01
engine: Commons-Engineering/graph-engine@v0.1.0
cut:
  - {source: registry, rev: 020a5f9efacb6531a49f862b5a5b995b3f85bc15, digest: "sha256:3d443a646c2a4c353565a59aff704b4f034cd56eb9bfe11ffd90069c99d713e9"}
method: {kind: stated-only, procedure: family-join@1}
policy: {classes: {registry: member}, where: local}
parent: null
states:
  - {state: ordered, at: "2026-11-01T08:00:00Z"}
outputs: {}
```

**Complete:** [the tool library's released lexical run](examples/graph/tool-library.core/graph/runs/tool-library-2026-11-02/run.yml), committed alone after its sources so that `intact` can read them at the recorded revision. Its cut holds the registry, the knowledge and the own patterns at that revision and the installed extract with its library's run `federation-2026-11-01`. It delivers three computed edges, each `member` because each rests on a `member` input, and two open proposals, each with its class; its key is that of its cut, method and policy; its record is of the earlier form, with `computing` and `checked`, and is read as R6 says. `check_graph.py` reads it with 0 fail.

**Not qualified here:** the Graph Engine itself, which is not built yet, the method `model`, hosted computation and serving through the MCP. The fixtures qualify the reader and the gate, nothing more.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-28 | commissioned | G3: the Graph Engine's result is one package per run (`run.yml`, `edges.jsonl` with computed edges only, `proposals.yml`, an extract for released runs only), with the run states, isolation like the Model Engine's, budget, checkpoints and golden runs; G4: the storage table | Holger, commons.o#93, comment 6464338661 |
| 2026-10-28 | reviewed | R11, R13, R14, R16, R17 and R18, with every other requirement, read at `196f7e2`: they hold within the reader and gate; the engine, hosted execution and R17's threats remain to be qualified | the EA, commons.o#93, comment 6468528889 |
| 2026-10-28 | adopted | Adopted at `196f7e2`, within the boundary the EA named: the specification, its schema and the fixture-qualified gate; the Graph Engine itself, `model` and `emulation`, hosted execution and the threats of R17 stay unqualified | Holger, commons.o#93, comment 6468689596 |
| 2026-10-28 | revised | **Adopted 29 October 2026 ([commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412)).** KISS: five states, a record of an earlier form read rather than rewritten (R6); `checked` folded into release (R7, from R7 and R8); `emulation` dropped; the engine's identity, budget, checkpoints, golden runs and hosting to its own repository (R11, R13, part of R12 and R15); R10 to `graph` R4; the extract (R16) to `library-patterns` R17 and its threats (R17) to `graph` R25; the rhythm (R18) cut; the Model Engine table removed. With LEARN: R19 names the proposal an item decides, R20 keeps a correction without release out of a run that leaves the commons; the ids of folded rules retired, never reused (SPECIFICATION R7) | Holger, commons.o#98 (*"Ja, alle"*); commons.o#92, 6473039584 |
| 2026-10-29 | adopted | Adopted 29 October 2026 | Holger, [commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412) |

What this specification supersedes, and what it carries of it, is in [`carry-over/graph-engine.md`](carry-over/graph-engine.md).
