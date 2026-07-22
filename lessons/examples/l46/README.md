# L46 example — an MCP server + client over Streamable HTTP

The L45 demo used **stdio** (the client launched the server as a subprocess).
This one uses **Streamable HTTP**: the server runs on its own URL + port, and
the client connects to it — the same model as the MuleSoft MCP server in L44.

- `mcp_http_server.py` — MCP server on `http://127.0.0.1:8000/mcp`. Has one
  finished tool (`get_order_status`) and **one you add** (`cancel_order`).
- `mcp_http_client.py` — connects by URL. Has **one deliberate bug** to fix
  (the HTTP transport yields a 3-tuple, not a 2-tuple) plus a call to your new
  tool to uncomment.

## Run it — TWO terminals

The `mcp` SDK is already in the project venv; use it (bare `python`/`pip`
aren't on PATH on this Mac — see L45).

**Terminal 1 — start the server (leave it running):**
```bash
source ~/ai/claude/projects/python/.venv/bin/activate
cd ~/ai/claude/projects/python/lessons/examples/l46
python mcp_http_server.py
```
Wait for: `Uvicorn running on http://127.0.0.1:8000`.

**Terminal 2 — run the client:**
```bash
source ~/ai/claude/projects/python/.venv/bin/activate
cd ~/ai/claude/projects/python/lessons/examples/l46
python mcp_http_client.py
```

## Success looks like (after both TODOs)

```
Available tools: ['get_order_status', 'cancel_order']
Order A100 status: shipped — arriving tomorrow
Cancel A200: order A200 has been canceled
```

Stop the server with `Ctrl-C` in terminal 1 when you're done.

## Verified against

Official MCP Python SDK v1.x (FastMCP `streamable-http` + `streamablehttp_client`):
https://github.com/modelcontextprotocol/python-sdk
