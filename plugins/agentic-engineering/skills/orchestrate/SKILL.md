---
name: orchestrate
description: Automatically optimize substantive software work using runtime-native capabilities. Proactively protect context, delegate and parallelize beneficial work, persist durable state for long-running tasks, deduplicate verification, and choose review topology without making the user manage orchestration.
version: 0.5.1
---

# Agentic Engineering

Optimize for verified engineering output per unit of human time, model usage, and maintenance cost.

The user should normally provide only the engineering objective. Automatically choose the execution shape needed to complete it efficiently.

## Automatic optimization loop

For every substantive task, automatically decide:

1. the minimum useful reasoning/effort level;
2. what should remain in the primary context;
3. what should be delegated to fresh subagents;
4. what independent work should run in parallel;
5. whether isolated worktrees/checkouts are required;
6. whether durable task state is required;
7. what verification evidence is sufficient;
8. whether the result should be one PR, independent PRs, or a Stacked PR.

Do not ask the user to make these orchestration decisions unless a real product, authorization, or irreversible-action decision requires input.

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

For ordinary work, use normal Claude Code effort. For high-leverage work, proactively use native Dynamic Workflows when available and beneficial. Ultracode remains an optional session-level accelerator, not a repository requirement.

### Codex

Do not require Ultra reasoning as a project default.

Keep native multi-agent capability available. Proactively delegate when fresh context, parallel investigation, isolated implementation, or independent verification will materially improve throughput or result quality. Use higher reasoning effort only when complexity justifies the additional usage.

## Context optimization

Protect the primary context proactively.

Delegate noisy or self-contained work to fresh subagents when the primary thread needs the conclusion rather than the full process. Typical candidates include:

- repository exploration;
- broad search;
- log and failure analysis;
- test-output analysis;
- independent review;
- isolated implementation units.

Return compact findings and decisions to the primary context instead of raw intermediate output.

Rely on runtime-native compaction and workflow state. Never require the user to manage context cleanup, `/clear`, or `/compact`.

## Parallelism

Automatically parallelize independent work when doing so materially improves wall-clock time, context quality, or independent verification.

Choose the number of agents automatically.

- Never allow multiple writers to mutate the same checkout concurrently.
- Parallel writes require isolated worktrees/checkouts and genuinely disjoint ownership.
- Shared schemas, ordered migrations, unstable interfaces, generated sources of truth, and scarce mutable test infrastructure are synchronization boundaries.
- Serialize dependent work when parallel execution would create coordination overhead or unsafe intermediate states.
- Never revert unrelated user changes.

Do not ask the user whether or how to parallelize.

## Methodology plugins

When Superpowers is installed:

- use TDD, systematic debugging, and verification methodology when useful;
- do not nest `subagent-driven-development`, `dispatching-parallel-agents`, or `executing-plans` under an already active native scheduler;
- deduplicate equivalent planning, review, verification, and worktree setup.

When Ponytail is installed:

- prefer the simplest correct implementation;
- project requirements, safety, and repository invariants take precedence over minimization.

## Project facts

Read `.agentic/PROJECT.md` before substantive changes when it exists.

If it is missing or clearly stale, automatically discover only durable facts needed repeatedly:

- build / test / lint / typecheck commands;
- package manager and lockfile;
- generated-code source of truth;
- architecture, migration, and compatibility constraints.

Update the file when newly discovered durable facts would materially help future tasks. Do not maintain file inventories or task-specific scratch state there.

## Long-running work

When a task is likely to cross sessions, runtimes, pull requests, or human handoffs, automatically create and maintain:

```text
.agent/tasks/<task>/
├── SPEC.md
├── STATE.md
└── DECISIONS.md
```

Use:

- `SPEC.md` for stable goal, acceptance criteria, and constraints;
- `STATE.md` for meaningful progress, verification status, blockers, and the next action;
- `DECISIONS.md` for durable rationale that should not be rediscovered.

Update durable state at meaningful milestones, not after every tool call.

Do not ask the user to initialize or maintain task state. Do not persist native runtime agent graphs, workflow queues, compaction state, or full transcripts.

## Verification

Automatically identify and run the narrowest useful checks, then expand verification according to blast radius and risk.

Substantive changes should receive independent review or verification when it materially reduces risk.

Do not repeat an equivalent review or verification pass merely because the runtime, Superpowers, or another installed tool can all provide one.

Do not declare completion while relevant verification is failing unless the failure is explicitly reported as a blocker.

## Review topology

Choose review topology automatically from dependency structure and reviewability:

- one focused reviewable change -> one PR;
- independent reviewable changes -> independent PRs;
- dependent but independently reviewable changes -> Stacked PRs.

Execution topology does not determine PR topology.

Use Stacked PRs when they improve reviewability without introducing unnecessary coordination cost.

## User experience

The normal interaction is:

```text
user objective
    ↓
automatic effort/context/parallelism/state/verification/PR optimization
    ↓
verified engineering result
```

Do not make the user manage agent count, parallelism, context cleanup, worktree allocation, durable-state initialization, reviewer creation, or PR topology.
