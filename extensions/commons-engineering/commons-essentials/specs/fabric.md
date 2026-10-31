---
id: fabric
title: Commons FABRIC
status: decided
lang: en
touches: [specification, core, core-knowledge, model, graph, extension, mcp, flow-bodies]
terms: [fabric, reading, commons, commons-core, graph, visibility-class, mcp]
schema: schemas/fabric.schema.json
check: tools/check_fabric.py
supersedes:
  - Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_SYSTEMS_MANIFEST.md
---

# Commons FABRIC

*What a commons senses from its own systems of record: a reading, never a record.*

## 1 · Goal

A commons' model says what it is heading for; its operational reality is kept elsewhere, in the systems of record it runs: its ledger, its bookings, its roster, its sensors. Without reading them, a model can agree with itself and never learn how far it is from what is. The Fabric is the commons' sensor: it reads its own systems, under access the commons gives, against elements of its model, and keeps of each reading only what was measured, when, as whom and against what, while the records stay where they are kept. This specification decides one thing for its reader: **whether what a commons took in from its systems of record can be relied on as a reading**, meaning it names its system, its query, its time and its access, is held to the element it was read against, carries no record and no person, and enters the commons only where a reading may.

## 2 · Boundary

**Belongs here:** the register of the systems a commons reads; a reading and its fields; what a reading may hold and what stays in a system; the access a reading is taken under; the area `fabric/`.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| a reading as a source of the graph, its node and its edge | `graph` (R3) |
| a claim that rests on a reading, its kind and standing; expectations beside what followed | `core-knowledge` (R3, R14, R16) |
| the elements a reading is read against | `model` |
| serving readings to callers, and grants | `mcp` |
| a domain's mapping of its systems to its model, offered as served depth | `extension` |
| what a commons does about a difference | `flow`: an item, decided by a person |
| connectors, their code, hosting and credentials | the commons that runs them |

**Touches** `specification`, `core`, `core-knowledge`, `model`, `graph`, `extension` and `mcp`. **Rests on** Holger's words: FABRIC specified next (commons.o#94, comment 6474207150), by D4-CE with D1-CE, as a component beside `core`, `graph`, `mcp` and `library` (commons.o#99; named a component, no longer a container, commons.o#100, comment 6497129609); the frame of interlocking loops, the Fabric taking signals in (commons.o#94, comment 6436299151); the KISS pass (commons.o#98); and one word, one meaning, `reading` for what the Fabric senses (commons.o#99, 6474472957).

## 3 · Terms

All terms resolve in the glossary. *System of record* and *query* keep their ordinary meaning, made precise by part 5.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | A commons' Fabric is the area `fabric/` of its CORE, with its register `fabric/systems.yml`, which the commons writes, and its readings in `fabric/readings/`, and when it outgrows its CORE it becomes the repository `[commons].fabric` with the same layout, named in the CORE's `locations` (`core` R7). | One place for what the commons senses, beside what it holds; moving it changes a location, never a reading. | layout |
| R2 | MUST | Every system of record the Fabric reads is one entry of the register with its id, its kind, who holds it, the access it is read under, named by reference and never by its secret, the visibility class of what it yields, and each query it may run with the address of the element it is read against (`model` R18), and no system, no query and no address short of ratified is read; a query by which a reading was taken keeps its address and what it yields and stays in the register while a reading names it, a new meaning being a new query. | What is read, from where and as whom must be known before anything is read; an unregistered query is a leak nobody chose; and a query whose meaning changed under its id would reinterpret every reading taken by it. | systems |
| R3 | MUST | The Fabric only reads: it writes into no system of record and acts on none, nothing of a system's records, persons, raw responses or credentials leaves that system, and what it keeps is the reading; an action on a system of record is the work of the Solution responsible for it, under the mandate it serves in (`flow-bodies` R21). | The model must never become a system of record, the records of a commons stay where they are kept and governed, and one job has one mechanism: a governed action has its accountable Body, a sensor has none. | review |
| R4 | MUST | A reading is one file `fabric/readings/<id>.yml` with its id `reading:<id>`, its system, its query, the time it was read, the access it was taken under, the element its query's address names, and its result as a value with its unit and period or as a signal, never a row of a system's records and never a person. | The same figure read under two accesses is two measurements, and a figure without its period is a different figure (`core-knowledge` R14). | readings |
| R5 | MUST | A reading never changes after it was taken and is never removed; a later reading of the same query is a reading of its own, and a reading withdrawn by the commons leaves its id and the reason in its place. | The history of readings is how drift is seen; a reading rewritten cannot show it. | readings |
| R6 | MUST | A reading is as restricted as the class of its system, a claim or expectation resting on a reading carries that restriction (`core-knowledge` R8), and a query whose result would name a person or carry a record is refused before it runs. | What a commons senses about its people and its records must not travel further than what it may say of them. | readings |
| R7 | MUST | A reading reaches the rest of the commons only as a source of its graph (`graph` R3) and as the source of a claim of kind `measure` or `signal` (`core-knowledge` R3), and never as a record of the registry, and what it feeds beyond its claim is what that claim may feed (`core-knowledge` R8, R9). | A sensed value informs the model; it does not become the model, and it reaches an expectation only as evidence does. | review |
| R8 | MUST | A reading is held beside the record it was read against and never changes it, a difference between them is an item decided by a person, and how readings met expectations is read as `core-knowledge` R16 says. | The record is the commons' reference, the near future it heads for (`core` R9), and a sensor that rewrites it is a thermostat that sets its own target; an expectation is a prediction, met or missed, and that is calibration. | review |
| R9 | MUST | The access a system is read under is the least it grants for its queries, read-only, given and withdrawn by the commons, and its withdrawal stops every query while the readings already taken stay as they were read. | A commons owns its systems and decides who reads them; what was read is history, not a standing permission. | systems |

