# graph · carry-over

What [Commons GRAPH](../graph.md) supersedes, and what it carries of each text (SPECIFICATION R26).

**Supersedes**, each text in part. What is not carried or dropped below stays in force in its text until the specification named under *Not superseded here*.

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | the graph is a derived view; every node points at a source elsewhere; it holds pointers and relations (§1) | carried | R6 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | every commons has one graph, derived from its own sources; one commons, one graph, its parts never separate graphs (§2) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | the scaffolding travels the chain from the hull (§2) | dropped |  | the chain is retired; the area and its rules come with the CORE and its specifications | Holger, 15 October 2026 (`_drafts/target_architecture.md` §11: the chain retired) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | the layers Model, Knowledge, Engagement and Work share one identity space (§3) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | the graph never holds the body of anything that lives elsewhere (§3) | carried | R11 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | no write path into the graph; a correction is made at the source (§4.1, §5) | carried | R4 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | a node deleted at its source disappears (§4.2) | carried | R6 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | what enters from a sensor is the reading, never the record (§5) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | measured, unwatched and unsighted are never conflated; where the graph cannot see, it says so (§7) | carried | R13 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | a graph that agrees with its sources is aligned, not grounded (§7) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | every work node carries an edge to the element it changes (§8) | carried | R6 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | it computes reach, dependency, coverage and order, never priority; order in the plural (§9) | carried | R15 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | relations between graphs are typed and without ranking; a coupling is agreed only where both sides assert it (§10) | carried | R17 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | permissionless observation, sovereign operation (§10) | carried | R17 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | aggregation reads; it never copies (§10) | carried | R18 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_GRAPH_MANIFEST.md` | commercial metadata, account data and credentials never enter the graph (§11) | carried | R11 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | one word, one meaning: knowledge, engagement, loop and evidence graph are readings of the one graph (§1) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | `.graph/` is a root directory of every CORE; its content is derived per commons (§2) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | a stable identity that encodes no path, and an address in the canon (§3) | carried | R5 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | node types are fixed per layer; a graph that invents a node type is not comparable (§4) | carried | R5 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | a work node holds nothing of its body or discussion (§4) | carried | R11 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | the families are given structure, never absorbed into a computed grouping; a grouping spanning two is a signal (§4a, §7) | carried | R5 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | edge types and their directions follow the specification that defines them (§5) | carried | R6 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | `couples-at` is asserted per side (§5, §11) | carried | R17 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | the sources of derivation: registry, packs and patterns, engagement, the board, readings (§7) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | a stale layer is served with its staleness stated; every response carries the age of its oldest part (§7, §10) | carried | R12 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | each derivation records per element measured, unwatched or unsighted (§7) | carried | R13 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | blast radius, communities, blockage, coverage, order as a set (§9) | carried | R15 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | an aggregate carries the union of its members' unsighted states (§11) | carried | R18 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | aggregation reads under each member's authority and never copies (§11) | carried | R18 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | ingestion: no commercial or account data, no credentials, no body text, no node without a resolvable source (§12) | carried | R11 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_KNOWLEDGE_GRAPH_SPEC_DRAFT.md` | agents write relationships inferred from content into the nodes (§12.2) | dropped |  | a computed relation reaches a source only as a proposal a person takes in | Holger, commons.o#95, comment 6438391848 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_KNOWLEDGE_GRAPH_SPEC_DRAFT.md` | relationships are typed and directional (§4) | carried | R6 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_KNOWLEDGE_GRAPH_LAYERS_DRAFT.md` | an agent sees one merged graph over the kernel, the extensions and the instance (§6) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_KNOWLEDGE_GRAPH_LAYERS_DRAFT.md` | domain and game are permissionless, operations sovereign; identities survive the handover (§7.3, §7.4) | carried | R17 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | several commons on the same reality; the same entity seen through several lenses (§1.2, §1.5) | carried | R5 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | every entity is potentially a commons with its own constellation (§1.4) | carried | R17 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | local detail stays local; only aggregation and learning flow upward (§1.6, §5.3) | carried | R18 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | broadcasting is sovereign and sends a signal, never private data (§5.4) | carried | R18 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | an agent reads another commons of a portfolio only where its human grants access (§10.3) | carried | R17 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | `.graph/` ships in the fork; its content is derived and never forked (§2.1) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | cross-namespace reading only where the human grants access (§6.7) | carried | R17 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | frontmatter references form a graph read in both directions; the files stay authoritative (§8.2) | carried | R6 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_EXTENSION_MANIFEST.md` | what a commons measures travels back; knowledge does not only flow outward (§9) | carried | R18 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | the graph is fractal: every stakeholder is a system, coupled at a shared touchpoint (§2) | carried | R17 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | the graph is fractal; a shared touchpoint is the common edge of two graphs (§3.2) | carried | R17 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | two coordinates: an own identity stable across slices, an address in the canon (§3.3) | carried | R5 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | a delta is a list over stable identities (§3.4) | carried | R16 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | the present is the last commit (§3.4) | dropped |  | the CORE holds the near future; comparing commits shows how the model changed, not how reality drifted | Holger, commons.o#89, comment 6415733592 |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | the loop graph is derived, never drawn; blast radius and epics read from it (§10, §11) | carried | R15 |  |  |
| `Commons-Engineering/commons-graph@main:README.md` | a directory over sources; a node is referenced by its address, never copied (decided 15 October 2026) | carried | R2 |  |  |
| `Commons-Engineering/commons-graph@main:README.md` | what never enters: authoring evidence, commercial metadata, account data, production scripts | carried | R11 |  |  |

**Not superseded here.** These parts of the texts above stay in force where they are until the specification named adopts or drops them:

| Text | Parts | Belongs to |
|---|---|---|
| `COMMONS_GRAPH_MANIFEST.md` | §6 (loops feed it), §11 (what may be served) | `flow`; `mcp` |
| `COMMONS_GRAPH_SPEC.md` | §2 and §6–§7 on derived records, provenance, rhythm and regeneration | `graph-engine` |
| `COMMONS_GRAPH_SPEC.md` | §4a.1–§4a.3 (ratifying a membership, a pattern in no family, names and slugs), §8 (loop emission), §10 (serving roles) | `library`; `flow`; `mcp` |
| `COMMONS_KNOWLEDGE_GRAPH_SPEC_DRAFT.md`, `COMMONS_KNOWLEDGE_GRAPH_LAYERS_DRAFT.md` | node types, governance hierarchy, consistency rules, change routes, layer precedence, collections, O4 served | `specification`, `core`, `flow`, `extension`, `library`, `mcp` |
| `COMMONS_CORE_MANIFEST.md` | §1.3 (the chaordic principle), §5.4 (the broadcast levels), §10.3 (building a portfolio) | `core`; `mcp`; — |
| `COMMONS_LOOPS_MANIFEST.md` | §11 (the backlog, its evaluation and roles) | `flow` |
| `commons-graph@main:README.md` and `sources.yml` | the federation's own sources, its rings and who may read it | the federation's graph, one instance of this structure |
