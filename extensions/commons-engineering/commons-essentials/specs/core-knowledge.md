---
id: core-knowledge
title: Commons CORE — knowledge
status: decided
lang: en
touches: [core, core-views, model, graph, mcp, extension]
terms: [commons, commons-core, world, address]
schema: schemas/core-knowledge.schema.json
check: tools/check_core.py
supersedes:
  - Commons-Engineering/workshop@main:_specifications/STAKEHOLDER_REGISTER_SPEC.md
---

# Commons CORE — knowledge

*How certain a statement of a CORE is, and where its grounding is kept.*

## 1 · Goal

A CORE holds the near future of a commons, and it is only as good as the grounding beneath it. People and agents must be able to tell what rests on evidence, what is claimed, what is assumed and what is only expected, without a number pretending to more than it knows. This specification sets where a CORE keeps its grounding and how the standing of a statement is read from it. It decides one thing for its reader: **whether the knowledge of a CORE is well-formed, and what standing each of its statements has**. Most of this is a question of few strokes: a statement is certain enough when a further source would change no decision.

## 2 · Boundary

**Belongs here:**
- `knowledge/`, its sources and claims;
- the standing of a statement, and its vocabulary;
- what may feed expectations;
- corrections by a commons' own people;
- sources of standards, frameworks and law, their editions and jurisdictions, and how a record binds them;
- the stakeholder register as evidence;
- the rules on persons in evidence.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| the CORE's areas, identity and party register | `core` |
| how standing is shown in a view | `core-views` |
| the grammar of what a claim is about | MODEL |
| serving expectations and readings to others, and aggregation across commons | GRAPH, MCP |
| what an extension's maker holds of its research, and what a release carries | EXTENSION |
| what a commons offers so that anyone can learn it | LEARN |

## 3 · Terms