## 5 · Structure

The schema is `schemas/fabric.schema.json`. Its root is `fabric/systems.yml`; its `$defs` hold `reading`.

```
fabric/
  systems.yml          the register of the systems read; the commons writes it
  readings/<id>.yml    one reading each; never changed after it was taken
```

| Field of a system | Holds |
|---|---|
| `id`, `kind` | the system's id in this register; what it is, an open word (`ledger`, `booking`, `roster`, `sensor`, `crm` …) |
| `holder` | who holds the system: the commons, or another party that gives it access |
| `access` | the access it is read under, by reference to where the commons keeps it (a secret store's entry, a key's name), never the secret |
| `class` | the visibility class of what it yields (`graph` part 5) |
| `queries` | each `{id, about, yields}`: the query's id, the address of the element it is read against (`model` R18: `to` as kind and slug, `weight`, `status`, `source`; a query the commons writes is `ratified` and `human`), and what it yields: a `measure` by its name with its `unit`, a count being a measure with the unit `count`, or a `signal` |

| Field of a reading | Holds |
|---|---|
| `id` | `reading:<id>`, stable, the file's name |
| `system`, `query` | the system and the query it was taken by |
| `read_at`, `as` | when it was read; the access it was taken under |
| `about` | the element its query's address names, `{kind, slug}` |
| `result` | `{value, unit, period}` or `{signal}` |
| `withdrawn` | where the commons withdrew it: `{at, reason}`, and no result |

**In the graph** (`graph` part 5) a reading is a source of kind `fabric`, its node `reading:<id>`, with one stated edge `about` to its element. **In `knowledge/`** a claim of kind `measure` or `signal` names it as a source; a mapping a domain offers in its extension's served `sor/` may help a commons write its queries, and the queries remain its own.

## 6 · Checks

`tools/check_fabric.py <core>` reads a CORE's `fabric/`. It reports **fail**, **should** or **gap**, and exits with 1 only on a fail.

| Check | Tests |
|---|---|
| `layout` | `fabric/`, or the place `locations` moves it to, holds only `systems.yml` and `readings/`; one moved to another repository is checked there; a CORE without a Fabric is a gap, unless git held a reading of it, whose loss fails `readings` (R1, R5) |
| `systems` | `systems.yml` validates; ids are unique, every query's id is unique within its system, and every `about` is an address as MODEL R24 reads it: a target the grammar cannot hold fails, one the registry does not hold yet is a gap, and one short of `ratified` is not read and fails; no `access` holds what looks like a secret; in git, a query a reading was taken by has the address and yields it had then (R2, R9) |
| `readings` | every reading validates, is named by its id, and names a system and a query of the register and that query's `about`; its result is of the kind the query yields, with the query's unit and a period for a measure; it holds no e-mail address, telephone number or name of the party register; in git, a reading is as it was first committed, is read against its query as the register held it then, one that left names its withdrawal, and none git ever held is gone, a declared move followed (R1, R4, R5, R6) |
| `review` | a reading by the human accountable, or by an agent that has only this file, of R3, R7 and R8 |

