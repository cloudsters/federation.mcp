---
id: extension
title: Commons EXTENSION
status: decided
lang: en
touches: [specification, model, core, core-knowledge, core-views, flow, library, graph, mcp]
terms: [extension, domain-core, essentials, enhanced, install, adopt, not-selected, archetype, kind, commons, commons-core, commons-library]
schema: schemas/extension.schema.json
check: tools/check_extension.py
supersedes:
  - Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md
  - ../commons/specs/PACK_SPEC.md
---

# Commons EXTENSION

*Where a domain is made, what it releases, and how a commons takes from it.*

## 1 · Goal

No commons holds enough knowledge of its own kind to model itself well from nothing. An extension is how that knowledge reaches it: a standard menu for one kind of commons, from which a commons takes what fits and rarely takes anything unchanged. This specification decides three things for its reader. **Where a domain is made:** a `[domain].core`, a CORE like any other, maintained and possibly private, whose own model is its research and stewardship, whose research stays whole in its `knowledge/`, and whose offer sits apart in `offer/`. **What it releases:** an **extension**, the released, gated offer of one `[domain].core`, one version held in a library and installed from it, with its *essentials* installed and its *enhanced* depth served. **How a commons takes from it:** it **installs** the essentials of one extension of its kind, whole and read-only, **adopts** archetypes into its own registry, each naming its origin, and records what it does **not select**; every departure stays visible, because it is derived from the record and its origin, never listed by hand.

## 2 · Boundary

**Belongs here:**
- a `[domain].core`'s offer and the research it rests on;
- the extension, its version, its parts and its release record;
- installing, adopting, adapting and not selecting;
- which extension a commons holds;
- Extension-Builders;
- freedom from intellectual property and private data.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| the grammar the archetypes are written in, and the fields every record has | MODEL |
| the areas of a CORE, its lock, its events, its tiers of topology | CORE |
| the offer page and every other view | CORE-VIEWS |
| sources, claims and their standing; a standard's edition, jurisdiction and verification; how a record binds a source | CORE-KNOWLEDGE |
| adopting as work: the Story, and the loop that brings a newer version | FLOW (`flow-workshops` R12 to R14) |
| where a library keeps its releases, how it runs the gate, how libraries are found | LIBRARY |
| what commons adopt, returned to the `[domain].core` as an aggregate; a `[domain].core` as a source of another commons' graph | GRAPH |
| who may read which part, and serving it | MCP |

An extension extends MODEL's grammar and never redefines it.

## 3 · Terms

