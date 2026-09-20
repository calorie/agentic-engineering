#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

MAX_PROJECT_CHARS = 5000
MAX_TASK_CHARS = 6000
WATCH_NAMES = (
    "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb",
    "pyproject.toml", "uv.lock", "requirements.txt", "Pipfile", "poetry.lock",
    "Cargo.toml", "Cargo.lock", "go.mod", "go.sum", "Gemfile", "Gemfile.lock",
    "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts",
    "composer.json", "composer.lock", "Dockerfile", "Makefile", "Taskfile.yml", "justfile",
)


def read_text(path: Path, limit: int) -> str:
    try:
        text = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError):
        return ""
    if len(text) > limit:
        return text[:limit] + "\n…(省略)"
    return text


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    cwd = Path(payload.get("cwd") or os.getcwd()).resolve()
    chunks = [
        "Agentic Engineering が有効です。ルート会話は control-plane とし、実質的なタスクは規模に応じ fresh-context subagent / workflow / worktree、Stacked PR、durable state を自動選択してください。人間に context clear や並列数の管理を委ねないでください。"
    ]

    project_path = cwd / ".agentic" / "PROJECT.md"
    project = read_text(project_path, MAX_PROJECT_CHARS)
    if project:
        chunks.append("プロジェクト固有情報:\n" + project)
    if "agentic-profile: pending" in project or (cwd / ".agentic" / "PROFILE_STALE").exists():
        chunks.append("Project profile は未初期化または stale。次の実質的な開発要求で project-bootstrap を適用してください。")

    active_file = cwd / ".agent" / "ACTIVE_TASK"
    task_id = read_text(active_file, 256).splitlines()[0].strip() if active_file.exists() else ""
    if task_id and "/" not in task_id and ".." not in task_id:
        task_dir = cwd / ".agent" / "tasks" / task_id
        pieces=[]
        for name, title, lim in [
            ("SPEC.md", "SPEC", MAX_TASK_CHARS//3),
            ("STATE.md", "STATE", MAX_TASK_CHARS//3),
            ("COMPACT.md", "LAST COMPACTION", MAX_TASK_CHARS//6),
            ("RUNTIME.md", "RUNTIME", MAX_TASK_CHARS//6),
        ]:
            value=read_text(task_dir/name, lim)
            if value:
                pieces.append(f"{title}:\n{value}")
        if pieces:
            chunks.append(f"再開対象の長期タスク: {task_id}\n" + "\n\n".join(pieces))

    watch_paths=[str(cwd/name) for name in WATCH_NAMES if (cwd/name).exists()]
    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n\n".join(chunks),
            "watchPaths": watch_paths,
        }
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
