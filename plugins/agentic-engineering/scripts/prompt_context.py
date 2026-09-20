#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    cwd = Path(payload.get("cwd") or os.getcwd()).resolve()
    project = cwd / ".agentic" / "PROJECT.md"
    stale = cwd / ".agentic" / "PROFILE_STALE"
    pending = False
    try:
        pending = "agentic-profile: pending" in project.read_text(encoding="utf-8")
    except OSError:
        pass

    parts = [
        "実質的な開発要求では agentic-engineering:orchestrate を適用する。ルート会話を control-plane とし、"
        "大量調査・実装試行・長いログは fresh-context subagent / workflow / worktree へ逃がす。"
        "人間に /clear、/compact、subagent数、並列数を管理させない。小さな作業は過剰分散しない。"
    ]
    if pending or stale.exists():
        parts.append("Project profile が未初期化または stale。現在タスクを始める前に project-bootstrap を軽量実行する。")

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": " ".join(parts),
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
