# Organization rollout

Agentic Engineering 0.5.0 distributes a small shared engineering policy while leaving execution to Claude Code and Codex.

## Cost-aware baseline

Do not standardize maximum effort as the organization default.

Claude Code:

- start ordinary work at the model default;
- use Dynamic Workflows for long-running, codebase-wide, strongly parallelizable, hard-to-verify, or high-risk work;
- treat ultracode as an optional session-level accelerator, not a repository requirement.

Codex:

- keep multi-agent capability available;
- do not pin project-level Ultra reasoning for every task;
- increase reasoning/delegation only when task complexity justifies the additional usage.

This policy is intended to maximize verified engineering throughput over time while reducing avoidable rate-limit pressure.

## Central policy

Keep only generic cross-runtime rules in the central Plugin:

- effort escalation guidance;
- parallel-write safety boundaries;
- durable engineering-state conventions;
- verification deduplication;
- dependency/version policy;
- GitHub review topology and Stacked PR policy;
- methodology-plugin coexistence.

Do not distribute custom schedulers, hook runtimes, worker pools, or context-management scripts when the native runtime already provides those capabilities.

## Project overlay

Keep project-specific configuration small:

- `AGENTS.md`;
- `CLAUDE.md` and `.claude/settings.json`;
- `.codex/config.toml`;
- `.agentic/PROJECT.md`;
- optional `.agent/tasks/` durable state.

## Methodology plugins

Superpowers may provide TDD, debugging, planning, and verification methodology, but should not become a nested scheduler underneath native orchestration.

Ponytail may bias implementation toward the simplest correct solution without overriding explicit requirements, safety, or repository invariants.

## Distribution

Distribute the central Plugin through the supported Claude Code and Codex Marketplace mechanisms for your environment.

Account, model, plan, and administrator limits always take precedence over repository policy.

## Stability

- Keep the Plugin slug stable.
- Keep portable, Claude, and Codex manifest versions synchronized.
- Prefer deleting compatibility code when runtimes gain equivalent native capabilities.
- Keep project-specific facts out of the central Plugin.
- Revisit effort policy when model capability, pricing, or rate limits materially change.
