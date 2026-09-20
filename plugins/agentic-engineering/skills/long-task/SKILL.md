---
name: long-task
description: Use this skill when engineering state must survive across sessions, runtimes, humans, or several pull requests. Keep durable product/engineering state while leaving transient agent graphs, workflow queues, and runtime checkpoints to Claude Code or Codex native orchestration.
version: 0.4.0
---

# Durable engineering state

Do not use chat history as the only source of truth, but also do not mirror native runtime internals into repository state.

Create `.agent/tasks/<task>/` only when work genuinely crosses sessions, runtimes, PRs, or human handoffs.

## SPEC.md

Stable contract:

- goal;
- acceptance criteria;
- constraints;
- non-goals;
- important external/interface contracts.

SPEC should change rarely.

## STATE.md

Cross-session engineering progress:

- current branch / PR / stack layer when relevant;
- completed reviewable units;
- important changed areas;
- verification status;
- blockers;
- next concrete engineering action.

Do not record every subagent, tool call, workflow stage, or temporary hypothesis.

## DECISIONS.md

Only durable decisions whose rationale would otherwise be re-litigated later.

## COMPACT.md / RUNTIME.md

Hooks may generate these as local fallback diagnostics.

- `COMPACT.md`: last available compaction summary.
- `RUNTIME.md`: branch / HEAD / working-tree snapshot.

They are not the source of truth when Claude Dynamic Workflows or Codex session state already preserve transient progress.

## ACTIVE_TASK

Use `.agent/ACTIVE_TASK` only for a task that genuinely requires durable cross-session state.

Remove it when the engineering task is complete.

## Checkpoints

Update durable state at meaningful boundaries only:

- acceptance criteria or architecture decision changed;
- reviewable unit completed;
- blocker changed;
- PR/stack layer completed;
- session/runtime handoff requires persistence.

Native workflow progress should stay native.
