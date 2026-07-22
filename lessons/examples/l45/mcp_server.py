"""
L45 demo — a tiny MCP SERVER in Python.

This is the "tools/data" side of MCP. It exposes ONE tool (an integration-style
API lookup) that any MCP client — your Python client, Claude Desktop, an IDE —
can discover and call. Compare this to the MuleSoft MCP server you built in L44:
same idea (each function = one tool), expressed in Python instead of a Mule flow.

Run it on its own to sanity-check (use the project venv; bare `python` isn't
on PATH on this Mac):
    ~/ai/claude/projects/python/.venv/bin/python mcp_server.py
(it will wait on stdin — that's correct; the client launches it for you.)

Verified against the official MCP Python SDK v1.x (FastMCP API):
    https://github.com/modelcontextprotocol/python-sdk
"""

# FastMCP is the high-level server class from the official 'mcp' package.
# It turns plain Python functions into MCP tools/resources via decorators.
from mcp.server.fastmcp import FastMCP

# Name your server. Clients see this name during the initialize handshake.
mcp = FastMCP("l45-demo-server")


# @mcp.tool() registers this function as an MCP TOOL.
# - The function NAME becomes the tool name ("get_order_status").
# - The type hints (order_id: str -> str) become the tool's input/output schema.
# - The docstring becomes the tool's description the LLM reads to decide when to call it.
@mcp.tool()
def get_order_status(order_id: str) -> str:
    """Look up the delivery status of a customer order by its ID."""
    # In real life this would be an http request to an order-management API.
    # We mock a small lookup table so the demo runs with no external system.
    fake_orders = {
        "A100": "shipped — arriving tomorrow",
        "A200": "processing — leaves the warehouse today",
        "A300": "delivered on 2026-07-01",
    }
    # dict.get(key, default) returns the default when the key is missing —
    # like Java's Map.getOrDefault().
    return fake_orders.get(order_id, f"no order found with id {order_id}")


# A RESOURCE is read-only context (think GET), addressed by a URI template.
# The {region} in the URI becomes the function argument. The client can READ
# this without it being a callable "action".
@mcp.resource("policy://returns/{region}")
def returns_policy(region: str) -> str:
    """Return the returns policy text for a given region."""
    policies = {
        "sg": "Returns accepted within 14 days with receipt.",
        "us": "Returns accepted within 30 days with receipt.",
    }
    return policies.get(region, "No policy on file for that region.")


if __name__ == "__main__":
    # transport="stdio": the client starts this script as a subprocess and talks
    # JSON-RPC over stdin/stdout. stdio is the recommended default transport for
    # a local server (the other standard transport is Streamable HTTP).
    mcp.run(transport="stdio")
