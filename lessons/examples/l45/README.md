# L45 example — a tiny Python MCP server + client

Two files that demonstrate the MCP lifecycle end-to-end on your machine:

- `mcp_server.py` — a finished MCP **server** (FastMCP). Exposes one tool
  (`get_order_status`) and one resource (`returns_policy`).
- `mcp_client.py` — an MCP **client** that launches the server, does the
  `initialize → list tools → call tool` handshake. **You finish STEP 3.**

## Run it

This project already has the `mcp` SDK installed in its virtual environment
(`~/ai/claude/projects/python/.venv`). On this machine the command is `python3`
/ `pip3` (there is no bare `python` / `pip`), so the simplest path is to use the
venv's own interpreter — no install step needed:

```bash
# From this folder:
~/ai/claude/projects/python/.venv/bin/python mcp_client.py
```

Prefer activating the venv? Then plain `python` works for the rest of the session:

```bash
source ~/ai/claude/projects/python/.venv/bin/activate
python mcp_client.py        # run the demo
deactivate                  # when you're done
```

Only if you're on a fresh machine WITHOUT the venv, install the SDK first
(note: use `pip3`, not `pip`):

```bash
pip3 install "mcp[cli]>=1.27,<2"
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
