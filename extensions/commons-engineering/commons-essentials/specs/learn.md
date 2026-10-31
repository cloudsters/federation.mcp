---
id: learn
title: Commons LEARN
status: decided
lang: en
touches: [specification, core, core-knowledge, core-views, model, graph, mcp]
terms: [commons, commons-core, pattern, specification]
schema: schemas/learn.schema.json
supersedes: []
---

# Commons LEARN

*What a commons offers so that anyone can learn its body of knowledge, with any agent.*

## 1 · Goal

A commons holds a body of knowledge: its model, its patterns, its specifications and its words. Anyone with access to the commons, directly or through its MCP, should be able to learn all of it, at their own level and in their own way, either by asking as questions arise or by following a curriculum. They bring an agent of their choice, which joins what the commons holds with the general knowledge of its own model. This specification states what a commons offers for that and what it keeps out. It decides one thing for its reader: **whether a commons can be learned**, by any learner with any agent, without the commons keeping anything about the learner and without the learner mistaking the agent's general knowledge for the commons'.

## 2 · Boundary

**Belongs here:** the body of knowledge as offered for learning; the curriculum as a view; the learner's state, which travels with a request; keeping the commons' knowledge apart from an agent's general knowledge.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| how a commons itself learns: evidence, standing, corrections by its people | `core-knowledge` |
| grants, the serving pipeline, `answer`, `node`, `propose`, the envelope, use records | `mcp` |
| how an answer is computed and what it says of its sources | `graph` |
| views, their definitions, build records and staleness | `core-views` |
| the agent file that orients any agent | `core` (R36) |
| a learner's knowledge state, progress and courses | the learner and their agent, outside every commons |

**Touches** `specification`, `core`, `core-knowledge`, `core-views`, `model`, `graph` and `mcp`. **Rests on** Holger's words of 28 October 2026: what LEARN is, any learner with any agent learning the body of knowledge ad hoc or by curriculum (commons.o#92, comment 6473604541); a commons keeps no learner's state (6472793436); and of 26 October 2026: a learning view that meets the learner's own background, differentiated within one definition rather than one content for all (6423094523).

## 3 · Terms

All terms resolve in the glossary. Two words are this specification's and enter the glossary with it, agreed with D0: **body of knowledge** (the model, patterns, specifications and glossary a commons holds) and **curriculum** (a view that orders the body of knowledge into paths).

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | A commons offers its body of knowledge to be learned through the same calls as any other use, `answer` and `node` of its MCP or its CORE read directly, within the reader's grant, and offers nothing for learning that the grant would not show otherwise. | Learning is reading with a purpose, not a second door with rules of its own. | review |
| R2 | MUST | A curriculum is a view of kind `curriculum` over the records the commons already holds, each such view one path whose sections are read in order and which names the paths it presupposes, generated and never a store or a copy of the content. | A course written beside the canon ages with it; one generated from the records follows every change. | schema |
| R3 | MUST | Learning by curriculum and learning by asking read the same body of knowledge, so that a curriculum adds order and prerequisites and no content of its own. | One body of knowledge, two ways in; a curriculum that says something the records do not would be a second truth. | review |
| R4 | MUST | The learner's state of knowledge travels with a request, brought by the learner's agent, and the commons uses it for that answer only and keeps nothing of it, in no cache, use record, item or view, and derives no profile from what was asked. | A commons is not a register of people's learning; the learner's state is the learner's (`mcp` R20, R21). | review |
| R5 | MUST | Everything a commons serves for learning carries its source and cut, and an agent that teaches from a commons shows the learner what comes from the commons, with its source, apart from what comes from its own model's general knowledge. | A learner must be able to tell the commons' knowledge from a fluent general answer, and the commons' words stay checkable against their source. | review |
| R6 | MUST | What a learner or their agent gives back, a question the body of knowledge could not answer or an error found in it, enters only as `propose` of the MCP (`mcp` R12), to the commons or, for an error in a release, to its maker, an item like any other, carrying nothing of the learner's state, and an agent's general knowledge never enters the commons as evidence. | The return of learning has the one door every proposal has, and a model's general answer is no source about this commons (`core-knowledge` R11). | review |

## 5 · Structure

The schema `schemas/learn.schema.json` decides a curriculum view: a view definition of `core-views` (R5) with kind `curriculum` and one further field, `after`, naming the paths it presupposes.

**What is offered, and how it is read:**

| Part of the body of knowledge | Held in | Read ad hoc | Read by curriculum |
|---|---|---|---|
| the model: elements, streams, capabilities | `registry/` (MODEL) | `node(id)`, `answer(question)` | sections that bind its nodes |
| what is known and how well | `knowledge/` (`core-knowledge`) | the same, within the grant | the same |
| patterns | the installed extension and extract (`core`, `graph`) | the same | the same |
| specifications and the glossary | `specs/` | the same, or read directly | the same |

**A path** is one view definition `views/<path>/view.yml` of kind `curriculum`. Its `sections` are blueprint sections (`core-views` R1), read in order; its `after` lists the paths a learner should have read first. Its `promise` says what the learner can do after it, and its `way_back` names `propose` (R6). The learner's agent chooses where to begin, from the learner's state, which it brings and the commons does not keep (R4). Different learners thus get different courses from one definition.

## 6 · Checks

| Check | Tests |
|---|---|
| `schema` | a curriculum view validates against `schemas/learn.schema.json` |
| `review` | a reading by the human accountable for this specification's mandate, or by an agent that has only this file, of R1 and R3–R6 |

**Gaps:** The MCP that R1, R4 and R6 rely on is specified in draft (`mcp`) and not implemented. No check yet tests that a cache or use record holds nothing of a learner's state beyond what `mcp` R20 and R21 test.

## 7 · Example

The tool library offers two paths. A new member starts with the first, and a keeper of the desk continues with the second:

```yaml
name: lending-basics
kind: curriculum
audience: anyone who wants to borrow or lend
promise: the learner can explain how lending works here and who carries it
way_back: a proposal through the library's MCP
sections:
- d0.perception-to-mandate
- d4.demand-to-fulfillment
formats: [markdown]
languages: [en]
```

**Complete:** [both paths, the second presupposing the first](examples/learn/tool-library-curriculum.yml).

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-28 | commissioned | LEARN authored by D2 | Holger, commons.o#92, comment 6472436136 |
| 2026-10-28 | revised | A commons keeps no learner's state | Holger, commons.o#92, comment 6472793436 |
| 2026-10-28 | revised | LEARN reframed: what a commons offers so that any learner with any agent learns its body of knowledge, ad hoc or by curriculum, with its knowledge kept apart from the agent's. The earlier draft's subject, how a commons learns from corrections, moves to `core-knowledge` (#98); the EA's question on its unit of learning falls away | Holger, commons.o#92, comment 6473604541 |
| 2026-10-29 | revised | The gap to `core-views` closed in the same change: its R6, schema and `views` check take the kind `curriculum` and `after`, and `after` must name another curriculum view of the CORE. Written for adoption; not yet adopted | the EA, commons.o#92, comment 6501201880 |
| 2026-10-29 | adopted | Adopted 29 October 2026 | Holger, [commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412) |
