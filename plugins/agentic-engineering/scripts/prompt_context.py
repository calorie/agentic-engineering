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
    runtime = "Codex" if os.environ.get("PLUGIN_ROOT") else "Claude Code"
    stale = profile_is_stale(cwd, cwd / ".agentic" / "PROJECT.md")

    if runtime == "Claude Code":
        execution = (
            "Claude Code ultracode/Dynamic Workflows に execution topology、fan-out、agent 数、"
            "runtime verification orchestration を任せる。Plugin の固定 custom-agent graph を先に作らない。"
        )
    else:
        execution = (
            "Codex Ultra の proactive delegation に execution topology と agent 数を任せる。"
            "ユーザーへ subagent 利用を要求せず、Claude 固有 graph を模倣しない。"
        )

    parts = [
        "実質的な開発要求では agentic-engineering:orchestrate を engineering-policy layer として適用する。",
        execution,
        "Agentic Engineering は project constraints、safe write isolation、durable engineering state、verification evidence、Git/PR topology を管理する。",
        "人間に clear、compact、parallelism、agent 数を管理させない。",
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
