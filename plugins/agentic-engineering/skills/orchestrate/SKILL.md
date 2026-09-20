---
name: orchestrate
description: Use this skill for substantive software-engineering requests such as implementing a feature, fixing a non-trivial bug, refactoring, migrating code, adding tests, changing an API or schema, or performing multi-file development work. It autonomously chooses direct implementation, subagents, isolated worktrees when available, long-task state, review, verification, and GitHub stacked pull requests so the user does not have to manage context windows or agent parallelism. Works with Claude Code and Codex.
version: 0.3.0
---

# 自律オーケストレーション

実装要求を受けたら、ユーザーに「何個エージェントを立てるか」「context をどう保つか」「いつ clear/compact するか」を決めさせず、作業形状を自動決定する。

## 0. Context firewall

ルート会話は control-plane とする。要求、制約、意思決定、統合結果だけを保持し、大量探索・長いログ・実装の試行錯誤を極力置かない。

- 新しい実質的タスクが前タスクと無関係なら、過去の実装詳細を前提にせず fresh-context subagent / isolated execution context で実行する。
- substantive なタスクでは、root context を実装 worker として使うより fresh context への委譲を優先する。ごく小さく局所的な編集だけ直接実装してよい。
- 大量 fan-out や多段 orchestration では、現在の runtime が提供する orchestration 機構を優先し、中間結果を root context に大量転載しない。
- /clear や /compact をユーザーへ運用手順として要求しない。runtime の compaction と durable state を利用する。

### Runtime adapter

Claude Code:
- 調査: investigator
- 独立実装: worktree isolation が安全な場合 worktree-worker
- 計画: task-planner
- レビュー: reviewer
- 検証: verifier
- 大規模 fan-out では利用可能なら Dynamic Workflow を使い、中間結果を root conversation から分離する。

Codex:
- 調査は built-in explorer または読み取り専用の fresh subagent を優先する。
- 実装は built-in worker または scoped subagent を利用できるが、同じ checkout に対する並列書き込みは避ける。
- Codex-managed Worktree / 独立 checkout を利用できる場合だけ、独立した書き込みタスクを並列化する。
- plan / review / verify は fresh subagent に役割を明示して委譲する。カスタム agent 定義がなくても動作するようにする。
- subagent の中間ログを root thread へ転載せず、結論・根拠・変更・検証結果だけを集約する。

runtime 固有機能が利用できない場合は、無理に模倣せず、読み取り並列 + 書き込み逐次へ安全に縮退する。

## 1. 最初に project profile と作業形状を判定する

.agentic/PROJECT.md が pending、または profile が stale と判定された場合、まず project-bootstrap を適用する。全面的なドキュメント化はせず、現在タスクに必要な durable facts を確認すればよい。

その後、次の順に判断する。

1. 小さく局所的: 変更境界が明確で、依存関係が少なく、短い検証で閉じるなら直接実装する。
2. 調査が重い: repository 全体の探索や複数の独立質問があるなら fresh subagents を並列利用し、親へは要約と根拠だけ戻す。
3. 独立した書き込み単位が複数: 互いに同じファイル・schema・未確定 interface を触らず、かつ worktree / checkout isolation が確保できる場合だけ並列実装する。
4. 依存するレビュー単位が複数: 並列 worker ではなく、下位から上位へ GitHub Stacked PR を構成する。stacked-pr Skill の手順を使う。
5. 長期化する: 複数セッション、複数 PR、長い migration、または context compaction を跨ぐ見込みなら long-task Skill の durable state を開始する。

必要なら fresh planner subagent を先に使い、依存関係だけを整理する。明白な小タスクでは planner を呼ばない。

## 2. コンテキストを節約する

- root context は要求、意思決定、現在状態、統合判断に集中させる。
- 大量検索、大量ログ、広域調査、独立レビューは subagent に逃がす。
- subagent には質問を狭く与え、返却は結論・根拠・影響・未解決点に限定する。
- 大きな出力をそのまま root context に転載しない。
- unrelated な新規タスクを同一長期状態に混ぜない。
- repository から確認できた、将来も繰り返し必要になる project 固有の非自明な事実だけを .agentic/PROJECT.md に短く反映する。汎用方針や一時的な状態は書かない。

## 3. 並列化は安全に独立して進められるかで決める

並列化してよい代表例:
- 独立した調査質問
- 実装後の reviewer / verifier
- worktree で分離された明確に別モジュールの実装
- worktree で分離可能な機械的 migration の独立ファイル群

逐次にする代表例:
- 同じ checkout への複数 writer
- 同じファイルを触る変更
- DB schema や共有型の競合
- interface がまだ確定していない producer / consumer
- Stacked PR の上下レイヤー
- 最終 integration

write worker を使う場合、各 worker が別 checkout / worktree にいることを確認する。結果を統合する前に diff と検証結果を確認する。

## 4. PR トポロジーを自動選択する

- 1つの焦点ある差分でレビューできる → 1 PR
- 相互依存しない複数差分 → 独立 PR / worktree
- 基盤 → consumer の順に依存する複数差分 → Stacked PR

大きいから stack ではなく、依存しつつ別々にレビュー可能だから stack を選ぶ。

## 5. 実装後の品質ループ

1. 最小の関連検証を実行する。
2. substantive な変更では fresh-context reviewer subagent を使う。
3. 必要なら別の fresh verifier subagent で独立検証する。小さな変更では重複コストが高ければ省略可。
4. 指摘を修正して必要な検証を再実行する。
5. PR 単位がレビュー可能であることを確認する。

## 6. 長期タスクの checkpoint

次のタイミングで durable state を更新する:
- 設計や受入条件が確定したとき
- PR / stack layer を完了したとき
- 大きな blocker が発生したとき
- セッション終了や context 圧縮が近いと判断したとき

詳細は long-task Skill を参照する。

## 追加資料

- references/parallelism.md — 並列化判断
- references/review-topology.md — PR / stack の選択
- references/context-policy.md — context の運用