All terms resolve in the glossary. No term is new with this specification. The four rungs and two flags of part 5 are words of this specification.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | `knowledge/` holds the grounding of the model: its sources, the claims projected from them, the stakeholder register, its gaps and notes, and it is not a second copy of the model. | The commons' reasoning about itself is kept apart from scratch work and from the model it grounds. | knowledge |
| R2 | MUST | Every source names its origin and, where graded, its trust tier, raw bytes it rests on are kept with their hash and a pinned reference, and what was left out of a source is declared with it. | Who said it, how far it is trusted, and whether it can be read again decide what it may carry. | sources |
| R3 | MUST | Every claim names what it is about, the sources it rests on and its kind, keeping a commons' own declaration, an observation and a derivation apart, and a derived claim names the claims it is derived from. | A claim without its grounding is an opinion; a derived one without its inputs cannot be checked. | claims |
| R4 | MUST | The standing of a claim is read from evidence fit for that claim, as one of `expected`, `assumed`, `claimed` or `evidenced` with the flags `contested` and `superseded`, and it is never stored as a state of its own. | A stored label drifts from the evidence it summarises; a derived one cannot. | ladder |
| R5 | MUST | A source is authoritative for the kind of statement it can settle, so that a commons settles what it declares, decides and says of how it works while a claim that something it intended worked needs evidence of its own, and copies of one source count once. | Authority is scoped to the claim; neither a count of sources nor a tier decides it alone. | ladder |
| R6 | MUST | The earlier confidence and status words are read through the one mapping of part 5, and a word the mapping does not hold fails. | One vocabulary, so that every reader reads a claim the same way. | ladder |
| R7 | MUST | An expected statement is an expectation with an id `expectation:<n>` that stays the same for the same inputs, computed and cached with the build record, never written into the registry or `knowledge/` as a fact and never a source, of this CORE or another, while an event that an expectation's difference decided names it as `expected`. | A prediction stored as a fact becomes evidence for the next prediction, and a difference that changed a decision is known only where the decision names what was expected. | expectations |
| R8 | MUST | An expectation is as restricted as the most restricted of its inputs, is filtered before inference, and records its inputs, so that every expectation resting on a withdrawn input can be found. | Inference must not launder what a reader may not see. | review |
| R9 | MUST | Evidence given by a commons feeds other commons' expectations only by its opt-in, public claims of twins feed them by default, and expected statements never do. | A commons decides what it shares; guesses must not breed guesses. | review |
| R10 | MUST | A world holds no evidence and no probability: its statements are projected and judged by coherence, and nothing from a world enters evidence or expectations. | A world is explored, not forecast. | review |
| R11 | MUST | Authored narrative is a knowledge record with its language and what it rests on, and generated narrative is never an input of fact. | Prose written by a machine cannot become the ground it was written from. | review |
| R12 | MUST | The stakeholder register is evidence of who stands where: each standing names the family it runs through and its source, each entry one of three visibilities, and in a CORE kept by an outside observer (`perspective: observed` in its `commons.yml`) the register holds only public records and published profiles. | Observing strangers needs a lawful limit; holding a repository is no mandate to observe. | register |
| R13 | MUST | No private contact datum or pipeline state appears in `knowledge/`, an assessment or inferred attribute of a person appears only where the commons' mandate, grants and storage policy allow it, and no extension relaxes this rule, R12 or the exclusions a commons states. | What may be written about a person follows the commons' own mandate, so a life commons can assess itself, and never an extension's convenience. | private |
| R14 | MUST | A measure is a claim with its measure and its period, kept apart from when it was published, and news is a claim of kind `signal`. | A figure without its period is a different figure. | sources |
| R15 | SHOULD | Staleness is raised by a signal, not by age alone. | Old evidence of a lasting fact is still evidence. | review |
| R16 | MUST | How well the near future met what followed is read by holding the model's history against the later observations in `knowledge/`, and no probability is shown before it is calibrated. | A number that was never checked against outcomes misleads more than no number. | review |
| R17 | MUST | A correction by a commons' own person is a claim of kind `self-description` that holds the words as given and names its giver from the party register, the role or Post they held, the date, the claim or record it corrects and, where one did, the agent that recorded it and the view that prompted it, and it contests what it corrects until a decision or a source fit for the claim settles it, while a picture left uncorrected stands as it was and a prompted agreement is judged on its own evidence. | A person's correction relayed by an agent cannot otherwise be told from the agent's paraphrase, and no correction is not confirmation. | corrections |
| R18 | MUST | A correction counts only within its giver's standing for those it speaks of, as the party register and element 9 recorded it on that date, the people described keep their own right to correct what is said of them, and any use beyond the correction's own CORE and claim, anonymised or aggregated included, rests on its giver's recoverable word, linked from the correction. | Speaking for others needs a mandate, and a correction given in confidence that sharpens someone else's picture breaks trust before it is a question of aggregation. | review |
| R19 | MUST | A source that is a standard, a framework or a law names its edition by an id that names one edition and never changes, beside its full title, each edition enacted and not yet in force with its own id and `in_force` date, its jurisdiction, `global` where none enacts it, its relation, licence and access class, and its verification against the primary source by confirmation and by refutation, with their dates and what the second lens corrected, while a commons' own synthesis is a source of relation `own` with `standing: design` and its derivation instead. | A new edition must reach what it affects, and a source is trusted only after it survived the second lens. A design must never pass for evidence of the world. | sources |
| R20 | MUST | A record binds a source by its id, the id of the edition in force at the time the record speaks for and, optionally, the `part` it rests on, so that a scheduled edition is never claimed before its date, a deliberate design rests on a claim of its own with that standing and never on a binding made for the purpose, and the bindings of one jurisdiction's law to records are kept in `knowledge/jurisdictions/<jurisdiction>.yml`. | The steering loops must know which text at which edition they watch, and law that holds in one place stays with the commons that lives under it. | sources |

## 5 · Structure

The schema is `schemas/core-knowledge.schema.json`. Its root is `knowledge/sources.yml` or `knowledge/claims.yml`, holding `sources` or `claims`. The register keeps its own shape, read by its validator.

**The ladder**, from what is stored:

| Rung | When |
|---|---|
| `evidenced` | evidence fit for that claim: a source authoritative for that kind of statement (a register for a filing, the commons for what it declares and decides), or independent sources, not copies, relevant to the claim and its period |
| `claimed` | a source that cannot settle the claim on its own, such as a commons' statement that an intended change worked |
| `assumed` | no source |
| `expected` | not stored at all: computed from the kind of commons and shown beside *missing* (R7) |

A claim is **contested** where another claim contradicts it, and **superseded** where a later one replaces it. A derived claim takes the lowest rung of its inputs. The kinds keep intent, observation and derivation apart: `self-description` for what a commons declares, `fact`, `measure` and `signal` for what is observed, `derived` for what is inferred. A source's tier and the count of sources inform the standing; they do not decide it.

**A correction** is a claim of kind `self-description` with a `correction` object: `given_by` (a party register id), `standing` (`post:`, `body:` or `role:` with its id), `given` (a date), `corrects` (a claim id or a record), optionally `recorded_by` and `prompted` (a view and its revision), and `release`, a list of `{use, word}` that is empty for the correction's own scope only (R17, R18). It names what it corrects and supersedes nothing by itself.