All terms resolve in the glossary.
- *Install*, *adopt*, *not selected*, *archetype* and *kind* are D0-CE's words (commons.o#90, 6420921361).
- *Extension*, *`[domain].core`*, *essentials* and *enhanced* are Holger's (6464648757, 6464676842). *Essentials* and *enhanced* name parts of one extension, never two.
- *Library* as an element-model key, *manifest* as an extension file, *activate* and *declined* are rejected.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | An extension is the released, gated offer of one `[domain].core`: one version of its `offer/`, held in a library and installed from it, named `<library>/<extension>@<version>`, where `<extension>` is the offer's `id`, the domain, and it and every archetype it offers are named qualified by library and extension, so that a bare slug establishes no equality between two extensions. | The maker may be private and is maintained in one place; what travels is one released thing with one name. Two extensions may use one word for two things. | release |
| R3 | MUST | A version is semantic and released once, never changed; renaming or removing an offered record is a new major version, whose release record maps each old id to its new id or to `null` where it is retired. | A commons that installed a version must be able to rely on it, and a rename cannot be derived. | release |
| R4 | MUST | The offer of a CORE sits in `offer/`, apart from its own model: `offer/offer.yml` states it as data; the essentials are the archetypes as records of `offer/registry/` in MODEL's grammar, one per file, and one steering loop in `offer/loops/` for every family its value streams name; the enhanced depth is in `offer/enhanced/`, where records may be held densely, each with a stable, addressable id; and nothing is in a format of its own. | The record, not the file, is the unit: what a commons maintains is one file per record, and served depth may be dense as long as every record can be named. | contents |
| R7 | MUST | An offer's records hold MODEL's grammar and state no dimension or family of their own: every value stream has steps and names one of MODEL's thirteen families, every step binds L3 capabilities of the map, every capability below L0 names its parent, and every record is an archetype, never an individual. | What a commons adopts must already be well-formed, and identical families keep every commons comparable with every other. | core |
| R8 | MUST | An offer whose records fail their checks is not released, and one that offers less is read as offering less: an archetype it does not offer is a gap, never borrowed from another extension. | A broken offer fails closed; a small offer is an honest one, and a commons built half from one extension and half from another belongs to neither. | contents |
| R9 | MUST | A commons holds the discipline's specifications, which are the grammar and no layer, and installs exactly one extension of its kind as its primary, the best fit read from what the commons is by routing rules that record why, or another it chooses with its reasons, with no base extension beneath it, no layering and no second extension. | The grammar is shared by every commons; for its kind, one extension answers, layers answer for nothing, and the commons has the last word. | fit |
| R11 | MUST | A commons that spans several kinds is several COREs, each with its own extension. | Each CORE stays readable in one grammar of one kind. | review |
| R12 | MUST | A commons installs only a released extension, from a library it names, and of it only the essentials, which are public and hold every part a commons needs offline and without rights, such as its steering loops, whole and read-only as a copy under `extensions/<library>/<extension>/`; it runs the gate's deterministic part again at install; the enhanced part, the depth, patterns and studies, is only ever served and never installed or copied into a CORE; its lock records the release, its origin in the library and which parts are installed and which served; and installing writes nothing into its registry. | What is installed is the offer, not the commons' model, and the gate decides, not the address. What a commons holds, it holds whole so that it can leave its host, while depth it may not hold stays protected where it lies. | install |
| R13 | MUST | An extension never writes into a commons: an archetype enters the commons' registry only as the commons' own complete record carrying `adopted_from`, never as a reference, an archetype the commons does not select is a `not-selected` event in `lifecycle/` with its reason, an update never overwrites what the commons wrote, and what a commons adopts, adapts or does not select returns to the maker only where the commons releases it, and only as an aggregate across commons. | A menu offers, a commons decides, and a decision against something differs from never having known it. The menu learns from its reception only as far as a commons lets it. | adopt |
| R14 | MUST | Every term in an offer's records, loops and views is Commons language, and a standard, framework or law is named only as a source: in the `[domain].core`'s `knowledge/sources.yml` and in the release's attribution list, with its edition; a served part whose subject is systems, exchange formats and identifiers may name them. | Practice is extracted, not copied, and what is attributed once cannot leak into a commons' words. | ip |
| R15 | MUST | An offer holds no customer or organisation name, no personal contact datum, no commercial or account data, no credentials and no proprietary structure or text. | An offer that carries someone else's property or data is a liability, not an offer. | private |
| R16 | MUST | Commons Essentials is the discipline's `specs/`, released from `commons.o` through a library, free and with no operator's content, and a commons installs it into its own `specs/` (CORE R26). | Every commons holds the discipline on equal terms, and no operator speaks through it. | review |
| R20 | MUST | A commons follows the version of the extension it holds: it sees when a newer release exists, reads which parts it changed, and takes it up, with its rename map, by a decision of its own. | An extension offers; a newer offer changes nothing in a commons until the commons decides. | review |
| R21 | MUST | An offer may carry specifications in `offer/specs/`, released with its essentials, each following SPECIFICATION and extending the discipline's specifications without taking any of their ids or superseding any of them, and the fields a kind adds to MODEL's records are declared in the schema of such a specification. | A kind of commons has rules and fields of its own, as readable and checkable as the discipline's, and the shared grammar cannot be played off against itself. | specs |
| R23 | MUST | `adopted_from` names `<library>/<extension>@<version>#<kind>:<slug>`, a step as `#value-stream:<stream>/<step>`, with the version the commons pins and the origin's slug even where the commons renames the record, and the archetype it names is offered at that version. | The origin is the identity of a binding (MODEL R22) turned outward; a branch or a renamed slug would point at something else tomorrow. | adopt |
| R24 | SHOULD | An offer marks its starting set, the archetypes a commons of its kind begins with, by `start: true`, and the starting set offers every capability its streams bind. | A menu without a beginning is a phone book, or is read as an order to take everything. | start |
| R25 | MUST | The offer is data in `offer/offer.yml`, its id, the kind it is made for, what it gives and what it asks back, while its version is the release, its licence the `[domain].core`'s `LICENSE`, its gaps the archetypes it does not offer, and its page a view generated from it and its records, never written by hand. | An offer stated once as data can be read, compared and rendered; one stated as a page cannot. | offer |
| R28 | MUST | A commons departs from what it adopted only visibly: the difference between an adopted record and its origin is derived and never listed by hand, tells a field written as `null` from an absent one, and reports an adopted Body's unresolved mandate or place and an adopted Post no one serves, while a specification the commons adapts is its own (SPECIFICATION R20). | The commons recognises in its own model what it took and what it changed, without a second list that drifts. An offered Body is a form: its mandate here and who serves its Posts are the commons' own acts. | adopt |
| R29 | MUST | A CORE whose purpose is to make and maintain a domain is a `[domain].core`: it is checked as a CORE in full, has a holder and a `LICENSE`, installs Extension-Builders as its primary, keeps its offer in `offer/` and its research whole in `knowledge/`, and releases nothing of its research. | A domain is kept true by people with a mandate and a record of their own, and what it rests on stays where it is maintained. | offer |
| R30 | MUST | A `[domain].core` keeps its research whole in `knowledge/`: every source of it holds what `core-knowledge` R19 requires of a standard's source and names the offered records it informs, what no standard reaches is held as claims with their standing, and a third-party term translated into Commons language is recorded with the records translated from it. | A source is trusted only after it survived the second lens, and a renamed term must be traceable to what it shaped. | research |
| R31 | MUST | Every offered record binds its sources as `core-knowledge` R20 says, at the edition in force today, and a release carries these bindings and an attribution list `sources.yml` with each bound source's designation, edition, jurisdiction and relation, never the research behind them. | The steering loops run in the adopting commons and must know what they watch; the evidence for a source stays with its maintainers. | binds |
| R32 | MUST | An extension is released only through a library's gate, which a `[domain].core` runs beforehand as the same code and which asks conformance of anyone who makes one, never permission, and its release record `release.yml` names the extension, the library, the version, the `[domain].core` and commit it was made from, the gate's result, the parts that changed and, for a major version, the rename map. | Knowledge spreads at the speed of trust, and a release that names where it came from and what it changed can be trusted and followed. A community passes locally exactly what the library checks. | release |
| R33 | MUST | Extension-Builders is the discipline's extension for making a `[domain].core`: it is made in `commons.o`'s `offer/` and released through a library; it offers the research commons' own model; and it carries no rule or check of its own, which come with Commons Essentials as one code base with the library's gate. | A community builds a domain the way the discipline does, and the rules change in one place. | review |
| R34 | MUST | Selecting a value stream to adopt prepares one coherent adoption proposal, holding the stream, the capabilities its steps bind with their parent chain, and the entities they reference, reusing what the commons holds adopted from that origin and showing optional choices, declined records, collisions with records the commons holds of its own, and unresolved bindings; a person accepts the package deliberately, and a dependency left open on purpose stays visible. | A stream adopted without what it binds leaves a model of open references nobody chose; a package accepted as a whole is a decision, and an open end that is shown is one the commons can close. | adopt |
| R36 | MUST | An extension is cut along its value model and is jurisdiction-neutral: an offered record binds only sources that no jurisdiction enacts, `global`, neither the offer nor its release carries a jurisdiction overlay, and a jurisdiction's law stays in the `[domain].core`'s own `knowledge/` (`core-knowledge` R20). | Law that holds in one place is no part of a model of a kind of commons, and what a commons does with its own law belongs to its own CORE. | binds |

