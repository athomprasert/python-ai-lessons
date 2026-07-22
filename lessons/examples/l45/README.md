# L45 example — a tiny Python MCP server + client

Two files that demonstrate the MCP lifecycle end-to-end on your machine:

- `mcp_server.py` — a finished MCP **server** (FastMCP). Exposes one tool
  (`get_order_status`) and one resource (`returns_policy`).
- `mcp_client.py` — an MCP **client** that launches the server, does the
  `initialize → list tools → call tool` handshake. **You finish STEP 3.**

## Run it

```bash
# Install the official SDK (stable v1 line)
pip install "mcp[cli]>=1.27,<2"

# From this folder:
python mcp_client.py
```

The client starts `mcp_server.py` for you (stdio transport) — you don't run
the server separately.

## Success looks like

```
Available tools: ['get_order_status']
Order A100 status: shipped — arriving tomorrow
```

Grey `INFO` lines from the server are normal logging, not errors.

## Verified against

Official MCP Python SDK v1.x (FastMCP + stdio client):
https://github.com/modelcontextprotocol/python-sdk
