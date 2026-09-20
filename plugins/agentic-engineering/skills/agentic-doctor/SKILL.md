---
name: agentic-doctor
description: Diagnose Agentic Engineering native-first setup: Claude Code ultracode readiness, Codex Ultra project configuration, plugin loading, project overlay, worktree support, GitHub CLI authentication, and native stacked-PR availability.
argument-hint: "[optional focus]"
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Bash"]
---

# Agentic Engineering Doctor

Report each check as PASS, WARN, or FAIL.

1. Confirm this is a Git repository.
2. Confirm `.agentic/PROJECT.md` and `.agentic/agentic.json` exist.
3. Confirm the Agentic schema declares the native-first policy.
4. If the Claude adapter is present, confirm the Plugin is enabled and ultracode is requested.
5. If the Claude CLI is present, confirm it accepts `--effort ultracode`.
6. If the Codex adapter is present, confirm `model_reasoning_effort = "ultra"` and `[agents] enabled = true`.
7. Confirm the Codex Plugin is installed and enabled.
8. Confirm `git worktree` is available.
9. Confirm `gh auth status` succeeds.
10. Confirm `gh stack --help` is available.
11. If an active long-running task exists, confirm its SPEC and STATE can be read.
12. Confirm transient runtime state is not being duplicated into durable engineering state.

If effective runtime capabilities are restricted by account, model, or administrator policy, state that limitation explicitly. Do not make destructive configuration changes automatically.
