---
id: library-patterns
title: Commons LIBRARY — patterns
status: draft
lang: en
touches: [specification, library, core, core-knowledge, core-views, model, graph, graph-engine, extension, mcp]
terms: [commons, pattern, orbit, known-use, singularity, value-stream-family, commons-library]
schema: schemas/library-patterns.schema.json
check: tools/check_library.py
supersedes:
  - Commons-Engineering/workshop@main:_manifests/COMMONS_PATTERNS_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_PATTERNS_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/PATTERN_PIPELINE_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/PATTERN_POOLS.md
  - Commons-Engineering/workshop@main:_specifications/PATTERN_PROMOTION_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/ADDRESSING_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md
---

# Commons LIBRARY — patterns

*A pattern is written by people, earns its orbit by a ruling, names no one, and reaches every commons as part of a released extract.*

## 1 · Goal

A commons recognises its own tension in a pattern only if the pattern is a whole, readable text, grounded in principles and in places where it was seen to work, and free of anyone's property or anyone's name. Patterns condense inward through the orbits by the judgement of people, never by the arithmetic of a machine, and what was learned at the edge must be able to return without exposing who learned it. This specification decides two things for its reader: **whether a pattern is well formed and may be released**, in its form, its grounding, its known uses and its relations, and **how a pattern moves**: how it enters at the edge, how its orbit changes, and how it reaches a commons as part of an extract with its agents' index.

## 2 · Boundary

**Belongs here:** a pattern's form; its id, orbit and hubs; its known uses; its relations and lifecycle; promotion and relegation; how an observation enters; the extract and its index.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| a library, its releases, versions, index, gate, and the provenance fields of a release | `library` (R10) |
| where a CORE installs an extract, its lock, own patterns and adaptations | `core` |
| a pattern's membership in a family: an address, its status and what counts as `ratified` | `model` (R18, R24) |
| computed neighbours and runs | `graph`, `graph-engine` |
| reading lists across patterns | `core-views`: a list is a view |
| a confidence word's standing | `core-knowledge` |
| how patterns are generated and enriched | the Pattern Engine |

**Touches** `specification`, `library`, `core`, `core-knowledge`, `core-views`, `model`, `graph`, `graph-engine`, `extension` and `mcp`. **Rests on** the decided rules that #91 carries: free of IP, no organisation names in the discipline (the known uses neutralised, commons.o#85, K4), never publish one to one, an incomplete package fails closed; on CORE's patterns revision (commons.o#95, comments 6438391848 and 6438865249); and on the KISS pass (commons.o#98).

## 3 · Terms

