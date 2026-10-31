---
id: core-views
title: Commons CORE — views
status: decided
lang: en
touches: [core, core-knowledge, model, flow, extension, mcp, learn]
terms: [commons, commons-core, blueprint, lighthouse, world]
schema: schemas/core-views.schema.json
check: tools/check_core.py
supersedes:
  - Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md
---

# Commons CORE — views

*The blueprint of the whole commons, and the views a CORE renders from it.*

## 1 · Goal

A commons is read by its board, its people, its partners, the public and agents, and each needs a different cut of the same picture. The picture is the blueprint: one definition covering the whole commons, section by section. A view selects and orders sections for one audience and is rendered from the CORE's records, never written beside them. This specification decides one thing for its reader: **whether what a CORE shows is a faithful rendering of what it holds**, for the reader it is meant for.

## 2 · Boundary

**Belongs here:**
- the blueprint definition and its outcomes;
- view definitions and their kinds;
- the rendering and its build record;
- what a view may say, and to whom.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| the records a view is rendered from | `core`, MODEL |
| the standing of a statement | `core-knowledge` |
| who renders, reviews and delivers, and when | FLOW |
| the sections an extension adds, templates for authored parts | EXTENSION |
| serving views to machines | MCP |

## 3 · Terms

All terms resolve in the glossary. No term is new with this specification. The view kinds and the five outcomes of part 5 are words of this specification.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | The blueprint definition covers the whole commons: one section per node of the frame (dimensions, families, elements, knowledge, lifecycle, operations), each with a stable id, the node it binds to, its cardinality and its labels per language. | A document's chapters are an accident; the frame is the same in every commons, which keeps commons comparable. | sections |
| R2 | MUST | A section reads the CORE through structure keys only, never through paths. | The CORE's layout can change without one section changing. | sections |
| R3 | MUST | Every section of a rendering has one outcome, `covered`, `not-selected`, `missing`, `documented-absence` or `unsighted`, and an expected picture is shown beside `missing`, never as an outcome of its own. | A gap is a question, an absence needs evidence, and what could not be read is neither. | build-record |
| R4 | MUST | A documented absence rests on evidence of the absence, and what the researcher could not see is unsighted, never absent. | Absence of evidence is not evidence of absence. | review |
| R5 | MUST | A view is a definition in `views/<name>/view.yml` naming its kind, its audience, its sections in order, its formats, its languages and, where it is delivered elsewhere, its host. | A view as data can be rendered, checked and compared; a document cannot. | views |
| R6 | MUST | The view kinds are `briefing` (full, summary, environment, futures), `lighthouse`, `spoken`, `portal`, `card`, `gaps` and `curriculum`, one path of sections read in order whose `after` names the paths it presupposes (`learn` R2), and a commons may add a kind of its own. | Shared kinds keep views comparable; an own kind is a commons' right. | views |
| R7 | MUST | A rendering is generated from records, never edited by hand and never a source of fact, and the full briefing's rendering is `briefing.md`. | A view written beside the model drifts from it. | build-record |
| R8 | MUST | Every rendering names what produced it in a committed build record, with the versions of its definitions and the hash of its inputs, and a rendering whose inputs changed is stale, never a defect. | A reader must be able to tell what a view rests on and whether it is current. | build-record |
| R9 | MUST | A view writes about the commons and its world, never about the evidence trail: a statement's standing shows as a source in brackets, an assumption says so, a contested claim is named, and a figure without a source is not stated. | The reader learns the commons, and still sees how sure each sentence is. | review |
| R10 | MUST | An interactive view reads data and section ids, never prose. | Prose cannot be queried without guessing. | review |
| R11 | MUST | Each view states what it promises its reader and where a correction goes. | A view without a way back cannot learn. | views |
| R12 | MUST | A view shows the commons' state, our confidence and the relationship as three axes, never as one score, and never shows the relationship in a public view. | One score hides which of the three it measures. | review |
| R13 | MUST | A rendering is filtered by the reader's grant before it is composed, and a committed rendering has one audience. | What is composed cannot be filtered afterwards. | review |
| R14 | MUST | The full briefing opens with the purpose, stated precisely enough to be challenged, and reads who the commons is, how it works and where it is heading, in that order, its middle part generated from the registry. | One reading order in every commons, and the working body never out of step with the model. | review |
| R15 | MUST | A futures view names and summarises worlds and their no-regret moves and never contains them, and every world it names has a world CORE behind it. | A world is a full instance of its slice, not a chapter. | review |
| R16 | MUST | The spoken view says the commons in seven beats (name, same, fame, pain, aim, game, exchange), keeps its two forms apart, and passes the repeat test: a stranger can give it back. | If a commons cannot say its purpose so that a stranger can repeat it, the purpose is not precise enough. | review |
| R17 | MUST | A public face in a repository of its own is the structure key `views/<name>` pointing there, never a submodule. | The membrane between the private CORE and its public face is a declared location. | review |
| R18 | MUST | A view is rendered in the commons' own language, and in another language only where its definition names it. | A commons speaks in its own words first. | views |
| R19 | SHOULD | Views rendered from one definition for different commons hold the same contract, each with its own selected elements. | Comparability is the point. | review |
| R20 | MUST | A deliverable of a milestone is a view committed at that milestone, and handing a CORE to its commons is an adoption, not a view. | A milestone is a moment; a handover is a change of who holds the CORE. | review |

