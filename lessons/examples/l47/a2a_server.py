"""
L47 demo — an A2A AGENT server (YOUR turn: drive the task lifecycle).

Where L45/L46 exposed TOOLS over MCP, this exposes an AGENT over A2A. Another
agent (or our client) discovers this one via its Agent Card, then delegates a
TASK to it. The agent moves that task through its lifecycle:
    submitted -> working -> (produces an artifact) -> completed
and streams each state change back to the caller.

HOW TO RUN (terminal 1 — leave it running)
    source ~/ai/claude/projects/python/.venv/bin/activate
    python a2a_server.py
    # Serves on http://127.0.0.1:9100 ; Agent Card at
    #   http://127.0.0.1:9100/.well-known/agent-card.json

Verified end-to-end against a2a-sdk 1.1.2 on Python 3.14.
NOTE: this SDK's API differs a lot from older A2A tutorials online — the code
here is written for 1.1.2 specifically (proto types, supported_interfaces, etc).
"""

import uvicorn
from fastapi import FastAPI

# --- Types that describe the agent (its "business card") ---
from a2a.types import AgentCard, AgentSkill, AgentCapabilities, AgentInterface
# --- Server plumbing: executor base, task lifecycle helper, in-memory store ---
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater, InMemoryTaskStore
from a2a.server.request_handlers import DefaultRequestHandler
# --- Route builders: publish the card + the JSON-RPC message endpoint ---
from a2a.server.routes.agent_card_routes import create_agent_card_routes
from a2a.server.routes.jsonrpc_routes import create_jsonrpc_routes
from a2a.server.routes.fastapi_routes import add_a2a_routes_to_fastapi
# --- Small helpers to build proto messages/parts without hand-writing them ---
from a2a.helpers import new_task_from_user_message, new_text_part


# ── 1. The AGENT CARD ─────────────────────────────────────────────────────────
# This is the /.well-known/agent-card.json a client fetches to DISCOVER the agent:
# what it's called, what it can do (skills), and how to reach it (interfaces).
SKILL = AgentSkill(
    id="fx",
    name="Currency convert",
    description="Convert an amount from one currency to another.",
    tags=["finance"],
)
CARD = AgentCard(
    name="fx-agent",
    description="Converts currency amounts between currencies.",
    version="1.0.0",
    # supported_interfaces replaces the single `url` field from older A2A versions.
    # protocol_binding="JSONRPC" says "talk to me with JSON-RPC over HTTP".
    supported_interfaces=[
        AgentInterface(url="http://127.0.0.1:9100/", protocol_binding="JSONRPC")
    ],
    capabilities=AgentCapabilities(streaming=True),  # we stream lifecycle updates
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    skills=[SKILL],
)


# ── 2. The EXECUTOR — what the agent actually DOES with a delegated task ───────
class FxExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        # The caller's text, e.g. "100 USD to SGD".
        user_text = context.get_user_input()

        # A2A rule: the Task object must be enqueued BEFORE any status update.
        # (If a task already exists we reuse it; otherwise create one.)
        task = context.current_task
        if task is None:
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        # TaskUpdater is the helper that publishes lifecycle events for this task.
        updater = TaskUpdater(event_queue, task.id, task.context_id)

        # <<< YOUR TASK >>> drive the lifecycle. Uncomment + complete these calls:
        #
        #   await updater.submit()       # -> TASK_STATE_SUBMITTED
        #   await updater.start_work()   # -> TASK_STATE_WORKING
        #
        #   result = f"{user_text} -> 135.20 SGD (mock rate)"
        #   # add_artifact publishes the actual RESULT of the task
        #   await updater.add_artifact([new_text_part(result)], name="conversion")
        #
        #   await updater.complete()     # -> TASK_STATE_COMPLETED
        #
        # Until you fill these in, the client will hang waiting for the task to
        # reach a terminal state. Do all five lines.
        raise NotImplementedError("Finish the lifecycle in FxExecutor.execute")

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        # Cancellation isn't part of this demo; A2A still requires the method.
        raise NotImplementedError


# ── 3. Wire executor + task store + card into a request handler, then serve ───
handler = DefaultRequestHandler(
    agent_executor=FxExecutor(),
    task_store=InMemoryTaskStore(),   # remembers tasks in RAM (fine for a demo)
    agent_card=CARD,
)

app = FastAPI()
add_a2a_routes_to_fastapi(
    app,
    agent_card_routes=create_agent_card_routes(CARD),      # publishes the card
    jsonrpc_routes=create_jsonrpc_routes(handler, rpc_url="/"),  # the message endpoint
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9100, log_level="warning")
