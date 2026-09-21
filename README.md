# agentic-engineering

Agentic Engineering is a deliberately small policy plugin for Claude Code and Codex.

It does **not** implement its own scheduler, context engine, worker pool, or hook runtime. Native runtimes evolve faster and are better positioned to own those responsibilities.

Current version: **0.5.0**

## Goal

Maximize long-term verified engineering throughput, not model usage per task.

```text
user objective
    |
    v
runtime-native execution
    |
    +-- ordinary work -> default effort
    |
    +-- high-leverage work -> workflow / higher effort
    |
    v
Agentic Engineering constraints
    |
    +-- safe write isolation
    +-- durable engineering state
    +-- verification evidence
    +-- Git / PR topology
```

## Cost-aware execution

### Claude Code

Start at the model default.

Use Dynamic Workflows for work that is long-running, codebase-wide, strongly parallelizable, hard to verify manually, or expensive to get wrong.

`ultracode` is useful as a **session-level accelerator**, but it is intentionally not required by the repository. Dynamic Workflows use substantially more tokens than typical sessions, so always-on ultracode is not the default policy.

To opt into one ultracode session:

```bash
claude --effort ultracode
```

You can also ask Claude to use a Dynamic Workflow directly when that is the right execution shape.

### Codex

The project template keeps multi-agent capability enabled but does not pin `model_reasoning_effort = "ultra"`.

Use normal reasoning for ordinary work and escalate/delegate when complexity justifies the additional usage.

## Methodology plugins

Superpowers and Ponytail are complementary when responsibilities stay separate.

- **Superpowers**: methodology such as TDD, systematic debugging, and verification. Do not nest another scheduler under an active native scheduler.
- **Ponytail**: prefer the simplest correct implementation. Explicit requirements, safety, and project invariants take precedence.

## Shared engineering policy

- never use multiple concurrent writers in one checkout;
- parallel writes require isolated worktrees/checkouts and disjoint ownership;
- do not duplicate equivalent planning, review, verification, or worktree setup;
- keep transient runtime state in the runtime;
- persist only durable cross-session engineering information;
- choose one PR, independent PRs, or Stacked PRs from review dependencies, not agent count;
- never revert unrelated user changes.

## Durable state

Use `.agentic/PROJECT.md` for durable project facts.

For long-running work, use only what is needed:

```text
.agent/tasks/<task>/
├── SPEC.md
├── STATE.md
└── DECISIONS.md
```

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

No runtime hooks, custom agents, or plugin-side Python scripts are required.

## Validation

```bash
python3 scripts/validate.py
```

## Project template

Use https://github.com/calorie/agentic-repo-template for the thin repository overlay.