All terms resolve in the glossary. *Hub*, *observation* and *ruling* keep their ordinary meaning, made precise by part 5.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | A pattern is one Markdown file whose front matter holds what machines read and whose body holds what people read, and every pattern of one release follows one version of the form of part 5. | People and agents read the same file, and a release in two forms is two releases. | form |
| R2 | MUST | A pattern's id is `pat_` followed by a stable identifier that is never regenerated or reused, its source-qualified id `<library>/<id>` names it across libraries, and its slug is only a label. | References outlive titles, slugs and folders; a reused id silently changes what others cite. | form |
| R3 | MUST | A pattern's orbit, 0 to 5 in the meaning of part 5, changes only by a person's ruling on evidence against part 5's criteria for that orbit, `promote`, `return`, `archive` or `reject` with its reasons, keeping the observations it rests on, and it moves outward only when a signal shows it contradicted or its context gone, never by its age, by default or by a script. | An orbit says how far a pattern has condensed; an orbit nobody ruled on is a script's opinion, and old evidence of a lasting pattern is still evidence. | lifecycle |
| R4 | MUST | Every pattern of orbit 2, 3 or 4 names at least one principle of orbit 1 it rests on. | A pattern that rests on no principle is a recipe, not a pattern of living systems. | anchor |
| R5 | MUST | A pattern's body holds the eight sections of part 5, none of them empty, a placeholder or cut off mid-sentence, and a pattern that lacks one is not released. | An incomplete pattern fails closed; a truncated one reads as complete. | form |
| R6 | MUST | A pattern's known uses are at least two, each a place named by its city, region or country, and none names an organisation or a person, so that a commons appears as `[commons]` or by its kind. | A known use shows that the pattern works somewhere; naming who it worked for makes the discipline a client list. | known-uses |
| R7 | SHOULD | At least one known use of a pattern lies outside the Western world. | A pattern drawn from one tradition mistakes a custom for a law. | review |
| R8 | MUST | A pattern names no framework code, trademark or hierarchy of a third party in its sections, and a tradition it draws on is named only in its sources, as attribution, never claimed. | Practice is extracted, not copied; what is attributed once cannot leak into a commons' words. | ip |
| R9 | MUST | A pattern's relationships are curated, by id, of three kinds, `requires`, which never runs in a circle of any length, `complementary` and `alternatives`, which may be mutual, none written by a machine, so that a computed neighbour remains a proposal of a run (`graph` R4). | A text a machine rewrites is no longer its authors', and a dependency in a circle explains nothing. | relations |
| R10 | MUST | A pattern's status is `candidate`, `stable` or `archived`, an earlier `draft` or `observed` being read as `candidate`, and a pattern that leaves is archived and never removed. | Lineage survives; a deleted pattern leaves every reference to it dangling. | lifecycle |
| R13 | MUST | A pattern addressed to no family records why: out of scope, a gap in the families claimed, or not yet looked at. | An absence with a reason is information; an absence without one is debt. | review |
| R15 | MUST | An observation enters orbit 5 as a proposal to the library's maker (`mcp` R12), names no person and no organisation, and one that repeats another merges into its evidence rather than becoming a second pattern. | Learning returns without exposing who learned it, and recurrence is evidence, not duplication. | review |
| R17 | MUST | An extract holds the patterns of orbits 0 to 3 at their release paths, the agents' index of part 5 and its release record (`library`), and it is cut from one released graph run by its extractor under a policy, so that the same patterns cut differently are another release. | Every commons works offline from the same condensed core, and a release must say what it was cut from. | extract |
| R18 | MUST | Every pattern line of the index holds the fields of part 5 and `context.families` with `vsf:<family>` for each family whose address the pattern holds `ratified` (`model` R18, R24). | The family join is how a commons' own model meets the library, and it needs no method (`graph` R14). | extract |

R14 and R16 are folded into R3; R11 moved to `library` R10, R12 and R20 to `model` (R18, R24), and R19 to `core-views`, a reading list being a view. None of these ids is reused.

## 5 · Structure

The schema is `schemas/library-patterns.schema.json`. Its root is a pattern's front matter; its `$defs` hold `index_line`, a line of the agents' index.

