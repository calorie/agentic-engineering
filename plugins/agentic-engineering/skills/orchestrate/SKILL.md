---
name: orchestrate
description: Automatically optimize substantive software work using runtime-native capabilities. Proactively protect context, delegate and parallelize beneficial work, persist durable state for long-running tasks, deduplicate verification, and choose review topology without making the user manage orchestration.
version: 0.5.3
---

# Agentic Engineering

Optimize for verified engineering output per unit of human time, model usage, and maintenance cost.

The user should normally provide only the engineering objective. Automatically choose the execution shape needed to complete it efficiently.

## Automatic optimization loop

Immediately after receiving a substantive objective, before broad implementation begins:

1. derive the review dependency graph for the full objective;
2. partition the objective into the smallest useful independently reviewable and independently verifiable units;
3. choose one PR, independent PRs, or a Stacked PR topology from that graph;
4. initialize the chosen review topology before implementing dependent upper layers;
5. then decide the minimum useful reasoning/effort level;
6. decide what should remain in the primary context;
7. decide what should be delegated to fresh subagents;
8. decide what independent work should run in parallel;
9. decide whether isolated worktrees/checkouts are required;
10. decide whether durable task state is required;
11. decide what verification evidence is sufficient.

Do not ask the user to make these orchestration decisions unless a real product, authorization, or irreversible-action decision requires input.

## Review dependency graph

Plan review topology from the **full user objective**, not only from the currently active implementation step.

For each candidate review unit, identify:

- what durable contract or behavior it establishes;
- which later units depend on it;
- whether it can be reviewed meaningfully on its own;
- whether it has a meaningful verification story on its own.

Choose topology before broad implementation:

- one focused reviewable unit -> one PR;
- multiple independent reviewable units -> independent PRs;
- multiple dependent, independently reviewable and independently verifiable units -> Stacked PRs.

When the objective already exposes dependent milestones or phases, treat that as strong evidence for a stack unless the milestones cannot produce meaningful intermediate review states.

If Stacked PR conditions are met, invoke the `stacked-pr` skill and initialize the stack **before implementing dependent upper layers**.

Do not serialize dependent work through the default branch merely because implementation proceeds one milestone at a time. Once a lower layer's contract is stable and locally verified, continue the dependent upper layer on top of it without waiting for the lower PR to merge.

Do not split work into stacks merely to create more PRs. Review units must reduce review risk, unblock later work, or shorten the merge-wait critical path.

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

## Autonomy and approval boundaries

Proceed without user approval for routine, reversible engineering work that is within the stated objective and repository constraints.

This includes, when appropriate:

- reading and editing repository files;
- running formatters, linters, tests, builds, and code generation;
- installing or updating dependencies consistent with the existing stack and dependency policy;
- creating branches and worktrees;
- `git add`, commits, rebases, and other normal feature-branch maintenance;
- pushing non-default branches;
- creating and updating pull requests;
- running review and verification workflows.

Ask the user before making an **important design decision** that materially changes long-lived system direction and cannot be inferred safely. Examples include:

- a major architecture or subsystem boundary;
- a public API or persistent data-contract change with broad compatibility impact;
- an irreversible or high-risk migration strategy;
- a security or trust-boundary change;
- adopting a foundational technology or dependency that materially changes the system architecture.

Do not ask for routine implementation choices, local refactors, naming, test structure, or other reversible decisions.

Treat integration into the default branch as a hard approval boundary:

- do not merge a pull request without explicit user approval immediately before the merge;
- do not locally merge into, or directly push to, the repository default branch without explicit user approval immediately before the action;
- creating/updating a PR, pushing its feature branch, and preparing it for merge do not require approval.

If repository or organization policy imposes a stricter boundary, obey the stricter policy.

## Verification

Automatically identify and run the narrowest useful checks, then expand verification according to blast radius and risk.

Substantive changes should receive independent review or verification when it materially reduces risk.

Do not repeat an equivalent review or verification pass merely because the runtime, Superpowers, or another installed tool can all provide one.

Do not declare completion while relevant verification is failing unless the failure is explicitly reported as a blocker.

## Review topology during execution

Preserve the review topology selected at objective intake unless new information materially changes the dependency graph.

Execution topology does not determine PR topology.

For a stack:

- keep dependency order explicit;
- stabilize and verify a lower layer before building dependent behavior on top of it;
- do not wait for lower-layer merge when the upper layer can safely proceed against the stable lower-layer contract;
- fix lower-layer defects in the lower layer and propagate/rebase upward;
- keep each layer independently reviewable and meaningfully verifiable;
- do not collapse later dependent milestones back into sequential `main`-based PRs simply because earlier layers have already been submitted.

Re-plan the topology only when scope or dependencies materially change.

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
