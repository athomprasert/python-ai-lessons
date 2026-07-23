# L47 example — an A2A agent + client (task lifecycle)

Where L45/L46 exposed **tools** over MCP, this exposes an **agent** over **A2A**.
A client discovers the agent from its Agent Card, delegates a task, and streams
the task lifecycle back: `submitted → working → (artifact) → completed`.

- `a2a_server.py` — the agent. Publishes an Agent Card at
  `/.well-known/agent-card.json` and runs an executor. **You finish the
  lifecycle** (`submit → start_work → add_artifact → complete`).
- `a2a_client.py` — discovers the agent by URL and delegates a task. Has **one
  deliberate bug**: the outgoing message needs `role=Role.ROLE_USER`.

## Run it — TWO terminals

The `a2a-sdk` is already in the project venv (installed for this lesson).
Use the venv Python — bare `python`/`pip` aren't on PATH on this Mac (see L45).

**Terminal 1 — start the agent (leave it running):**
```bash
source ~/ai/claude/projects/python/.venv/bin/activate
cd ~/ai/claude/projects/python/lessons/examples/l47
python a2a_server.py
```
It serves on `http://127.0.0.1:9100`. Peek at the Agent Card in a browser:
`http://127.0.0.1:9100/.well-known/agent-card.json`

**Terminal 2 — run the client:**
```bash
source ~/ai/claude/projects/python/.venv/bin/activate
cd ~/ai/claude/projects/python/lessons/examples/l47
python a2a_client.py
```

## Success looks like (after both fixes)

```
Delegating task to fx-agent...
  <- task
  <- status: TASK_STATE_SUBMITTED
  <- status: TASK_STATE_WORKING
  <- result: 100 USD to SGD -> 135.20 SGD (mock rate)
  <- status: TASK_STATE_COMPLETED
```

Stop the server with `Ctrl-C` in terminal 1 when done. Restart it after any
server edit — a running process holds the old code.

## Common errors (all are steps of the exercise)

- `NotImplementedError: Finish the lifecycle...` — you haven't filled in the five
  `updater.*` calls in the server's `execute()`.
- `InternalError: Message must be from a user` — the client bug: add
  `role=Role.ROLE_USER` to `new_text_message(...)`.
- Client hangs — the task never reached a terminal state; make sure
  `updater.complete()` is called.

## Verified against

`a2a-sdk` **1.1.2** on Python 3.14, end-to-end (card discovery + full lifecycle).
Heads-up: this SDK version's API differs substantially from older A2A tutorials
online (proto-based types, `supported_interfaces`, `Role` enum, mandatory
task-enqueue). This code is written for 1.1.2 specifically.
https://github.com/a2aproject/a2a-python
