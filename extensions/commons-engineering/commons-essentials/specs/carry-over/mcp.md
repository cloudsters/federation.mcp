# mcp · carry-over

What [Commons MCP](../mcp.md) supersedes, and what it carries of each text (SPECIFICATION R26).

**Supersedes**, each text in part. What is not carried or dropped below stays in force in its text until the specification named under *Not superseded here*.

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | a commons' MCP is the service it runs over its own graph, one per commons; one role, two postures, not two kinds (§1) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | it serves the graph and is never a second author of the model (§1) | carried | R20 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | the delivered numbers of patterns and lighthouses, cross-domain at scale (§1.1) | dropped |  | a measured state, never a requirement | Holger, commons.o#87, comment 6413669417 (SPECIFICATION R27) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | model-agnostic, tool-native and composable over the protocol (§1.2) | carried | R22 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | structure first: graph traversal, search one tool among many (§1.3) | carried | R2 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | the free tier: all knowledge navigable, revenue from tools (§1.4, §6.2) | dropped |  | what a commons serves to whom is its grant; an operator's terms are not the discipline's | Holger, 18 October 2026 (`_drafts/auftrag_01/DECISIONS_HOLGER.md`, E6) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | alignment, not grounding: the canon is a reference, reality is Fabric's (§1.4) | dropped |  | expected beside observed is `core-knowledge`'s (R16), served through `answer` | Holger, commons.o#98 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | remote first, local as fallback (§1.4) | dropped |  | local is a real small-tier path with the same semantics, as a CORE works offline first | Holger, commons.o#95, comments 6438391848 and 6464307584 (`core` R28, R32) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | three channels: one shared Commons MCP, a Blueprint MCP per instance, Fabric MCPs (§2.1) | dropped |  | one shape at every level; Fabric is `fabric` | Holger, commons.o#94, comment 6436299151 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | private data flows to the shared service only as anonymised insight, never through the protocol (§2.2) | carried | R19 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | H2H, H2A and A2A as interaction modes (§2.3) | carried | R2 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | the five layers: git, ETL, Neo4j with vectors, the server, the Weaver; costs and hosting (§3) | dropped |  | storage and engines are `graph-engine`'s and the operator's; costs are measurements | Holger, commons.o#93, comment 6464338661 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | git is the source of truth; everything downstream is derived, rebuildable, disposable (§3.1) | carried | R20 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | the Weaver's syntheses return only as pull requests curated by people (§3.5) | carried | R12 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | the tool catalogue of navigation, lighthouse, diagnostic, engagement, meta and extension tools (§4.1–§4.6) | dropped |  | a few generic tools mapped onto one pipeline; the domain lives in the model, and the earlier service was the federation's offer, never the commons' own MCP | Holger, commons.o#93, comment 6424755304 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | the own-model tools of a house, the same role turned inward (§4.7) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | `record_adoption` writes into the instance (§4.7) | dropped |  | adopting is the commons' decision, recorded by it, never through the MCP | Holger, commons.o#90, comment 6419482445 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | the data layer: three knowledge layers, orbit-to-layer mapping, Neo4j model, vectors (§5) | dropped |  | the graph's sources and nodes are `graph`'s; the layers and the chain are retired | Holger, 15 October 2026 (`_drafts/target_architecture.md` §11: the chain retired) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | access tiers mapped to one federation's rings, audience manifests, revenue routing, standard offers (§6) | dropped |  | closeness to the model is the shell; an operator's memberships and prices stay with the operator | Holger, 24 October 2026 (commons.o#80, S1–S7) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | identity from the organisation's provider; the server holds no password (§7, §7.1) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | entitlement from group claims; the server holds no user list (§7, §7.1) | dropped |  | the commons lists its users by shell in `access.yml`, and the platform's teams are generated from it | Holger, commons.o#100 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | OAuth with the MCP as resource server, validating tokens for itself (§7.2) | carried | R22 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | the Organisations and tier-group tables (§7.3–§7.5) | dropped |  | `access.yml` lists a commons' own users by shell | Holger, 24 October 2026 (commons.o#80, S1–S7); commons.o#100 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | a service account for one service calling another (§7.6) | carried | R19 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | revocation by the identity provider and on a contract's end (§7.7) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | a visible drop to a lower grant, saying what still works (§7.8) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | gating by tool, rate limits per organisation (§7.9) | carried | R8 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | no private data and no identity in the service beyond a hashed audit; a retention for audit (§7.10) | carried | R21 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | timeouts and truncation of large traversals (§7.11) | carried | R8 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | the phases A–C (§8) | dropped |  | a dated status, never a requirement | Holger, commons.o#87, comment 6413669417 (SPECIFICATION R27, R28) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MCP_SPEC.md` | a writing tool must carry who decided, on what, the decider not the producer, reconstructible without the interface (§9) | carried | R12 |  |  |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | it serves the instance's graph and never authors the graph (§1) | carried | R20 |  |  |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | one per sovereign instance, owned and operated by it (§1, §2) | carried | R22 |  |  |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | customer-built and customer-hosted as the only model (§2.1) | dropped |  | local or hosted, the same code; where it runs is the commons' choice | Holger, commons.o#93, comment 6424755304 |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | public knowledge flows in; private data never flows out (§3.2, §7.3) | carried | R19 |  |  |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | git is authoritative; the index is a rebuildable cache (§3.3, §5.4) | carried | R20 |  |  |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | three deployment shapes with costs (§3.4) | dropped |  | an operator's choice and a measurement | Holger, commons.o#87, comment 6413669417 (SPECIFICATION R27) |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | the merged graph of public and private, private adoption edges (§4.1, §5.3) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | adoption tools and `record_adoption` (§4.3) | dropped |  | adopting is the commons' decision; the MCP proposes | Holger, commons.o#90, comment 6419482445 |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | enrichment calls the shared service and overlays the instance (§4.4) | carried | R19 |  |  |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | the difference between two snapshots (§4.5) | carried | R2 |  |  |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | activation by engagement stage, scaffolded from day one (§6) | dropped |  | every CORE can serve itself from the start; an engagement stage is no condition | Holger, commons.o#93, comment 6424755304 |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | spec versions in a config file, migrations (§6.3) | dropped |  | an installed specification is pinned in the lock (`core` R26) | Holger, commons.o#89, comment 6418322780 |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | the organisation's provider decides who signs in (§7.1) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | group claims map to permissions (§7.1) | dropped |  | a user's shell in `access.yml` carries its access | Holger, commons.o#100 |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | the outbound call runs under the service's own identity, never the user's token (§7.2) | carried | R19 |  |  |
| `Commons-Engineering/workshop@main:_specifications/BLUEPRINT_MCP_SPEC.md` | every invocation is logged with caller, tool and a digest, in the owner's environment (§7.4) | carried | R21 |  |  |

**Not superseded here:** `FABRIC_MCP_SPEC` goes to `fabric` (M3); `COMMONS_MCP_ARCHITECTURE_SPEC` is already marked deprecated in favour of `COMMONS_MCP_SPEC` and its companions; the access drafts (commons.o PR #54, branch `d4-ce/access-shells`) are drafts taken up into part 5 and close with this specification; the repository `commons-mcp` and the worker `commons-mcp-worker` are implementations that retire when the MCP built from this specification serves.
