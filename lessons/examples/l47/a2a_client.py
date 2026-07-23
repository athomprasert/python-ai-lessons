"""
L47 demo — an A2A CLIENT (YOUR turn: fix the message role, watch the lifecycle).

This does the two things a calling agent does in A2A:
  1. DISCOVER the target agent from its URL (fetches the Agent Card for you).
  2. DELEGATE a task by sending it a message, then stream the lifecycle back.

Start a2a_server.py FIRST in another terminal, then run this.

HOW TO RUN (terminal 2)
    source ~/ai/claude/projects/python/.venv/bin/activate
    python a2a_client.py

Verified end-to-end against a2a-sdk 1.1.2 on Python 3.14.
"""

import asyncio
import httpx

from a2a.client import ClientFactory, ClientConfig
from a2a.helpers import new_text_message, get_stream_response_text
from a2a.types import SendMessageRequest, Role, TaskState

# The agent's base URL. create_from_url() will fetch its Agent Card from
# <BASE>/.well-known/agent-card.json to learn how to talk to it.
BASE = "http://127.0.0.1:9100"


async def main():
    async with httpx.AsyncClient() as http:
        # A ClientFactory builds a protocol-correct client from the discovered card.
        factory = ClientFactory(ClientConfig(httpx_client=http, streaming=True))
        client = await factory.create_from_url(BASE)   # <-- discovery happens here

        # Build the message we want to delegate.
        #
        # <<< YOUR TASK (the bug) >>>
        # new_text_message defaults role to AGENT. But WE are the user delegating
        # a task — the server rejects a task whose first message isn't from a user
        # ("InternalError: Message must be from a user"). Add the user role:
        #
        # TODO: change to  new_text_message("100 USD to SGD", role=Role.ROLE_USER)
        msg = new_text_message("100 USD to SGD")

        req = SendMessageRequest(message=msg)

        print("Delegating task to fx-agent...")
        # send_message STREAMS back a series of StreamResponse events. Each one is
        # a different stage: the task itself, status changes, then the result.
        async for resp in client.send_message(req):
            kind = resp.WhichOneof("payload")   # task | status_update | artifact_update
            if kind == "status_update":
                state = TaskState.Name(resp.status_update.status.state)
                print(f"  <- status: {state}")
            elif kind == "artifact_update":
                print(f"  <- result: {get_stream_response_text(resp)}")
            else:
                print(f"  <- {kind}")

        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
