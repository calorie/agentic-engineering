#!/usr/bin/env python3
from __future__ import annotations
import json, sys

def main():
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    text = (
        "Treat automatic compaction as normal operation. Preserve the current objective, unchanged acceptance criteria, "
        "confirmed design decisions, changed files, verification results, blockers, and the next concrete action. "
        "For long-running work, use .agent/tasks/<task>/STATE.md as the durable engineering source of truth. "
        "Do not ask the user to manage /clear or /compact."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreCompact", "additionalContext": text}}, ensure_ascii=False))

if __name__ == "__main__":
    main()
