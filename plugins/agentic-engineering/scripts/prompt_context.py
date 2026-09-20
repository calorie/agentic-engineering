#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

WATCH_NAMES = (
    "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb",
    "pyproject.toml", "uv.lock", "requirements.txt", "Pipfile", "poetry.lock",
    "Cargo.toml", "Cargo.lock", "go.mod", "go.sum", "Gemfile", "Gemfile.lock",
    "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts",
    "composer.json", "composer.lock", "Dockerfile", "Makefile", "Taskfile.yml", "justfile",
)


def profile_is_stale(cwd: Path, project: Path) -> bool:
    try:
        text = project.read_text(encoding="utf-8")
    except OSError:
        return True
    if "agentic-profile: pending" in text:
        return True
    if (cwd / ".agentic" / "PROFILE_STALE").exists():
        return True
    try:
        profile_mtime = project.stat().st_mtime
    except OSError:
        return True
    for name in WATCH_NAMES:
        path = cwd / name
        try:
            if path.exists() and path.stat().st_mtime > profile_mtime:
                return True
        except OSError:
            continue
    return False


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    cwd = Path(payload.get("cwd") or os.getcwd()).resolve()
    project = cwd / ".agentic" / "PROJECT.md"
    stale = profile_is_stale(cwd, project)

    parts = [
        "実質的な開発要求では agentic-engineering の orchestrate Skill を適用する。ルート会話を control-plane とし、"
        "大量調査・実装試行・長いログは fresh-context subagent / isolated execution context へ逃がす。"
        "人間に clear、compact、subagent数、並列数を管理させない。小さな作業は過剰分散しない。"
    ]
    if stale:
        parts.append("Project profile が未初期化または stale。現在タスクを始める前に project-bootstrap を軽量実行する。")

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": " ".join(parts),
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