## 5 · Structure

The schema is `schemas/core-views.schema.json`. Its root is one of two files: `views/blueprint.yml`, holding `sections`, or a `views/<name>/view.yml`, a flat `view`.

**The blueprint definition** is authored once in commons-essentials and generated identically into every extension. A commons may add sections of its own in `views/blueprint.yml`.

**A view** lives in `views/<name>/`: its definition `view.yml`, and its renderings.

**Identity:** a view is known as `view:<name>`, by its folder, and a section as `section:<id>`, by its id (R1), wherever another specification reads them, as a graph does (`graph` R5).

**The build record** of a view is `.build/<name>/manifest.json`. It holds:
- `definitions`: the versions of the blueprint definition, the view definition and the structure;
- `inputs`: each input with its hash;
- `outcomes`: each section id with its outcome.

The outcomes:

| Outcome | Means |
|---|---|
| `covered` | the section is rendered from records |
| `not-selected` | the commons has chosen not to hold it: an answer |
| `missing` | nothing is known yet: a gap and a question |
| `documented-absence` | evidence shows it does not exist |
| `unsighted` | it could not be read under the access at hand |

## 6 · Checks

`tools/check_core.py <core>` checks a CORE's views together with the rest of the CORE.

| Check | Tests |
|---|---|
| `sections` | every section validates, ids are unique, and every need is a structure key (R1, R2) |
| `views` | every `view.yml` validates, carries its folder's name, names sections that exist, and states its promise, way back and languages; a curriculum's `after` names curriculum views of the CORE; an unknown kind is reported, not failed (R5, R6, R11, R18) |
| `build-record` | every rendering has a build record that names its definitions and inputs and an outcome for each of its sections, among the five; an empty record is no provenance (R3, R7, R8) |
| `review` | a reading by the human accountable for this specification's mandate, against the Why of R4, R9, R10 and R12 to R20 |

## 7 · Example

**Minimal:** one view of kind `card`, its `views/card/view.yml`:

```yaml
name: card
kind: card
audience: anyone who meets the commons
promise: what the commons is and how to reach it
way_back: a proposal item in the Commons Workshop
sections: [d0.perception-to-mandate]
formats: [markdown]
languages: [en]
```

