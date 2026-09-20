#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys
from pathlib import Path


def read(path):
    try: return path.read_text(encoding='utf-8').strip()
    except OSError: return ''

def main():
    try: p=json.load(sys.stdin)
    except Exception: p={}
    cwd=Path(p.get('cwd') or os.getcwd()).resolve()
    task=read(cwd/'.agent'/'ACTIVE_TASK').splitlines()
    if not task: return
    task_id=task[0].strip()
    if not task_id or '/' in task_id or '..' in task_id: return
    summary=(p.get('compact_summary') or '').strip()
    if not summary: return
    path=cwd/'.agent'/'tasks'/task_id/'COMPACT.md'
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('# Last automatic compaction summary\n\n'+summary+'\n', encoding='utf-8')
    except OSError: pass

if __name__ == '__main__': main()
