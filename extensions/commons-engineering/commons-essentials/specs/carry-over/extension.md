# extension · carry-over

What [Commons EXTENSION](../extension.md) supersedes, and what it carries of each text (SPECIFICATION R26).

**Supersedes**, each text in part. What is not carried or dropped stays in force in its text until the specification named under *Not superseded here*.

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | an extension is a named body of value-creation knowledge, offered in the shared shape (§1) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | a pack proposes, a commons decides; adoption is not inheritance; a decline is recorded (§2) | carried | R13 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | essentials travel with the CORE, enhanced is served (§3) | carried | R12 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | all four domains ship with every fork (§4) | dropped |  | a commons holds exactly one domain extension | Holger, 18 August 2026 (commit `511a674974`: one pack per instance, no base pack, no layering, fail closed) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | the standard is not renamed; a commons' word is mapped onto it (§5) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | anyone may publish; conformance, not a fee, is asked (§6) | carried | R32 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | what an extension owes: element structure, value model, entity model, loops, template, identity and sources (§7) | carried | R4 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | a pack without template, loops or element shapes has a gap, not a licence (§7) | carried | R8 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | an extension never writes into an instance or another provider's pack (§8) | carried | R13 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | no proprietary structure, no sources' words in the models, no commercial data or credentials (§8) | carried | R15 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | an extension carries the domain model, entities, record shapes, loops and template, never the commons (§1) | carried | R4 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | `manifest.yml` is the only file a CORE needs to read a pack (§2.2) | carried | R25 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | one canonical file set, identical across domains, in two halves (§2.2) | dropped |  | one extension on one version line; *essentials* and *enhanced* are its parts, by access class | Holger, commons.o#90, comment 6464676842 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | `MANIFEST.md` and the PDF are generated, never edited (§2.2) | carried | R25 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | the value model's dimensions and families are generated from the canon; streams, steps and the map L0–L3 are the pack's (§2.2) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | one model, two depths: every enhanced node addresses an essentials node, and essentials never depend on enhanced (§2.2) | carried | R4 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | a manifest-only pack is structurally valid (§2.2) | dropped |  | an incomplete extension fails closed | Holger, 18 August 2026 (commit `511a674974`: one pack per instance, no base pack, no layering, fail closed) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | the identity fields `pack`, `provider`, `version`, `title`, `description` (§2.3) | carried | R25 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | `kind: role`, a pack for a role or membership beside the domain pack (§2.3, §4.4) | dropped |  | a second installable beside the domain is layering; the only other extension is Commons Essentials | Holger, 18 August 2026 (commit `511a674974`: one pack per instance, no base pack, no layering, fail closed) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | `dependencies` resolved at install (§2.3) | dropped |  | one extension has no halves to resolve | Holger, commons.o#90, comment 6464676842 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | `license` an SPDX value (§2.3) | carried | R29 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | the catalogue may list `specs` (§2.3) | carried | R21 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | `standards:` the only place for external references (§2.3, §2.5) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | no manifest field is a count (§2.3) | carried | R25 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | the models are English Commons language; a commons' words arrive as `stated_as` (§2.5) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | no slug, title or summary in a model names a standard, statute, framework, vendor or product (§2.5) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | the enhanced body may name the practices and systems behind solutions (§2.5) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | archetypes only: no named individual in any model or element library (§4.1, §5.2) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | without a blueprint template a commons of the domain cannot produce a briefing (§4.1) | carried | R25 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | SemVer, with MAJOR for renamed or removed elements (§4.2) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | breaking changes announced by version and changelog, never by deprecation fields (§4.2) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | pre-loading the essentials of all four domains, and a `base` pack (§4.3, §6) | dropped |  | a commons holds exactly one domain extension, and there is no base pack | Holger, 18 August 2026 (commit `511a674974`: one pack per instance, no base pack, no layering, fail closed) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | install reports what was declared but not delivered, and goes on (§4.4) | dropped |  | an incomplete extension fails closed | Holger, 18 August 2026 (commit `511a674974`: one pack per instance, no base pack, no layering, fail closed) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | the agent asks before upgrading an incompatible installed version (§4.4) | carried | R13 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | a commons installs exactly one domain pack (§4.4) | carried | R9 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | every commons installs the pack of the commons it belongs to (§4.4) | carried | R9 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | a commons spanning several domains is several COREs (§4.4) | carried | R11 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | no pack borrows from another; the two halves of a pack are one pack (§4.4) | carried | R8 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | an update never overwrites what the commons wrote; differences are surfaced and decided (§4.5) | carried | R13 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | content conforms to the grammar before publication (§5.1) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | the limits of the stakeholder register may not be relaxed by any pack (§5.1) | carried | R15 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | conformance errors: manifest, SemVer, paths resolve, family universality, file set, model language, steps bound to L3 with parents (§5.2) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | loop coverage and dependency resolution are warnings only (§5.2) | dropped |  | a missing file or dependency fails closed | Holger, 18 August 2026 (commit `511a674974`: one pack per instance, no base pack, no layering, fail closed) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | a structure proven universal may be lifted into the canon (§7) | carried | R7 |  |  |
| `../commons/specs/PACK_SPEC.md` | packs deliver knowledge to a Commons OS instance (§1) | dropped |  | Commons OS is retired | Holger, 28 July 2026 (glossary `rejected.yml`: Commons OS) |
| `../commons/specs/PACK_SPEC.md` | the content of a pack is its provider's IP (§1) | dropped |  | extensions are free of IP, and Commons extensions are free | Holger, 18 October 2026 (`_drafts/auftrag_01/DECISIONS_HOLGER.md`, E2 and E6) |
| `../commons/specs/PACK_SPEC.md` | only `manifest.yml` is required; the internal structure is free (§2.2) | dropped |  | the places of a CORE (R4) | Holger, 18 August 2026 (commit `511a674974`: one pack per instance, no base pack, no layering, fail closed) |
| `../commons/specs/PACK_SPEC.md` | the identity fields `pack`, `provider`, `version`, `title`, `description` (§2.3) | carried | R25 |  |  |
| `../commons/specs/PACK_SPEC.md` | `patterns: int` must match the file count (§2.3) | dropped |  | no manifest field is a count | Holger, 18 August 2026 (commit `511a674974`: one pack per instance, no base pack, no layering, fail closed) |
| `../commons/specs/PACK_SPEC.md` | SemVer (§4.2) | carried | R3 |  |  |
| `../commons/specs/PACK_SPEC.md` | updates by `git pull upstream` from the commons-os template (§4.5) | dropped |  | there is no upstream chain | Holger, 15 October 2026 (`_drafts/target_architecture.md` §11: the chain retired) |
| `../commons/specs/PACK_SPEC.md` | all four domain packs and `base` ship with every fork (§6) | dropped |  | a commons holds exactly one domain extension, and there is no base pack | Holger, 18 August 2026 (commit `511a674974`: one pack per instance, no base pack, no layering, fail closed) |

