"""
L46 demo — an MCP SERVER over STREAMABLE HTTP (YOUR turn: add a second tool).

Unlike L45's stdio server (which the client launched as a subprocess), this
server runs as its own long-lived process on a URL + port — exactly like the
MuleSoft MCP server you ran in L44. You start it in ONE terminal; the client
connects from ANOTHER.

HOW TO RUN (terminal 1)
    source ~/ai/claude/projects/python/.venv/bin/activate
    python mcp_http_server.py
    # It stays running and prints:  Uvicorn running on http://127.0.0.1:8000
    # Leave it running; start the client in a SECOND terminal.

Verified against the official MCP Python SDK v1.x (FastMCP streamable-http):
    https://github.com/modelcontextprotocol/python-sdk
"""

from mcp.server.fastmcp import FastMCP

# host/port/path are FastMCP settings. The Streamable HTTP endpoint defaults to
# "/mcp", so the full URL a client uses is  http://127.0.0.1:8000/mcp
mcp = FastMCP("l46-http-server", host="127.0.0.1", port=8000)


# --- Tool 1: finished, same as L45 so you have a working reference ---
@mcp.tool()
def get_order_status(order_id: str) -> str:
    """Look up the delivery status of a customer order by its ID."""
    fake_orders = {
        "A100": "shipped — arriving tomorrow",
        "A200": "processing — leaves the warehouse today",
        "A300": "delivered on 2026-07-01",
    }
    return fake_orders.get(order_id, f"no order found with id {order_id}")


# --- Tool 2: <<< YOUR TASK >>> ---
# TODO: add a SECOND tool called "cancel_order" that takes an order_id (str)
#       and returns a str.
#   1. Copy the @mcp.tool() decorator line above.
#   2. Define:  def cancel_order(order_id: str) -> str:
#   3. Give it a one-line docstring (that's the description the LLM reads).
#   4. Return a message, e.g.  f"order {order_id} has been canceled"
#      (mock it — no real system needed, just like get_order_status).
#
# When done, the client's "Available tools" line should list BOTH
# get_order_status AND cancel_order.


if __name__ == "__main__":
    # transport="streamable-http": run as an HTTP server (not a stdio subprocess).
    mcp.run(transport="streamable-http")