R2, R6, R10, R17, R19, R22, R26, R27 and R35 are merged into the requirement that now holds them (part 8), as R5 and R18 were retired before; none is reused.

## 5 · Structure

The schema is `schemas/extension.schema.json`: the offer, and in `$defs` the release record. A `[domain].core` is checked as a CORE first (CORE, MODEL), so this part names only what it adds.

**The `[domain].core`**

| Place | Holds |
|---|---|
| `.commons/commons.yml` | as every CORE's, with a `holder`; `extensions` pins Commons Essentials and `<library>/extension-builders` as the primary |
| `registry/`, `operations/` | its own model: the research commons, adopted from Extension-Builders |
| `knowledge/sources.yml` | its research, each source in the form of `core-knowledge` R19 (R30); `knowledge/claims.yml`: claims for the negative space, `about` the records they ground; the translation record of third-party terms |
| `offer/offer.yml` | `id` (the domain), `kind`, `gives`, `asks` |
| `offer/registry/` | the essentials' archetypes, one per file, in MODEL's element folders; `start: true` marks the starting set; `binds` per record |
| `offer/loops/` | one steering loop for every family the offer's streams name, `_family.<family>.loop.yml`, and operating loops per value stream; a family it does not reach is a gap (R8) |
| `offer/specs/` | the kind's specifications; the schema of one declares the fields the kind adds |
| `offer/enhanced/` | the served depth, patterns and studies; dense where needed, every record with a stable `id` |
| `workshop/` | open research, studies and build scripts; never released |

