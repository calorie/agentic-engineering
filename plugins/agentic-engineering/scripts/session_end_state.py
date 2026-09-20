#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path


def read(path):
    try: return path.read_text(encoding='utf-8').strip()
    except OSError: return ''

def run(cwd, *args):
    try:
        return subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=0.5).stdout.strip()
    except Exception:
        return ''

def main():
    try: p=json.load(sys.stdin)
    except Exception: p={}
    cwd=Path(p.get('cwd') or os.getcwd()).resolve()
    lines=read(cwd/'.agent'/'ACTIVE_TASK').splitlines()
    if not lines: return
    task_id=lines[0].strip()
    if not task_id or '/' in task_id or '..' in task_id: return
    branch=run(cwd,'git','branch','--show-current')
    head=run(cwd,'git','rev-parse','HEAD')
    status=run(cwd,'git','status','--short')
    content=f"# Runtime snapshot\n\n- branch: `{branch}`\n- HEAD: `{head}`\n\n## Working tree\n\n```text\n{status}\n```\n"
    path=cwd/'.agent'/'tasks'/task_id/'RUNTIME.md'
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    except OSError: pass

if __name__ == '__main__': main()
