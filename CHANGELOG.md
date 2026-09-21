# Changelog

## 0.5.0

- Replaced always-on maximum-effort policy with cost-aware escalation.
- Claude Code now starts from normal model effort; ultracode is an optional session-level accelerator for high-leverage work.
- Codex no longer requires project-level Ultra reasoning; native multi-agent capability remains available.
- Removed Plugin hooks and runtime Python state/context scripts.
- Removed custom Claude agents.
- Removed separate doctor, project-bootstrap, and long-task Skills; their durable policy was folded into the minimal orchestrate Skill.
- Removed orchestration reference documents and kept only two Skills: orchestrate and stacked-pr.
- Kept Superpowers as methodology and Ponytail as implementation-minimization policy without introducing nested schedulers.
- Reduced persistent state to project facts and optional SPEC / STATE / DECISIONS files.

## 0.4.2

- Added an explicit Superpowers compatibility contract.
- Kept Claude ultracode / Dynamic Workflows and Codex Ultra as the sole default owners of execution topology.
- Classified Superpowers TDD, systematic debugging, verification, and review disciplines as composable methodology.
- Prevented nested scheduling from `subagent-driven-development`, `dispatching-parallel-agents`, and `executing-plans` when native proactive orchestration is active.
- Added deduplication rules for code review, verification, and worktree setup.
- Added compatibility guidance for brainstorming, planning, worktree lifecycle, and branch-finishing skills.

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
