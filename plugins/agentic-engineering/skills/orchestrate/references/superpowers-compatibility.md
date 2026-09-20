# Superpowers compatibility

Agentic Engineering and Superpowers can coexist, but they must not compete for execution-topology ownership.

## Ownership order

1. Explicit user requirements and repository constraints
2. Agentic Engineering safety, durable-state, verification, and Git/PR policy
3. Runtime-native orchestration
   - Claude Code ultracode / Dynamic Workflows
   - Codex Ultra proactive multi-agent delegation
4. Superpowers methodology
5. Agentic Engineering fallback specialists

Superpowers may shape **how an individual engineering activity is performed**, but it must not replace the native runtime as the scheduler when native proactive orchestration is available.

## Use directly

These Superpowers skills are methodology-oriented and normally compose well with Agentic Engineering:

- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `receiving-code-review`
- `diagnosing-superpowers`

Apply them inside whatever execution topology the native runtime chooses.

## Use conditionally and deduplicate

### brainstorming

Use when requirements, product behavior, architecture, or UX contain material ambiguity.

If the user already supplied clear requirements and acceptance criteria, do not manufacture extra approval checkpoints merely because the skill exists. Escalate only when a consequential choice cannot be inferred safely.

### writing-plans

Plans may describe:

- desired outcomes;
- acceptance criteria;
- dependency ordering;
- interfaces;
- verification steps;
- reviewable units.

Do not encode a mandatory agent count, worker graph, or fixed dispatch sequence that overrides native orchestration.

### requesting-code-review

Use only when the native workflow has not already produced equivalent independent review evidence.

Do not add a duplicate reviewer after an adequate native review.

### using-git-worktrees

Use its workspace-safety and environment-detection rules, but prefer an existing runtime-managed worktree or isolated checkout.

Do not create another worktree around work already isolated by Claude Code, Codex, or an external harness.

### finishing-a-development-branch

Use its verification and environment-detection discipline.

Agentic Engineering still owns the final review topology:

- one PR;
- independent PRs;
- Stacked PRs.

Do not force an additional merge/PR decision menu when the user's requested outcome and repository policy already determine the next action.

## Do not nest a second scheduler

The following Superpowers skills own execution topology and therefore must not become a second scheduler under Claude ultracode or Codex Ultra:

- `subagent-driven-development`
- `dispatching-parallel-agents`
- `executing-plans`

When native proactive orchestration is available:

- do not invoke these skills to allocate another fixed set of workers;
- do not create nested fan-out under an already active Dynamic Workflow / Ultra delegation graph;
- preserve any useful methodology from them, such as fresh context, task-level verification, and review gates, inside the native workflow instead.

Use these skills as direct execution engines only when:

- native proactive orchestration is unavailable; or
- the user explicitly requests that specific Superpowers execution workflow.

Even then, Agentic Engineering write-isolation and Git/review-topology constraints still apply.

## Verification deduplication

A verification or review step is satisfied when there is fresh, relevant evidence from either:

- runtime-native orchestration;
- a Superpowers methodology skill;
- an Agentic Engineering fallback specialist.

Do not repeat the same review simply because more than one installed framework offers it.

## TDD and throughput

TDD is compatible with parallel execution when ownership is isolated.

The runtime may execute independent RED-GREEN-REFACTOR loops in parallel worktrees/checkouts, but must serialize work that shares:

- the same checkout;
- unstable interfaces;
- ordered migrations;
- generated sources of truth;
- scarce mutable test infrastructure.

## Context policy

Superpowers plans, review notes, and debugging traces are transient unless they contain durable engineering information.

Persist only cross-session facts, decisions, blockers, and verification state in `.agent/tasks/`. Do not copy the full Superpowers workflow transcript into durable state.
