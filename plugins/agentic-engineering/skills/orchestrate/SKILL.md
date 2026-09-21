---
name: orchestrate
description: Apply lightweight engineering policy to substantive software work. Keep execution topology runtime-native, use ordinary effort by default, escalate only high-leverage tasks, and coordinate cleanly with Superpowers and Ponytail.
version: 0.5.0
---

# Agentic Engineering

Optimize for verified engineering output per unit of human time, model usage, and maintenance cost.

## Effort policy

Start ordinary work at the runtime/model default.

Escalate only when the task is meaningfully:

- long-running;
- codebase-wide;
- strongly parallelizable;
- difficult to verify manually;
- expensive to get wrong.

### Claude Code

Do not require ultracode as a project default.

For ordinary work, use normal Claude Code effort. For high-leverage work, use a Dynamic Workflow when available; ultracode is an optional session-level convenience for automatically selecting workflows, not a repository requirement.

### Codex

Do not require Ultra reasoning as a project default.

Keep native multi-agent capability available and delegate when the task benefits from parallel investigation, isolated implementation, or independent verification. Use higher reasoning effort only when task complexity justifies the additional usage.

## Execution ownership

The runtime owns:

- decomposition;
- agent count;
- fan-out;
- transient workflow state;
- runtime-local review and verification scheduling.

Agentic Engineering owns only cross-runtime engineering constraints and final Git/review topology.

Never create a fixed worker graph before the native runtime has made its execution decision.

## Methodology plugins

When Superpowers is installed:

- use TDD, systematic debugging, and verification methodology when useful;
- do not nest `subagent-driven-development`, `dispatching-parallel-agents`, or `executing-plans` under an already active native scheduler;
- deduplicate equivalent planning, review, verification, and worktree setup.

When Ponytail is installed:

- prefer the simplest correct implementation;
- project requirements, safety, and repository invariants take precedence over minimization.

## Write isolation

- Never allow multiple writers to mutate the same checkout concurrently.
- Parallel writes require isolated worktrees/checkouts and genuinely disjoint ownership.
- Shared schemas, ordered migrations, unstable interfaces, generated sources of truth, and scarce mutable test infrastructure are synchronization boundaries.
- Never revert unrelated user changes.

## Project facts

Read `.agentic/PROJECT.md` before substantive changes when it exists.

If it is missing, pending, or clearly stale, discover only durable facts needed repeatedly:

- build / test / lint / typecheck commands;
- package manager and lockfile;
- generated-code source of truth;
- architecture, migration, and compatibility constraints.

Do not maintain file inventories or task-specific scratch state there.

## Durable state

For work that must survive sessions, runtimes, pull requests, or human handoff, use only:

```text
.agent/tasks/<task>/
├── SPEC.md
├── STATE.md
└── DECISIONS.md
```

Persist stable requirements, progress, verification status, blockers, and durable rationale. Do not persist native runtime agent graphs, workflow queues, compaction state, or full transcripts.

## Verification

Completion requires relevant fresh evidence.

Do not repeat an equivalent review or verification pass merely because the runtime, Superpowers, or another installed tool can all provide one.

## Review topology

- one focused reviewable change -> one PR;
- independent reviewable changes -> independent PRs;
- dependent but independently reviewable changes -> Stacked PRs.

Execution topology does not determine PR topology.

## User experience

The user should normally provide the engineering objective, not orchestration instructions.

Do not ask the user to manage agent count, parallelism, context cleanup, worktree allocation, reviewer creation, or PR topology unless a real product or authorization decision requires input.