There is no `offer/overlays/`. The law of a jurisdiction, the EU's included, stays in the research, in `knowledge/jurisdictions/<jurisdiction>.yml` (`core-knowledge` R20, R36).

**The release**, as a library holds it and a commons installs its essentials: `release.yml`, `offer.yml`, `sources.yml` (the attribution list), `registry/`, `loops/` and `specs/`. A library's layout is LIBRARY's.

**In the commons.** `commons.yml` pins the extension as `<library>/<extension>` with its version and `primary: true`, and names each library it installs from as `libraries: {<id>: <owner>/<repo>}` (CORE R1). The essentials lie in `extensions/<library>/<extension>/`. An adopted record carries `adopted_from: <library>/<extension>@<version>#<kind>:<slug>`. A `not-selected` event carries `archetype:` in the same form, its reason as `title`, who acted and the Story it came from (FLOW).

## 6 · Checks

`tools/check_extension.py <domain.core> …` reads `[domain].core`s, each first with `check_core.py`. It is the same code as a library's gate (R32). `--core <core>` reads a commons that installs a released extension. It reports **fail**, **should** or **gap**, exits with 1 only on a fail, and lists each adopted record as *unchanged* or *adapted*, with the fields it changes. `tools/propose_adoption.py <core> <stream>` prepares the adoption proposal of R34 and, accepted by a person, writes it all or nothing. `tools/take_update.py <core> --from <release> --to <release>` takes up a newer release by the commons' decision (R20), all or nothing, and surfaces every conflict instead of overwriting it.

