"""main.py — the Cloudflare Worker `federation-mcp`: a Python Worker that answers at mcp.cloudsters.net/federation and
hands each request to mcp_http, which runs the released serve_mcp.py unchanged."""
from urllib.parse import urlparse

from workers import Response, WorkerEntrypoint

import mcp_http


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        body = await request.text() if request.method == "POST" else ""
        status, headers, text = mcp_http.handle(request.method, urlparse(request.url).path, body)
        return Response(text, status=status, headers=headers)
