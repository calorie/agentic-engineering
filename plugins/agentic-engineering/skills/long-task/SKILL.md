---
name: long-task
description: This skill should be used when work is likely to span multiple sessions, context compactions, several pull requests, a long migration, or a sequence of dependent implementation phases. It externalizes only durable state so work can resume without relying on chat history.
version: 0.2.0
---

# 長期タスク状態管理

会話履歴を唯一の状態にしない。必要になった時点で `.agent/tasks/<task>/` を作る。

## ファイル

### `SPEC.md`

安定した情報だけを置く:
- goal
- acceptance criteria
- constraints
- non-goals
- 重要な interface 契約

### `STATE.md`

現在進行形の情報だけを置く:
- 現在の branch / stack layer
- 完了済み項目
- 変更済みファイルの要点
- verification と結果
- blocker
- 次の具体的アクション

### `COMPACT.md` / `RUNTIME.md`

Plugin hooks が自動生成する local runtime state。`COMPACT.md` は直近の auto/manual compaction summary、`RUNTIME.md` は session 終了時の branch / HEAD / working-tree snapshot。手動編集を前提にしない。Git 管理外とする。

### `DECISIONS.md`

将来の実装者が理由を知らないと再判断する重要事項だけを置く。ログにはしない。

## Active task

作業中タスク ID を `.agent/ACTIVE_TASK` に1行で記録する。SessionStart hook がこのファイルを見て STATE / SPEC を次セッションへ自動的に戻す。

## 更新タイミング

毎 tool call 後には更新しない。以下だけで更新する:
- 設計が確定した
- reviewable unit を完了した
- blocker が変わった
- session を終了する
- compaction を跨ぎそう

## 完了

タスク完了後は `.agent/ACTIVE_TASK` を削除する。STATE は既定で Git 管理外とし、SPEC / DECISIONS はチーム共有の価値がある場合だけ commit する。

詳細な雛形は `references/templates.md` を参照する。