| Check | Tests |
|---|---|
| `core` | the `[domain].core` is a well-formed CORE, read as unmigrated where it is still on an earlier layout (a gap, CORE R4), and its offer's records are in MODEL's grammar and on MODEL's families (R7, R29) |
| `offer` | `offer/` exists; `offer/offer.yml` validates; `LICENSE` exists; a `holder`; Extension-Builders as the primary, else a should (R4, R25, R29) |
| `contents` | at least one value stream, a steering loop for every family its streams name (any other family a gap), every enhanced record with an `id`, no `offer/overlays/`, and no file of the earlier format (R4, R8, R36) |
| `start` | a starting set is marked, and it offers every capability its streams bind (R24) |
| `ip` | no term of a source appears in the offer (`offer/`, its specifications aside), the research, the maker's own model and its workshop not being the offer: its designation, the designation's leading part, a short title in parentheses, its slug and its `terms`; a term with capitals is matched as written, one in lower case in any case; a binding's `source`, which refers to a source by its id, is no naming (R14, R31) |
| `private` | no e-mail address or telephone number in the offer (R15) |
| `specs` | each specification in `offer/specs/` passes `check_spec.py`, and none takes the id of, or supersedes, a specification of the discipline (R21) |
| `research` | every source carries the fields of `core-knowledge` R19, a known relation, both lenses or, for an own source, `standing: design` and a derivation, and informs only records the offer holds; without `knowledge/sources.yml`, a gap; an offered record grounded by no source of a standard (one that informs it or that it binds) and no claim about it is a gap, counted per kind; a source of the relation `own` grounds only through a claim; each scheduled edition has an id of its own and an `in_force` date, and it is reported with the records its currency loop will raise: those binding a part it `affects`, those binding no part, and those it informs without a binding; each `knowledge/jurisdictions/<j>.yml` names its jurisdiction and binds offered records to sources of that jurisdiction at their edition in force (R30, R36) |
| `binds` | every binding names a source of the research at its edition and jurisdiction; a `part`, where given, names a part; no binding names a scheduled edition or a source of any jurisdiction, national or regional, only `global` ones (R36); in a release, an attributed source (R31) |
| `release` | with `--core`: the installed copy has a release record that validates, names the pinned extension and passed the gate (R1, R3, R32) |
| `install` | with `--core`: the pinned extension comes from a library the commons names (`commons-library` unnamed is read as unmigrated, a gap), is installed at its pinned version, and its copy holds no enhanced part, research, workshop or overlay (R12, R36) |
| `adopt` | with `--core`: every `adopted_from` has its form, names the pinned extension and version and an archetype it offers; no archetype is both adopted and not selected; each `not-selected` event names an archetype; the difference to the origin counts a field written as `null` apart from an absent one; an adopted Body without a resolved mandate or place, and a Post no one serves, are gaps; every record an adopted record binds and the commons does not hold is a gap, or a note where a `decision` event names it under `open` (R13, R23, R28, R34) |
| `fit` | with `--core`: exactly one extension, as the primary, beside the discipline's specifications (R9) |
| `review` | a review by the human accountable for this specification's mandate, against the Why of R11, R16, R20 and R33, and of the judgements no tool makes in R1 (no equality by slug), R9 (the routing's reasons), R13 (what returns), R25 (the page generated) and R32 (no permission asked) |

## 7 · Example

**Minimal:** [a `[domain].core` for community gardens](examples/extension/demo.garden.core/offer/offer.yml). It has its own steward, one source with its research, and an offer:
- a starting stream with one step, bound to that source;
- a capability map from L0 to L3;
- one entity and one stakeholder;
- a steering loop for each of the thirteen families.

Its `offer/offer.yml`:

```yaml
id: garden
kind: community-garden
gives: 'A first model of a community garden: how it grows and shares, and who tends it.'
asks: A Body that holds what is adopted, and evidence from the garden's own season.
```

A commons installs its release `commons-library/garden@0.1.0` and adopts the stream unchanged and the gardener renamed as its member. It does not select the plot. This commons is the fixture [`adopts.core`](tools/tests/extension/cores/adopts.core/.commons/commons.yml). `check_extension.py --core` lists the stream as *unchanged* and the member as *adapted: slug, stated_as, title*.

