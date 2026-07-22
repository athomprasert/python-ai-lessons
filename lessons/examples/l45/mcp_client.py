"""
L45 demo — a tiny MCP CLIENT in Python (YOUR turn to finish it).

This is the "host/client" side of MCP. It launches the server (mcp_server.py),
performs the initialize handshake, discovers the tools, and calls one.

This mirrors EXACTLY the three lifecycle steps you saw over the wire in L44:
    initialize  ->  list tools  ->  call tool

HOW TO RUN
    # The project .venv already has the SDK; on this Mac use python3 / the venv,
    # not a bare `python` / `pip` (those aren't on PATH). Simplest:
    ~/ai/claude/projects/python/.venv/bin/python mcp_client.py
    # Fresh machine without the venv? Install once:  pip3 install "mcp[cli]>=1.27,<2"

You will complete ONE step (marked TODO). When it works you should see:
    Available tools: ['get_order_status']
    Order A100 status: shipped — arriving tomorrow

Verified against the official MCP Python SDK v1.x stdio client example:
    https://github.com/modelcontextprotocol/python-sdk
"""

import asyncio  # MCP's Python API is async; asyncio runs the async function below
import sys      # sys.executable = the exact python running THIS file

# ClientSession drives the protocol; StdioServerParameters says how to launch the server.
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Tell the client how to start our server. We use sys.executable (not the bare
# string "python") so it launches with the SAME interpreter running this client —
# works whether your command is `python` or `python3`, venv or not.
server_params = StdioServerParameters(
    command=sys.executable,
    args=["mcp_server.py"],
)


async def main():
    # stdio_client(...) launches the server subprocess and gives us two pipes:
    # 'read' (messages FROM the server) and 'write' (messages TO the server).
    # 'async with' guarantees the subprocess is cleaned up when we're done —
    # like a try-with-resources block in Java.
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # STEP 1 — initialize: negotiate protocol version + capabilities.
            await session.initialize()

            # STEP 2 — discover: ask the server what tools it exposes.
            tools = await session.list_tools()
            # tools.tools is a list of tool objects; each has a .name
            print("Available tools:", [t.name for t in tools.tools])

            # STEP 3 — call a tool.  <<< YOUR TASK >>>
            # TODO: call the "get_order_status" tool with order_id "A100".
            #   - Use: result = await session.call_tool(<tool name>, arguments=<dict>)
            #     where <dict> maps the argument name to its value, e.g. {"order_id": "A100"}.
            #   - The text you want is at: result.content[0].text
            #   - Print it as:  print("Order A100 status:", <that text>)
            #
            # Delete the two lines below once you've written the real call.
            print("Order A100 status: <not implemented yet — finish STEP 3>")
            return


if __name__ == "__main__":
    asyncio.run(main())
