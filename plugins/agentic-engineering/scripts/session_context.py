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
        return text[:limit] + "\n...(truncated)"
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
            "Use Claude Code ultracode / Dynamic Workflows as the primary execution engine. "
            "Agentic Engineering must not choose a fixed worker graph or agent count; it should add only project constraints, "
            "verification requirements, durable engineering state, and Git/PR topology."
        )
    else:
        runtime_policy = (
            "Use Codex Ultra proactive multi-agent orchestration as the primary execution engine. "
            "Agentic Engineering must not choose a fixed worker graph or agent count; it should add only project constraints, "
            "verification requirements, durable engineering state, and Git/PR topology."
        )

    chunks = [
        "Agentic Engineering 0.4 native-first policy is active. Do not make the user manage context cleanup, parallelism, or agent count.",
        runtime_policy,
    ]

    project_path = cwd / ".agentic" / "PROJECT.md"
    project = read_text(project_path, MAX_PROJECT_CHARS)
    if project:
        chunks.append("Project-specific context:\n" + project)
    if profile_is_stale(cwd, project_path, project):
        chunks.append(
            "The project profile is uninitialized or stale. Apply project-bootstrap before the next substantive engineering task."
        )

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
            chunks.append(f"Long-running task to resume: {task_id}\n" + "\n\n".join(pieces))

    hook_output = {
        "hookEventName": "SessionStart",
        "additionalContext": "\n\n".join(chunks),
    }

    if runtime == "Claude Code":
        hook_output["watchPaths"] = [str(cwd / name) for name in WATCH_NAMES if (cwd / name).exists()]

    print(json.dumps({"hookSpecificOutput": hook_output}, ensure_ascii=False))


if __name__ == "__main__":
    main()
