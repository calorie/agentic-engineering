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


def profile_is_stale(cwd: Path, project_path: Path, project_text: str) -> bool:
    if "agentic-profile: pending" in project_text:
        return True
    if (cwd / ".agentic" / "PROFILE_STALE").exists():
        return True
    try:
        profile_mtime = project_path.stat().st_mtime
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

    chunks = [
        "Agentic Engineering が有効です。ルート会話は control-plane とし、実質的なタスクは規模に応じ fresh-context subagent / isolated worktree、Stacked PR、durable state を自動選択してください。人間に context clear や並列数の管理を委ねないでください。",
        f"現在の agent runtime: {runtime}。runtime 固有機能が利用できない場合は安全に縮退してください。",
    ]

    project_path = cwd / ".agentic" / "PROJECT.md"
    project = read_text(project_path, MAX_PROJECT_CHARS)
    if project:
        chunks.append("プロジェクト固有情報:\n" + project)
    if profile_is_stale(cwd, project_path, project):
        chunks.append("Project profile は未初期化または stale。次の実質的な開発要求で project-bootstrap を適用してください。")

    active_file = cwd / ".agent" / "ACTIVE_TASK"
    task_id = read_text(active_file, 256).splitlines()[0].strip() if active_file.exists() else ""
    if task_id and "/" not in task_id and ".." not in task_id:
        task_dir = cwd / ".agent" / "tasks" / task_id
        pieces = []
        for name, title, lim in [
            ("SPEC.md", "SPEC", MAX_TASK_CHARS // 3),
            ("STATE.md", "STATE", MAX_TASK_CHARS // 3),
            ("COMPACT.md", "LAST COMPACTION", MAX_TASK_CHARS // 6),
            ("RUNTIME.md", "RUNTIME", MAX_TASK_CHARS // 6),
        ]:
            value = read_text(task_dir / name, lim)
            if value:
                pieces.append(f"{title}:\n{value}")
        if pieces:
            chunks.append(f"再開対象の長期タスク: {task_id}\n" + "\n\n".join(pieces))

    hook_output = {
        "hookEventName": "SessionStart",
        "additionalContext": "\n\n".join(chunks),
    }

    # Claude Code は watchPaths を使って FileChanged hook を補助できる。
    # Codex では未対応なので出力しない。
    if runtime == "Claude Code":
        watch_paths = [str(cwd / name) for name in WATCH_NAMES if (cwd / name).exists()]
        hook_output["watchPaths"] = watch_paths

    print(json.dumps({"hookSpecificOutput": hook_output}, ensure_ascii=False))


if __name__ == "__main__":
    main()
