# agentic-engineering

Agentic Engineering is a deliberately small policy plugin for Claude Code and Codex.

It does **not** implement its own scheduler, context engine, worker pool, or hook runtime. Instead, it tells native runtimes to automatically optimize execution around a user-provided engineering objective.

Current version: **0.5.3**

## Goal

Maximize long-term verified engineering throughput while minimizing human orchestration, model usage, and maintenance cost.

```text
user objective
    |
    v
automatic optimization
    |
    +-- effort
    +-- context isolation
    +-- delegation / parallelism
    +-- durable task state
    +-- verification
    +-- PR topology
    |
    v
runtime-native execution
    |
    v
verified engineering result
```

The user should not need to decide agent count, context cleanup, worktree allocation, long-task state, reviewer creation, or PR topology.

## Cost-aware execution

### Claude Code

Start at the model default.

For high-leverage work, proactively use native Dynamic Workflows when available and beneficial.

`ultracode` is an optional session-level accelerator, not a repository requirement.

```bash
claude --effort ultracode
```

Always-on maximum effort is intentionally avoided so ordinary work does not consume disproportionate usage.

### Codex

Keep multi-agent capability enabled without pinning `model_reasoning_effort = "ultra"`.

Use the runtime/model default for ordinary work. Proactively delegate or increase reasoning when the task benefits enough to justify the additional usage.

## Automatic context optimization

Keep the primary context focused on requirements, decisions, integration state, blockers, and final evidence.

Automatically push noisy or self-contained investigation, search, logs, test analysis, review, and isolated implementation into fresh subagent contexts when only the conclusion is needed.

Use runtime-native compaction. Do not make the user manage context cleanup.

## Automatic parallelism

Automatically parallelize independent work when it materially improves elapsed time, context quality, or independent verification.

Choose agent count automatically.

Parallel writes require isolated worktrees/checkouts and disjoint ownership. Never use concurrent writers in the same checkout.

## Automatic long-task state

When work is likely to cross sessions, runtimes, pull requests, or human handoff, automatically maintain:

```text
.agent/tasks/<task>/
├── SPEC.md
├── STATE.md
└── DECISIONS.md
```

Use `.agentic/PROJECT.md` for durable repository facts.

Transient runtime state remains in the runtime.

## Methodology plugins

- **Superpowers** provides methodology such as TDD, systematic debugging, and verification. Do not nest another scheduler under an active native scheduler.
- **Ponytail** biases implementation toward the simplest correct solution. Explicit requirements, safety, and project invariants take precedence.

Deduplicate equivalent planning, review, verification, and worktree setup.

## Approval boundaries

Routine development should proceed autonomously without repeated confirmation.

Normal edits, tests, `git add`, commits, feature-branch pushes, PR creation/updates, and verification are not approval boundaries.

Ask the user only for:

- important long-lived design decisions that cannot be inferred safely;
- the final action that integrates changes into the default branch, such as merging a PR or directly merging/pushing to the default branch.

The project template configures Codex so normal repository and Git metadata writes can proceed without sandbox approval prompts while merge commands remain an explicit approval boundary.

## Automatic review topology

Immediately after receiving a substantive objective, derive the review dependency graph for the **full objective** before broad implementation.

Choose automatically:

- one focused reviewable unit -> one PR;
- independent reviewable units -> independent PRs;
- dependent, independently reviewable and independently verifiable units -> GitHub Stacked PRs.

When stack conditions are met, initialize the stack before implementing dependent upper layers. Once a lower layer's contract is stable and locally verified, continue the upper layer on top of it without waiting for the lower PR to merge.

Do not fall back to sequential PRs all based on `main` merely because implementation is milestone-by-milestone. Use Stacked PRs when they reduce review risk or remove merge-wait time from the critical path.

## Install

### Claude Code

```bash
claude plugin marketplace add calorie/agentic-engineering
claude plugin install agentic-engineering@agentic-engineering
```

### Codex

```bash
codex plugin marketplace add calorie/agentic-engineering \
  --sparse .agents/plugins \
  --sparse plugins/agentic-engineering

codex plugin add agentic-engineering@agentic-engineering
```

## Plugin contents

```text
plugins/agentic-engineering/
├── plugin.json
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
└── skills/
    ├── orchestrate/SKILL.md
    └── stacked-pr/SKILL.md
```

No runtime hooks, custom agents, or plugin-side orchestration scripts are required.

## Validation

```bash
python3 scripts/validate.py
```

## Project template

Use https://github.com/calorie/agentic-repo-template for the thin repository overlay.
