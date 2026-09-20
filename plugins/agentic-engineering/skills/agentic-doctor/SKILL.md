---
name: agentic-doctor
description: Diagnose the Agentic Engineering setup, plugin loading, project overlay, worktree support, GitHub CLI authentication, and native stacked-PR availability. Use when the user asks whether the orchestration setup is working or reports that automatic behavior is not activating.
argument-hint: "[optional focus]"
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Bash"]
---

# Agentic Engineering Doctor

次を確認し、PASS / WARN / FAIL で報告する。

1. Git repository であること。
2. `.agentic/PROJECT.md` と `.agentic/agentic.json` の存在。
3. project settings で `agentic-engineering@agentic-engineering` が有効か。
4. `git worktree` が利用可能か。
5. `gh auth status` が成功するか。
6. `gh stack --help` が利用可能か。
7. `.agent/ACTIVE_TASK` がある場合、対応する SPEC / STATE が読めるか。
8. generic policy と project-specific policy が重複して context を肥大化させていないか。

設定を勝手に破壊的変更せず、修正案とコマンドを提示する。
