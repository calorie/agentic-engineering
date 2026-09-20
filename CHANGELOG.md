# Changelog

## 0.4.1

- Converted all repository documentation, runtime prompts, agent instructions, manifests, comments, and examples to English.
- Added English-only validation so Japanese text cannot be reintroduced accidentally.

## 0.4.0

- Switched Claude Code to a native-first architecture with ultracode / Dynamic Workflows as the primary execution engine.
- Switched Codex to project-level `model_reasoning_effort = "ultra"` with proactive multi-agent delegation as the primary execution engine.
- Removed the policy of pre-allocating a fixed agent graph or agent count.
- Reclassified bundled Claude custom agents as fallback specialists.
- Explicitly separated execution topology from Git/review topology.
- Limited long-task state to durable engineering state and reduced duplication of runtime-native workflow state.
- Simplified root-context policy to requirements, decisions, integration state, and verification evidence.
- Added safe fallbacks for environments where native orchestration is unavailable.

## 0.3.0

- Added a native Marketplace for Codex CLI and supported Codex surfaces.
- Added a portable Agent Plugins 1.0 manifest.
- Added a Codex compatibility manifest and lifecycle hooks.
- Converted the orchestrate Skill to a Claude Code / Codex runtime-adapter model.
- Added a safe fallback strategy using Codex built-in explorer / worker roles and fresh subagents.
- Improved stale project-profile detection using manifest modification times.
- Extended CI validation to Claude/Codex manifests, versions, and hook compatibility.

## 0.2.0

- Added a context firewall that treats the root session as a control plane and removes manual `/clear` / `/compact` from normal operation.
- Added project-bootstrap and manifest freshness tracking.
- Added durable local state for automatic compaction summaries and session runtime snapshots.
- Updated GitHub Actions to immutable SHA pins for checkout v7.0.1 and setup-python v7.0.0.
- Added Dependabot updates for GitHub Actions.
- Changed `gh-stack` setup to force-refresh the latest stable release.

## 0.1.0

- Initial release.
- Added the automatic orchestration Skill.
- Added investigator, reviewer, verifier, worktree-worker, and task-planner agents.
- Added long-task state management.
- Added the GitHub native Stacked PR workflow.
- Added SessionStart, UserPromptSubmit, and PreCompact hooks.
