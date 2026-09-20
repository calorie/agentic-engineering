#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys
from pathlib import Path


def main():
    try: p=json.load(sys.stdin)
    except Exception: p={}
    cwd=Path(p.get("cwd") or os.getcwd()).resolve()
    changed=Path(p.get("file_path") or "")
    marker=cwd/".agentic"/"PROFILE_STALE"
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(f"Dependency/toolchain manifest changed: {changed.name}\n", encoding="utf-8")
    except OSError:
        pass

if __name__ == '__main__': main()
