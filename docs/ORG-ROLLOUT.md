# Organization rollout

Agentic Engineering 0.4.x distributes a **native proactive orchestration + shared engineering policy** model across Claude Code and Codex environments.

## Execution baseline

Claude Code:

- use ultracode / Dynamic Workflows as the primary execution engine;
- account, model, or administrator restrictions on workflows or xhigh reasoning take precedence.

Codex:

- request `model_reasoning_effort = "ultra"` in project configuration;
- on supported accounts/models, use proactive task delegation as the primary execution engine.

Do not hardcode agent count or a fixed worker graph as an organization-wide policy.

## Central policy

Keep these in the central Plugin:

- project discovery policy;
- parallel-write safety boundaries;
- durable engineering-state protocol;
- verification requirements;
- dependency/version policy;
- GitHub review topology and Stacked PR policy;
- runtime adapters and safe fallbacks.

Keep these in each project:

- `AGENTS.md`;
- `CLAUDE.md` and `.claude/settings.json`;
- `.codex/config.toml`;
- `.agentic/PROJECT.md`;
- project-specific architecture, test, migration, and compatibility facts.

## Distribution

For Claude Code organization management, connect the Marketplace and distribute the Plugin as Required or Installed by default as appropriate.

For Codex / ChatGPT workspaces, distribute through the supported Plugin Marketplace or directory policy. The Codex IDE extension does not currently support Plugins, so `AGENTS.md` remains the fallback policy there.

## Stability

- Keep the Plugin slug stable.
- Keep portable, Claude, and Codex manifest versions synchronized.
- Require PR + CI + CHANGELOG + version bump for policy changes.
- Do not copy generic policy into each project.
- As runtime-native capabilities improve, make adapters thinner instead of adding custom orchestration.
- Do not hardcode project-specific facts in the central Plugin.
