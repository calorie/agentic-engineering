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
            "Delegate execution topology, fan-out, agent count, and runtime verification orchestration to "
            "Claude Code ultracode/Dynamic Workflows. Do not build a fixed custom-agent graph first."
        )
    else:
        execution = (
            "Delegate execution topology and agent count to Codex Ultra proactive delegation. "
            "Do not require the user to request subagents and do not copy a Claude-specific graph into Codex."
        )

    parts = [
        "For substantive engineering requests, apply agentic-engineering:orchestrate as an engineering-policy layer.",
        execution,
        "If Superpowers skills are available, use methodology skills such as TDD, systematic debugging, and verification inside the native workflow. "
        "Do not let subagent-driven-development, dispatching-parallel-agents, or executing-plans create a nested scheduler under native orchestration.",
        "Deduplicate equivalent code review, verification, and worktree setup across the runtime, Superpowers, and Agentic Engineering.",
        "Agentic Engineering owns project constraints, safe write isolation, durable engineering state, verification evidence, and Git/PR topology.",
        "Do not ask the user to manage clear, compact, parallelism, or agent count.",
    ]
    if stale:
        parts.append(
            "The project profile is uninitialized or stale. Run a lightweight project-bootstrap before starting the substantive task."
        )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": " ".join(parts),
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