**Not built yet** (R27): the area in CORE R5 and its structure key `fabric`, which `core` gains on FABRIC's adoption; connectors that take readings from systems, and the refusal of a query before it runs (R6), which is a connector's; a source kind `fabric` with a reader in `answer_graph.py`, so that GRAPH reports readings as not read until it has one; the qualification of readings served through the MCP.

## 7 · Example

**Minimal:** a tool library that reads its loan ledger, and one reading:

```yaml
systems:
  - id: loan-ledger
    kind: ledger
    holder: the tool library
    access: "secret-store:tool-library/loan-ledger-read"
    class: member
    queries:
      - id: returned-damaged
        about: {from: "fabric/systems.yml#loan-ledger/returned-damaged", to: {kind: capability, slug: tool-care}, weight: 1.0, status: ratified, source: human}
        yields: {measure: returned damaged, unit: share of returns}
```

and `fabric/readings/2026-11-loan-ledger-returned-damaged.yml`:

```
id: "reading:2026-11-loan-ledger-returned-damaged"
system: loan-ledger
query: returned-damaged
read_at: "2026-12-01T06:00:00Z"
as: "secret-store:tool-library/loan-ledger-read"
about: {kind: capability, slug: tool-care}
result: {value: 0.12, unit: share of returns, period: 2026-11}
```

**Complete:** [the tool library's Fabric](tools/tests/fabric/good/tool-library.core/fabric/systems.yml), two systems and three readings, one withdrawn; `check_fabric.py` reads it with 0 fail.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-28 | commissioned | Commons FABRIC: how a commons reads its own operational reality, a reading never a record, a container beside core, graph, mcp and library; by D4-CE with D1-CE | Holger, commons.o#94, comment 6474207150; commons.o#99 |
| 2026-10-29 | revised | The EA's two counterexamples: a reading taken is never removed, a deletion in the working files or by a commit failing (R5); a query keeps its address and what it yields once a reading was taken by it, a new meaning being a new query, and a reading is checked against its query as it was when taken (R2, R5). Adopted 29 October 2026 ([commons.o#99, comment 6509201179](https://github.com/Commons-Engineering/commons.o/issues/99#issuecomment-6509201179)) | the EA, commons.o#99, comment 6501096955 |
| 2026-10-29 | revised | F1 decided as proposed: FABRIC reads only, and an action on a system of record is the work of the responsible Solution under its FLOW mandate (R3); the older write-exception clauses are retired, not kept elsewhere (carry-over). Adopted 29 October 2026 ([commons.o#99, comment 6509201179](https://github.com/Commons-Engineering/commons.o/issues/99#issuecomment-6509201179)) | Holger, commons.o#99, comment 6501928492 |
| 2026-10-28 | revised | D1's co-read: the record as the reference and calibration apart (R8); a reading feeds what its claim may feed (R7); a query's element as a MODEL address (R2); a result's value apart from the measure's name (R4); the move by CORE's `locations` (R1); restriction carried into claims (R6). D0's glossary: `fabric` part of the CORE, keeping readings | commons.o#99, comments 6476245514 and 6476238963 |
| 2026-10-29 | revised | An established Fabric cannot disappear: before a CORE without a Fabric is reported as the initial gap, git's history is read, and every reading it held and the Fabric no longer holds fails; a move declared in `locations` is followed, to a folder of the CORE through git, to another repository by checking it there (R1, R5; checks `layout`, `readings`). Adopted 29 October 2026 ([commons.o#99, comment 6509201179](https://github.com/Commons-Engineering/commons.o/issues/99#issuecomment-6509201179)) | the EA, commons.o#99, comment 6503717209 |
| 2026-10-29 | revised | The glossary aligned with D0's component and practice: `fabric` is the term Commons FABRIC, a component (`is_a: component`), as CORE, LIBRARY, GRAPH and MCP are; FABRIC is the practice of the same name. Adopted 29 October 2026 ([commons.o#99, comment 6509201179](https://github.com/Commons-Engineering/commons.o/issues/99#issuecomment-6509201179)) | Holger, commons.o#100, comment 6497129609 |
| 2026-10-29 | adopted | Adopted 29 October 2026 | Holger, [commons.o#99, comment 6509201179](https://github.com/Commons-Engineering/commons.o/issues/99#issuecomment-6509201179) |

What this specification supersedes, and what it carries of it, is in [`carry-over/fabric.md`](carry-over/fabric.md).
