# agentic-engineering

Agentic Engineering is a runtime-neutral Agent Plugin / Marketplace that uses **Claude Code ultracode** and **Codex Ultra** native proactive multi-agent orchestration while standardizing project constraints, durable engineering state, verification, and Git/PR topology.

- Marketplace: https://github.com/calorie/agentic-engineering
- Project Template: https://github.com/calorie/agentic-repo-template
- Current version: **0.4.2**

## Architecture

Agentic Engineering does not act as the execution engine.

```text
Engineering objective
       |
       v
agentic-engineering
  project facts / constraints
  durable engineering state
  verification requirements
  Git / PR topology
       |
       +---------------+
       v               v
Claude Code          Codex
ultracode            Ultra
Dynamic Workflows    proactive multi-agent
       |               |
       +---- native execution topology ----+
```

The runtime owns **execution topology**:

- agent count;
- task decomposition;
- fan-out;
- staged execution;
- runtime verification passes;
- transient workflow state.

Agentic Engineering owns **engineering policy**:

- project-specific constraints;
- safe parallel-write boundaries;
- durable cross-session state;
- dependency/version policy;
- required verification evidence;
- single PR / independent PR / Stacked PR topology.

## Claude Code

This project assumes **ultracode**.

The project template requests ultracode in `.claude/settings.json`, and setup/doctor checks verify that the current CLI accepts `--effort ultracode`.

With ultracode, Claude decides whether a substantive task should use a Dynamic Workflow. The Plugin does not pre-allocate investigator, planner, worker, reviewer, or verifier agents before the native workflow makes that decision.

Bundled custom agents are fallback specialists.

Install directly:

```bash
claude plugin marketplace add calorie/agentic-engineering
claude plugin install agentic-engineering@agentic-engineering
```

Start an explicit ultracode session when needed:

```bash
claude --effort ultracode
```

## Codex

The project template requests:

```toml
model_reasoning_effort = "ultra"

[agents]
enabled = true
```

Codex Ultra is expected to own execution topology through proactive delegation rather than copying Claude's Dynamic Workflow graph.

Install directly:

```bash
codex plugin marketplace add calorie/agentic-engineering \
  --sparse .agents/plugins \
  --sparse plugins/agentic-engineering

codex plugin add agentic-engineering@agentic-engineering
```

The Codex IDE extension does not currently support Plugins. On that surface, `AGENTS.md` remains the fallback policy. Use Codex CLI or another Plugin-capable Codex surface for the full Plugin / Hooks / Skills behavior.

## Use the project template

For a new repository:

```bash
./scripts/setup-agentic.sh
```

Then start the runtime you want:

```bash
claude
# or
codex
```

The user should normally provide only the engineering objective:

```text
Add user search by name and email address.
```

The user should not need to manage agent count, parallelism, worktree allocation, context cleanup, reviewer creation, or PR topology.

## Superpowers compatibility

Superpowers is treated as a **methodology provider**, not as a second scheduler.

Use methodology-oriented skills inside the runtime-native execution topology when useful:

- `test-driven-development`;
- `systematic-debugging`;
- `verification-before-completion`;
- `receiving-code-review`.

Use `brainstorming`, `writing-plans`, `requesting-code-review`, `using-git-worktrees`, and `finishing-a-development-branch` conditionally and deduplicate work already performed by the native runtime.

Under Claude ultracode / Dynamic Workflows or Codex Ultra, do not let these Superpowers skills take over execution topology:

- `subagent-driven-development`;
- `dispatching-parallel-agents`;
- `executing-plans`.

Their useful principles—fresh context, isolated work, verification, and review gates—should be expressed through the native runtime instead of nesting another scheduler.

An explicit user request for a specific Superpowers execution workflow still takes precedence, subject to write-isolation and Git/review-topology constraints.

See `plugins/agentic-engineering/skills/orchestrate/references/superpowers-compatibility.md`.

## Parallel-write guardrails

Native runtimes own most execution decisions, but the following constraints remain shared:

- never place multiple writers in the same checkout at the same time;
- allow parallel writes only with isolated worktrees/checkouts and disjoint ownership;
- treat shared DB schemas, ordered migrations, and unstable shared interfaces as synchronization boundaries;
- preserve dependency order for dependent Stacked PR layers;
- never revert unrelated user changes.

## Durable state

Separate runtime-native workflow state from durable engineering state.

Leave these to the runtime:

- Claude Dynamic Workflow agent graphs and checkpoints;
- Codex Ultra subagent execution and thread state;
- transient logs and scratch queues.

Persist these in the repository only when needed:

```text
.agentic/PROJECT.md
.agent/tasks/<task>/
├── SPEC.md
├── STATE.md
└── DECISIONS.md
```

`COMPACT.md` and `RUNTIME.md` are fallback diagnostics rather than primary state. Do not duplicate transient state the runtime already preserves.

## Review topology

Execution topology and PR topology are separate concerns.

- one focused reviewable change -> one PR;
- independent reviewable changes -> independent PRs;
- dependent but separately reviewable changes -> GitHub Stacked PRs.

Do not split PRs merely because multiple agents were used.

## Dependency policy

- use the latest stable dependency version compatible with project constraints;
- update lockfiles when supported;
- pin GitHub Actions to the full commit SHA of the latest stable release;
- use Dependabot for continuing updates;
- use pre-release versions only for an explicit reason.

## Plugin structure

```text
agentic-engineering/
├── .claude-plugin/marketplace.json
├── .agents/plugins/marketplace.json
└── plugins/agentic-engineering/
    ├── plugin.json
    ├── .claude-plugin/plugin.json
    ├── .codex-plugin/plugin.json
    ├── skills/
    ├── agents/                  # Claude fallback specialists
    ├── hooks/
    └── scripts/
```

## Validation

```bash
python3 scripts/validate.py
python3 -m py_compile plugins/agentic-engineering/scripts/*.py
```

## Versioning

Keep the Claude Marketplace version, Claude manifest version, portable manifest version, and Codex manifest version synchronized.

## Security

Plugin hooks can execute local commands. Install Plugins only from a Marketplace you trust. Codex requires trust review for unmanaged hooks on first use.
