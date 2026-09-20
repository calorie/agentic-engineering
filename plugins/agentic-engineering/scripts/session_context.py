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

    if runtime == "Claude Code":
        runtime_policy = (
            "Claude Code ultracode / Dynamic Workflows を実行エンジンの第一選択とする。"
            "Agentic Engineering は agent 数や固定 worker graph を決めず、project constraints、"
            "verification requirements、durable engineering state、Git/PR topology だけを補強する。"
        )
    else:
        runtime_policy = (
            "Codex Ultra の proactive multi-agent orchestration を実行エンジンの第一選択とする。"
            "Agentic Engineering は agent 数や固定 worker graph を決めず、project constraints、"
            "verification requirements、durable engineering state、Git/PR topology だけを補強する。"
        )

    chunks = [
        "Agentic Engineering 0.4 native-first policy が有効です。人間に context clear、parallelism、agent 数の管理を委ねないでください。",
        runtime_policy,
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
            ("COMPACT.md", "LAST COMPACTION (fallback)", MAX_TASK_CHARS // 6),
            ("RUNTIME.md", "RUNTIME (fallback)", MAX_TASK_CHARS // 6),
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

    if runtime == "Claude Code":
        hook_output["watchPaths"] = [str(cwd / name) for name in WATCH_NAMES if (cwd / name).exists()]

    print(json.dumps({"hookSpecificOutput": hook_output}, ensure_ascii=False))


if __name__ == "__main__":
    main()