**Not superseded here**

| Text | Rules | Stays until |
|---|---|---|
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | §9 (the return path: what a commons measures travels back) | graph |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | §2.1, §2.2 (pack locations, `pack-naming.yml`), §2.3 (`status`), §2.4 (collections), §3 (provider registry and naming), §4.3 (publishing methods) | library |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | §2.3 (`served_to`), §2.2 (served subject to rights), §4.4 (`download_pack`, the fetch wrapper), §4.5 (update channels) | mcp |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | §4.1 (the order of creating a pack), §3.2 (registration through a reviewed change) | flow |
| `../commons/specs/PACK_SPEC.md` | §2.4 (collection index), §3 (provider profiles, registration, naming), §5.1 (pattern format) | library |
| `../commons/specs/PACK_SPEC.md` | §4.3, §4.4 (publishing and install over MCP) | mcp |

**Where the earlier file set went.** Nothing of what the earlier format held is lost; each part has one place.

| Earlier | Now |
|---|---|
| `manifest.yml`: `pack`, `provider`, `title`, `description` | `offer/offer.yml`: `id`; the `[domain].core`'s `holder` and `name`; `gives` |
| `version`, `status`, `changelog`, `created`, `updated` | the release record; *released* is a release that exists; the dates are in the history |
| `license`; `standards` with *derived from · adopt · bind · mirror* | `LICENSE`; `knowledge/sources.yml` (R30) and the release's attribution list (R31) |
| `domains`; `kind`; `half`; `dependencies`; `served_to` | `kind`; essentials and enhanced as parts of one extension, one version; nothing to resolve; the access class (R27, MCP) |
| `min_core_version`; `models`, `loops`, `templates`, `scripts` lists | `structure`; read from the files, never declared |
| `MANIFEST.md` and its PDF | the offer page, a view (R25) |
| `value-model.yml`, `entity-model.yml`, `element-model.yml` (archetypes) | records in `offer/registry/` |
| `capability-map.deep.yml` (L4, L5) and the enhanced depth | `offer/enhanced/`, dense, with stable ids (R4) |
| `element-model.yml`: the fields per element, and its conventions | MODEL's fields where MODEL has them; the rest in the schema of a specification of the offer (R21) |
| `loops/` per family and per value stream; `measures/` | `offer/loops/`; measures with the loops they belong to |
| `blueprint.template.md`; `pipeline/skeletons/`; `pipeline/gate1-evals.overlay.yml` | view definitions; a specification of the offer, with its checks |
| `pipeline/*.pipeline.md`, `_authoring/`, `ip-translation.yml` | `workshop/`; the translation record in `knowledge/` (R30) |
| `sor/` | a served part of `offer/enhanced/` (R14, R12) |
| `patterns/`; `collections/` | unchanged until LIBRARY decides their place |
