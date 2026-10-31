# federation.mcp

The Federation's MCP: serves the canon of Commons Engineering at ROAM and the offer per shell; code and deployment.

Content arrives by pull request only; see [cloudsters/cloudsters.o#59](https://github.com/cloudsters/cloudsters.o/issues/59).

It answers at `https://mcp.cloudsters.net/federation` (H3).

| Path | What |
|---|---|
| `.commons/commons.yml` | the pin: `commons-engineering/commons-essentials` 0.2.0, from the library `commons-engineering` in `cloudsters/federation.library` |
| `.commons/lock.yml` | generated at install: origin and record digest, as the library's index gives them (`library` R9) |
| `extensions/commons-engineering/commons-essentials/` | the installed release copy, never edited; the service runs its `specs/tools/serve_mcp.py`, the same code on every level (`mcp` R1, R22) |

**What is never here:**
- `access.yml` and its users. The Federation's access lives in the CORE this MCP serves, `cloudsters/cloudsters.o`, under `.commons/` (`mcp` R1).
- Any credential. The deployment credential is held apart from the code (H4).

Run the tools with `python -B`, so that no bytecode is written into the installed copy.

## The Worker (H4)

`federation-mcp` is a **Cloudflare Python Worker** (Pyodide, Python 3.14), on the route `mcp.cloudsters.net/federation*`. It is no port: it runs the released `serve_mcp.py` unchanged, behind a thin transport.

| Path | What |
|---|---|
| `worker/src/mcp_http.py` | the transport: MCP Streamable HTTP, JSON-RPC over `POST /federation`, answered with JSON |
| `worker/src/main.py` | the Worker's entry |
| `worker/wrangler.toml` | name, route and the `python_workers` flag; no credential |
| `deploy/build.py` | packs the served CORE (the installed copy, the pin and lock, and `served/`) into `worker/src/core_bundle.py`, which is build output |
| `served/` | the users-free access and the register of what is served at the first deployment |
| `tests/test_transport.py` | the calls a session makes, run over the built CORE |
| `.github/workflows/check.yml` | the checks, on every pull request |
| `.github/workflows/deploy.yml` | the deployment on every merge to `main`; it reads only the secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`, and does nothing while they are unset |

**Locally:**
- `python -B deploy/build.py`, then `python -B tests/test_transport.py`;
- `cd worker && uv run pywrangler dev` serves it at `http://127.0.0.1:8787/federation`.
