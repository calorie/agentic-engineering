# Context policy

## Runtime state vs engineering state

Runtime-native orchestration owns transient execution state:

- Claude Code Dynamic Workflow plan, agent graph, intermediate variables, workflow checkpoints;
- Codex Ultra subagent execution and thread state.

Agentic Engineering should not duplicate that state into chat or repository files.

Durable engineering state owns only information that must survive runtime/session boundaries:

- project facts in `.agentic/PROJECT.md`;
- stable task requirements in `.agent/tasks/<task>/SPEC.md`;
- cross-session engineering progress in `STATE.md`;
- durable rationale in `DECISIONS.md`.

## Root context

Keep the root conversation/thread focused on:

- user requirements;
- constraints;
- confirmed decisions;
- integration status;
- verification evidence;
- blockers;
- final result.

Do not paste bulk searches, long test logs, or every subagent result into root context.

## Compaction

Treat runtime-native compaction and workflow checkpointing as normal operation.

Do not ask the user to manage `/clear` or `/compact`.

`COMPACT.md` and `RUNTIME.md` are fallback diagnostics/checkpoints only. They are not the primary state when the runtime already preserves its own workflow progress.