**Complete:** a gap. One family of health taken through Extension-Builders, the gate and an adoption is the work of commons.o#96.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | Commons EXTENSION, in parallel with the `specs/` move, after FLOW | commons.o#90, opened on the word of the human accountable |
| 2026-10-26 | revised | V1: a CORE orients itself on the canon by installing it as extensions and following their versions, taking up a new one by its own decision and departing only visibly (R20); the return flow is GRAPH's. V2: every commons carries Commons Essentials, the grammar and no layer, and beside it exactly one domain extension; one best fit, no layering and no borrowing apply to the domain extension (R9), which narrows the rule of 18 August 2026 (`511a674974`: one pack per instance) to the domain | Holger, commons.o#90, comment 6419482445 |
| 2026-10-26 | adopted | Adopted after the EA's three points and a green check: departures in the place the commons owns, registry or own specifications (R20); content checked, not only paths (R4, the `files` and `commons` checks); halves resolved by identity, direction and compatible version, failing closed (R5, R12) | Holger, commons.o#90, comment 6419891571 |
| 2026-10-26 | revised | condition 4: every extension may carry specifications in its essentials half (R21); a domain specification extends and never redefines Commons Essentials (R22); domain specifications follow SPECIFICATION. R16 keeps the discipline's specifications in Commons Essentials, and the earlier file set now allows `specs/` in any essentials | Holger, commons.o#90, comment 6419956010 |
| 2026-10-26 | revised | Commons Essentials 0.2.0 is commissioned: it carries the discipline's specifications and passes `check_extension.py`; D4-CE builds and releases it in the Workshop, D1-CE gives its content, and publishing it outside the Workshop needs the human accountable's word. CORE gains the structure key `extensions` (CORE R27) | Holger, commons.o#90, comment 6419928036 |
| 2026-10-26 | revised | **Draft, contingent on the probe and not decided.** An extension is a CORE whose registry is a menu of archetypes; no manifest, no halves (R5 and R18 retired, ids not reused); public parts installed, every other part served; `adopted_from`; `not-selected`; versions followed by decision; departures derived; the offer as data and its page a view; a starting set; reception opt-in; Commons Essentials as the discipline's `specs/` at a tag | Holger, commons.o#90 (the principle, contingent on the probe 6421206970; not yet decided) |
| 2026-10-28 | revised | **Draft until E3.** E1, L1: a `[domain].core` is where a domain is made and maintained, may be private, offers in `offer/` apart from its own model; an extension is its released, gated offer, held in a library and installed from it, and the term stays (R1, R4, R12, R29). E2: one extension per `[domain].core` on one version line; *essentials* its installable public part, *enhanced* its served part; the pair rule and double versioning end; a commons installs only the released extension, with the sources each record binds; the research stays whole in `knowledge/` (R3, R12, R14, R27, R30, R31). E5: the record is the unit; served depth may be dense with stable ids (R4). L2: Extension-Builders (R29, R33). L3: prepared for other libraries (`libraries:`, library-qualified ids, the gate again at install), operated first with `commons-library` only. E3: one health family through the builders' path before anything migrates. E4: no release in today's format | Holger, commons.o#90, comments 6464648757, 6464676842 and 6464808164 |
| 2026-10-28 | revised | **Draft until E3.** A steering loop is required for every family the offer's streams name, and a family it does not reach is a gap, so that one family can be offered and proved (R4, R8); a maker on an earlier layout is read as unmigrated, never refused (CORE R4) | on the gate's first run for E3, raised by @D4-CE (commons.o#96); within the decided R8 |
| 2026-10-28 | revised | **Draft until E3.** An edition is bound by a short id, its full title kept once in the source; the second lens's corrections are recorded as `verified.corrected` (R30, R31) | on @DA-Extension's finding in E3 step 3 (commons.o#96, 6466782307); within the decided E2 |
| 2026-10-28 | revised | **Draft until E3.** An edition id names one immutable edition: a new edition is a new id, and the earlier coordinate stays; a designed or synthesised record rests on a claim of its own with its derivation, never on a manufactured binding (R30, R31) | the EA on E3 (commons.o#96, 6467474160); within the decided E2 |
| 2026-10-28 | revised | **Draft until E3.** The check `ip` reads the offer only, as R14 says, and no longer the maker's own model or workshop (part 6) | on the refusal of the second candidate (commons.o#96, 6467535717); within the decided R14 |
| 2026-10-28 | revised | **Draft until E3.** A source of relation `own`, the commons' own synthesis, carries `standing: design` and its derivation instead of the two lenses (R30) | @DA-Extension's question on the EA's advice (commons.o#96, 6467751417); within the decided E2 |
| 2026-10-28 | revised | **Draft until E3.** The updater's two defects corrected: a rename never takes the place of another record and two renames never meet, checked before any write; references follow MODEL's own bindings, the step bindings and a kind's declared `x-refers`, not a second grammar (part 6) | the EA's review of the E3 account (commons.o#96, 6468579455) |
| 2026-10-28 | revised | Q-a: selecting a value stream prepares one coherent adoption proposal, accepted deliberately, with what is left open visible (R34). Q-b: the derived difference tells a written `null` from an absent field, and an adopted Body's unresolved mandate or place, or a Post no one serves, is reported (R35) | Holger, commons.o#96, comment 6468782933 |
| 2026-10-28 | revised | the adoption proposal checks every target before writing, all or nothing with the event last, and lists a collision with an own record in the proposal itself (R34, part 6) | the Office's second check of `62930c2` (commons.o#96) |
| 2026-10-28 | revised | D4-CE's coverage reading carried: an offered record grounded by neither a source nor a claim is a gap per kind; `ip` reads a source's terms; a release carries `overlays/` (part 5, part 6) | commons.o#96, step 5, merged from `d4-ce/e3-gate` with D4-CE |
| 2026-10-28 | adopted | **Adopted with open conditions** after E3 as a bounded experiment: the [domain].core and offer architecture kept; the conditions are named in part 6, and no pack migrates until they are met | Holger, commons.o#96, comment 6468782933 (Q-d) |
| 2026-10-28 | revised | a scheduled edition, enacted and not yet in force, has its place in the source with its `in_force` date and the parts it `affects`, so that the currency loop raises it before the date; a binding may name the `part` it rests on, and never binds a scheduled edition (R30, R31, part 6) | on @DA-Extension's two gaps (commons.o#96, 6469709788), proposed in #90 (6469769051); merge on Holger's word |
| 2026-10-28 | revised | **Overlays out of the extension**: an extension is cut along its value model and jurisdiction-neutral; it binds no national source and carries no overlay; national law, its editions and scheduled changes stay in `knowledge/` (R36; part 5 retires `offer/overlays/` and the release's `overlays/`; part 6) | Holger, commons.o#91, comment 6470680520 |
| 2026-10-28 | revised | jurisdiction-neutral read as Holger's cut says: the EU is a jurisdiction too, so an offered record binds only `global` sources; the bindings of a jurisdiction live in `knowledge/jurisdictions/<j>.yml`, @DA-Extension's form, as research (R36, part 5, part 6). A reading D1 made, named for Holger to overrule | Holger, commons.o#91, comment 6470680520; the Office's question and DA's form, relayed in #96 |
| 2026-10-28 | adopted | **The revision adopted:** R36 (an extension jurisdiction-neutral, binding only `global` sources, no overlays; national and EU law in `knowledge/jurisdictions/<j>.yml`, D1's reading of the EU not overruled), R30 `scheduled` and R31 `part`; with R31 scoped to current applicability, so that a world CORE may bind the edition of its target date (the EA, 6470773876). CORE R27's `record` lands with LIBRARY | Holger, commons.o#90, comment 6472435387 |
| 2026-10-28 | revised | **Draft until E3.** Taking up a newer release by decision, with a tool: three-way per record, renames followed or surfaced, local changes kept, conflicts never overwritten (R3, R20, R28, part 6) | the EA's third point on E3 (commons.o#96, 6466512297); within the decided R20 |

| 2026-10-28 | commissioned | KISS pass: R2 merged into R1, R6 into R7, R10 into R9, R27 into R12, R26 into R13, R22 into R21, R17 into R25, R35 into R28, R19 into R32; R30, R31 and R36 keep their goal while the form of a standard's source and of a binding moves to `core-knowledge` R19, R20; R12, R16 and R33 name a library the commons names instead of a built-in one; the open conditions of the adoption and the migration plan move to the work item (commons.o#96), and the map of the earlier file set to the carry-over; the carry-over moves to `carry-over/extension.md`. Written for adoption; not yet adopted | Holger, commons.o#98 ("Ja, alle") |
| 2026-10-28 | adopted | The KISS revision adopted; the open conditions and the migration plan are kept in commons.o#96 | Holger, commons.o#98, comment 6474773388 |
**Rests on:**
- one pack per commons, with no base pack and no layering (18 August 2026, commit `511a674974`);
- one canonical Commons Essentials foundation, loaded first during boot (E2), qualified identities (E5), and Commons extensions free, with no operator content (E6), all of 18 October 2026;
- the families identical in every pack (MODEL R3);
- installed specifications in `specs/` (CORE R26);
- the positions of commons.o#90: D0-CE's words (6420921361), D2-CE's FLOW (6420909990), D3-CE's three conditions (6420897885), D4-CE's means (6420919514), the Model Engine's facts (6420933164), @DA-Extension's points (6442218005, 6462655214), and D1-CE with D4-CE on the delivered unit (6462683977).

What this specification supersedes, and what it carries of it, is in [`carry-over/extension.md`](carry-over/extension.md).