**A source of a standard, framework or law** adds to the fields of every source: `designation` and `terms`, `edition` and `edition_title`, `scheduled` (`{edition, in_force, affects?}`), `jurisdiction`, `area`, `relation` (`derived-from`, `adopt`, `bind`, `mirror`, `own`), `verified` (`confirmation`, `refutation`, `corrected`), `licence`, `class` and `informs`; a source of relation `own` holds `standing: design` and `derivation` (R19). **A binding** is `{source, edition, jurisdiction?, relation?, part?}`. A jurisdiction's file is `{jurisdiction, bindings: [{record, binds: [binding]}]}` (R20).

**The mapping of earlier words**, the only one: `belegt` and `established` and `Beleg` → at most *evidenced*; `unbestätigt`, `unbestaetigt`, `website`, `marktreport`, `intern`, `inferred`, `abgeleitet`, `gerechnet` and `Nachweis` → at most *claimed*; `Annahme` and `hypothesis` → *assumed*; `divergent`, `contested` and `contested-strong` → the flag *contested*. A word not listed fails (R6).

## 6 · Checks

`tools/check_core.py <core>` checks a CORE's `knowledge/` together with the rest of the CORE.

| Check | Tests |
|---|---|
| `knowledge` | `knowledge/` is where the structure definition puts it, or reported as unmigrated (R1) |
| `sources` | every source validates and names its origin, a standard's fields in their form; a measure names its period; every file in `knowledge/jurisdictions/` validates and binds only sources of its jurisdiction (R2, R14, R19, R20) |
| `claims` | every claim validates; its sources and inputs resolve; an empty list is a gap (R3) |
| `ladder` | every confidence or status word maps (R4, R5, R6) |
| `expectations` | no source points into a build record (`.build/`) or a run's package (`graph/runs/`), of this CORE or another (R7) |
| `corrections` | a claim with a `correction` is of kind `self-description` and its correction validates; its giver is in the party register; it corrects a claim or record the CORE holds; a prompted correction resting on no source is a gap (R17) |
| `register` | the register's visibilities; no `private` entry where the CORE's `perspective` is `observed`; `holder` alone sets no limit (R12) |
| `private` | no e-mail address or telephone number in `knowledge/` outside the party register; assessments of persons only where the commons' grants allow them (R13) |
| `review` | a review by the human accountable for this specification's mandate, against the Why of R8 to R11, R15, R16 and R18 |

**Gap (R16, R27 of SPECIFICATION):** an expected statement is shown beside *missing* without a share, because no population of commons of one kind exists yet against which completion under sparse evidence could be held to the base rate; the public twins are too heterogeneous to derive one (Holger, commons.o#97, 6473799025).

## 7 · Example

**Minimal:** one claim resting on one source in which the library speaks about itself:

```yaml
sources:
  - {id: S1, title: The library's own opening notice, origin: given, about_itself: true}
claims:
  - {id: C1, statement: The library lends tools on Tuesdays and Saturdays., about: [lending], sources: [S1]}
```

C1 is what the library declares about how it works, and the library is authoritative for that, so C1 reads as *evidenced* (R5). **Complete:** the `knowledge/` of [the tool library's CORE](examples/core/tool-library.core/knowledge/claims.yml), and its [corrections](examples/core-knowledge/corrections.yml) (R17, R18).

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | the knowledge part of Commons CORE, split along its boundary | commons.o#89, opened on the word of the human accountable |
| 2026-10-26 | adopted | Adopted after the EA's points: standing from evidence fit for the claim, intent and observation kept apart; the public-only limit for outside observation only; assessments of persons scoped to the commons' mandate, grants and storage | Holger, commons.o#89, comment 6415733592 |
| 2026-10-28 | commissioned | KISS pass: corrections by a commons' own people come here from LEARN (R17, R18, the check `corrections`); the fields of a standard's source and of a binding come from EXTENSION R30, R31 and R36 (R19, R20); an expected statement is an `expectation` with an id, is named by the event it decided and is never a source (R7, the check `expectations`, from P1), so that `reading` stays the Fabric's word (D0-CE, commons.o#99 6474472957); no population for calibration yet, named as a gap under part 6 (P1 demonstration 1, Holger 6473799025); the carry-over moves to `carry-over/core-knowledge.md`. Written for adoption; not yet adopted | Holger, commons.o#98 ("Ja, alle"); P1, commons.o#97 |
| 2026-10-28 | adopted | The KISS revision adopted: the corrections (R17, R18), a standard's source and a binding (R19, R20), and the expectation with its check (R7) | Holger, commons.o#98, comment 6474773388 |

**Rests on:** S6 (commons.o#74, 25 October 2026); B2–B6 (#79); H1, H2, H4, H6 and the reconciliation of the ladder (#86, 25 October 2026); T1, the few-strokes principle and the near future (26 October 2026).

What this specification supersedes, and what it carries of it, is in [`carry-over/core-knowledge.md`](carry-over/core-knowledge.md).
