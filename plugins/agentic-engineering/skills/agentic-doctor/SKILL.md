---
name: agentic-doctor
description: Diagnose Agentic Engineering native-first setup: Claude Code ultracode readiness, Codex Ultra project configuration, plugin loading, project overlay, worktree support, GitHub CLI authentication, and native stacked-PR availability.
argument-hint: "[optional focus]"
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Bash"]
---

# Agentic Engineering Doctor

PASS / WARN / FAIL で確認する。

1. Git repository。
2. `.agentic/PROJECT.md` / `.agentic/agentic.json`。
3. Agentic schema が native-first policy を宣言している。
4. Claude adapter がある場合、Plugin enabled と ultracode request がある。
5. Claude CLI がある場合、`--effort ultracode` を受理する。
6. Codex adapter がある場合、`model_reasoning_effort = "ultra"` と `[agents] enabled = true`。
7. Codex Plugin が installed/enabled。
8. `git worktree`。
9. `gh auth status`。
10. `gh stack --help`。
11. active long task がある場合、SPEC / STATE が読める。
12. runtime transient state と durable engineering state を重複保存していない。

Native runtime の実効 capability が account/model/admin policy で制限される場合は、その制限を明示する。設定を勝手に破壊的変更しない。