| Front matter | Holds |
|---|---|
| `id`, `slug`, `title`, `summary`, `aliases` | the stable id (R2); its label, name and one-paragraph summary |
| `orbital_layer` | the orbit, 0 to 5 |
| `gravitational_hubs` | the principles of orbit 1 it rests on, by id or slug (R4) |
| `ontology` | `search_hints.primary_tension` (the tension in one sentence), domain and cross-domains |
| `lifecycle` | `status` (R10), `version`, `confidence` (read through core-knowledge's mapping) |
| `relationships` | curated lists by id: `requires`, `complementary`, `alternatives` (R9) |
| `value_model` | the families it is addressed to, each an address with `slug`, `weight` and `status` (`model` R18), or `unaddressed` with its reason (R13) |
| `contributors`, `sources`, `license`, `attribution` | provenance and licence, the only fields that name anyone (`library` R10) |

No other field holds a relation, and no pattern holds a garden block.

**The body,** in this order, each a level-3 heading `### Section <n>: <name>`: 1 Context, 2 Problem, 3 Solution, 4 Implementation, 5 Consequences, 6 Known Uses, 7 Cognitive Era, 8 Vitality. A known use is a paragraph that begins with its place in bold.

**The orbits and what earns the next** (R3):

| Orbit | Holds | Earned by |
|---|---|---|
| 5 | observations at the edge | a commons' proposal (R15) |
| 4 | domain patterns | at least three independent commons |
| 3 | transversals, cross-domain by constitution | re-expression in at least two domains |
| 2 | commons patterns | constitutive of a commons as such |
| 1 | principles, fewer than a hundred | reduction to a law of living systems |
| 0 | the singularity | touching the axiom |

**The agents' index** (`index.jsonl`): its first line is `{kind: index, release, graph_run, extractor, policy, scope, licence}`; each further line is `{kind: pattern, id, slug, orbit, file, title, tension, summary, context: {sector, labels, families}, hubs, links, beyond}`: `links` to patterns inside the extract, each `{to, kind, by}`, `by` being `stated` or `computed`, a computed link naming its `method` and, with a `score`, what it measures in `score_is`, never a confidence, and `beyond`, at most five ids outside it, as strings.

## 6 · Checks

`tools/check_library.py <library>` runs these checks on every extract a library holds, with those of `library`; `--patterns <folder>` runs them on a folder of pattern files, as a pattern source does before it releases.

| Check | Tests |
|---|---|
| `form` | the front matter validates against `$defs/pattern`, with no garden block; the id is `pat_…` and unique; the eight sections are there, none empty, none a placeholder, none ending mid-sentence; licence and attribution are stated; with `--names`, no listed name in a section outside the Known Uses; one form version in a release (R1, R2, R5) |
| `anchor` | a pattern of orbit 2, 3 or 4 names a hub that is a principle of orbit 1 (R4) |
| `known-uses` | at least two known uses, none an e-mail address or a name of `--names` (R6) |
| `ip` | no term of `--terms` (third-party codes and trademarks), and none of the discipline's rejected words, in the eight sections (R8) |
| `relations` | every curated relationship is of the three kinds and names an id that resolves, and no `requires` runs in a circle of any length (R9) |
| `lifecycle` | the status is one of R10's; the orbit is 0 to 5 (R3, R10) |
| `extract` | an extract's patterns are of orbits 0 to 3 at their release paths, every file its index names lies inside it, its index validates line by line against `$defs/index_line`, links included, repeats its release record and has the record's digest, and every family in `context.families` is ratified in its pattern (R17, R18) |
| `review` | a reading by the human accountable, or by an agent that has only this file, of R3, R7, R13 and R15 |

## 7 · Example

**Minimal:** a pattern of orbit 2 with a hub, ratified for one family, its eight sections following its front matter:

```yaml
id: pat_tool0001
slug: sharing-tools-across-households
title: Sharing Tools Across Households
summary: A neighbourhood pools its tools so that everyone can borrow what each owns.
orbital_layer: 2
gravitational_hubs: [reciprocity-sustains-cooperation]
ontology: {search_hints: {primary_tension: Idle tools in every household vs. scarce access for those who need them}}
lifecycle: {status: candidate, version: '0.1', confidence: 2}
value_model: {vsf: [{slug: demand-to-fulfillment, weight: 1.0, status: ratified}]}
contributors: [the garden library's stewards]
license: CC-BY-SA-4.0
attribution: Commons Engineering contributors
```

**Complete:** [the demo library's extract](examples/library/demo.library/patterns/v2026.11.0/release.yml), three patterns with their index; `check_library.py` reads it with 0 fail.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | Patterns with their known uses, the 244 known uses neutralised, never published one to one; part of LIBRARY | Holger, commons.o#91; commons.o#85, K4 |
| 2026-10-28 | revised | KISS: one rule for an orbit's change (R3, from R3, R14 and R16); provenance to `library` R10, memberships and what `ratified` means to `model` R18 and R24, the model addressing the library to `model`; three relation kinds and three statuses; `influence`, `regions` and the garden block cut; collections are views (`core-views`); the ids of folded rules retired, never reused (SPECIFICATION R7) | Holger, commons.o#98 (*"Ja, alle"*) |
| 2026-10-29 | revised | The schema holds a link's shape, `{to, kind, by}`, a computed link with its `method`, a `score` with its `score_is` and no confidence, so that the shared check of a copy covers what CORE checked of an installed extract; every file the index names lies inside the extract (R17) | D1-CE on the EA's read of #98 |

**Open for Holger:** **P1** whether addressing keeps *depth follows generality* (ADDRESSING §2: orbit 4 to value streams, orbit 3 to families only), which its own §9 doubts; **P2** the editorial Posts for promotion (a Pattern Editor per domain, an appeal), or none (PROMOTION §6.3); **P3** whether `canonical` with aliases is a status for redundant patterns (PIPELINE §14.3a).

What this specification supersedes, and what it carries of it, is in [`carry-over/library-patterns.md`](carry-over/library-patterns.md).
