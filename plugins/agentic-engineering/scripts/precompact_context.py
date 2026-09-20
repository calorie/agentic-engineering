#!/usr/bin/env python3
from __future__ import annotations
import json, sys

def main():
    try: json.load(sys.stdin)
    except Exception: pass
    text=("自動 compaction を通常運用として受け入れる。現在の目的、未変更の受入条件、確定した設計判断、変更ファイル、検証結果、blocker、次の具体的アクションを優先して保持する。長期タスクでは .agent/tasks/<task>/STATE.md を正本とし、ユーザーへ /clear や /compact を要求しない。")
    print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreCompact','additionalContext':text}},ensure_ascii=False))
if __name__=='__main__': main()