**Complete:** [the views of the tool library's CORE](examples/core/tool-library.core/views/card/view.yml), with a blueprint definition, a full briefing and a card, each with its build record.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | the views part of Commons CORE, split along its boundary | commons.o#89, opened on the word of the human accountable |
| 2026-10-26 | adopted | Adopted together with `core` and `core-knowledge`; empty build records are no provenance | Holger, commons.o#89, comment 6415733592 |
| 2026-10-29 | revised | R6 and the schema take the kind `curriculum` and its field `after`, to be adopted together with `learn` (R2), as the EA asked (commons.o#92, comment 6501201880). Adopted 29 October 2026 ([commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412)) | Holger, commons.o#92, comment 6473604541 |
| 2026-10-29 | revised | Part 5: a view is known as `view:<name>` and a section as `section:<id>`, and the `views` check holds a view's `name` to its folder (part 6), so that a graph can serve a curriculum step to a learner outside the repository (`learn` R2). Adopted 29 October 2026 ([commons.o#92, comment 6509201761](https://github.com/Commons-Engineering/commons.o/issues/92#issuecomment-6509201761)) | D2-CE's demonstration, commons.o#92, comment 6505909477; the form agreed with @D4-CE |

**Rests on:** #79 A–E, C1 and C3 (Holger, 25 October 2026); H8 (#86).

**Supersedes**, each text in part.

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | the Living Blueprint is the Core's file format and its boot sequence (§2.1, §7) | dropped |  | the blueprint is a view generated from records | Holger, 25 October 2026 (commons.o#79, comment 6397521121) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | the blueprint's three parts: who we are, how we work, where we are heading (§7) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | where it overlaps the registry the blueprint summarises and points; nothing is kept twice (§7.1) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | touchpoint definitions, view configuration and generated output are kept apart (§8.2) | carried | R5 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | one blueprint per commons, narrative over the database, nothing entered twice (§6.4) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | old blueprints stay readable as history and are not rewritten (§6.4) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | publishing: views generated, delivered to their host (§6.6, §8.1) | carried | R5 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | who sees which view is decided per view (§6.6) | carried | R13 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | an intranet dashboard of completion per part (§8.3) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | two phases: an authored Blueprint Specification and a Living Blueprint (pre) | dropped |  | the blueprint is a view generated from records | Holger, 25 October 2026 (commons.o#79, comment 6397521121) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | the Blueprint is the maintained deliverable, and the best truth where records are not integrated (§2) | dropped |  | views are never a source of fact | Holger, 25 October 2026 (commons.o#79, comment 6397521121) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | three layers in one text: shared vocabulary, the evidenced layer, the commons' own voice (§3) | carried | R9 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | text about the system and its world, never about the evidence trail (§3) | carried | R9 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | the shape: who we are, how we work, where we are heading (§3, §4) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | every briefing opens with purpose, precise enough to be challenged (§5) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | the spoken-form test (§5) | carried | R16 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | a register of no-regret moves across the futures (§6) | carried | R15 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | the triad: the Blueprint says, the Core has, the Graph sees (§11) | dropped |  | the blueprint is a view inside the CORE | Holger, 25 October 2026 (commons.o#79, comment 6397521121) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | one commons, one full briefing (§2) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | its location is `blueprint.md` at the instance root (§2) | dropped |  | the generated root document is `briefing.md`; views live in `views/<name>/` | Holger, 25 October 2026 (commons.o#79, comment 6397521121) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | written in the commons' language, with other languages where needed (§2) | carried | R18 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | the audience is stakeholders, not auditors (§2) | carried | R5 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | the narrative summarises; the registry is the database (§2, §5) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | the contents of Part I, II and III (§3) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | the parts are never reordered or omitted (§3) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | an omitted dimension is named in its place (§4, §8.1) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | no audit voice; sources in brackets, gaps in their own place (§5) | carried | R9 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | no invented figure (§5) | carried | R9 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | no claim to completeness; what is not carried is named (§5) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | every substantive claim shows its standing (§6) | carried | R9 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | the apparatus lives in the model; the view shows standing only (§6) | carried | R9 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | a view names and summarises futures and never contains them (§7) | carried | R15 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | conformance is checked by machine; a stale view is regenerated (§9) | carried | R8 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md` | the spoken form: seven beats, two forms never merged, universal beats with the commons' own filling (§3.3) | carried | R16 |  |  |

**Not superseded here**

| Text | Rules | Stays until |
|---|---|---|
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | §1–§2 (one architecture for all domains), §2 (the pack owns the template) | extension |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | §4–§9 (anatomy, physiology, purpose review, transition engineering, feedback, governance, the Triple Diamond) | flow |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_BLUEPRINT_MANIFEST.md` | §10 (the blueprint pattern collection) | library |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | §8 (templates per pack, one domain pack, template conformance) | extension |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | §5 (no physiology chapters: loops live in the loop registry) | flow |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_BLUEPRINT_SPEC.md` | §10 (MCP serving) | mcp |
