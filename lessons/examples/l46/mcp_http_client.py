"""
L46 demo — an MCP CLIENT over STREAMABLE HTTP (YOUR turn: fix the connection).

This connects to the HTTP server by URL — it does NOT launch it. So you must
start mcp_http_server.py FIRST, in another terminal (see that file's header).

The one real difference from the L45 stdio client:
    stdio_client(...)        yields TWO values:  (read, write)
    streamablehttp_client(url) yields THREE:     (read, write, get_session_id)
HTTP connections carry a session id, so the transport hands you a helper to
read it. You don't need the id here, but you must still unpack all three values
or Python raises a "too many / not enough values to unpack" error.

HOW TO RUN (terminal 2, while the server runs in terminal 1)
    source ~/ai/claude/projects/python/.venv/bin/activate
    python mcp_http_client.py

Verified against the official MCP Python SDK v1.x streamable-http client:
    https://github.com/modelcontextprotocol/python-sdk
"""

import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# The server's Streamable HTTP endpoint. Base host:port + the default "/mcp" path.
SERVER_URL = "http://127.0.0.1:8000/mcp"


async def main():
    # STEP 1 — connect over HTTP.  <<< YOUR TASK (part A) >>>
    # The line below is WRONG on purpose: streamablehttp_client yields THREE
    # values, but this unpacks only two. Fix it by adding a third name for the
    # session-id helper. Convention: name an unused value "_" or "_get_session_id".
    #
    # TODO: change  as (read, write):  ->  as (read, write, _get_session_id):
    async with streamablehttp_client(SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:

            # STEP 2 — initialize + discover (same as L45).
            await session.initialize()
            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools.tools])

            # STEP 3 — call the finished tool (this part is done for you).
            result = await session.call_tool("get_order_status", arguments={"order_id": "A100"})
            print("Order A100 status:", result.content[0].text)

            # STEP 4 — call YOUR new tool.  <<< YOUR TASK (part B) >>>
            # Once you've added cancel_order to the server, uncomment and complete:
            #
            # cancelled = await session.call_tool("cancel_order", arguments={"order_id": "A200"})
            # print("Cancel A200:", cancelled.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
