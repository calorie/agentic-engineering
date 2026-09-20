---
name: orchestrate
description: This skill should be used for substantive software-engineering requests such as implementing a feature, fixing a non-trivial bug, refactoring, migrating code, adding tests, changing an API or schema, or performing multi-file development work. It should autonomously choose direct implementation, subagents, worktree-isolated parallel workers, long-task state, and GitHub stacked pull requests as appropriate so the user does not have to manage context windows or agent parallelism.
version: 0.2.0
---

# 自律オーケストレーション

実装要求を受けたら、ユーザーに「何個エージェントを立てるか」「context をどう保つか」「いつ clear/compact するか」を決めさせず、作業形状を自動決定する。

## 0. Context firewall

ルート会話は **control-plane** とする。要求、制約、意思決定、統合結果だけを保持し、大量探索・長いログ・実装の試行錯誤を極力置かない。

- 新しい実質的タスクが前タスクと無関係なら、過去の実装詳細を前提にせず fresh-context subagent / workflow / worktree worker で実行する。
- substantive なタスクでは、main context を実装 worker として使うより fresh context への委譲を優先する。ごく小さく局所的な編集だけ直接実装してよい。
- 大量 fan-out や多段 orchestration では Dynamic Workflow を優先し、中間結果を script variables に保持して main context へ戻すのは最終要約だけにする。
- `/clear` や `/compact` をユーザーへ運用手順として要求しない。Claude Code の auto-compaction と durable state を利用する。

## 1. 最初に project profile と作業形状を判定する

`.agentic/PROJECT.md` が `pending`、または `.agentic/PROFILE_STALE` が存在する場合、まず `project-bootstrap` を適用する。全面的なドキュメント化はせず、現在タスクに必要な durable facts を確認すればよい。

その後、次の順に判断する。

1. **小さく局所的**: 変更境界が明確で、依存関係が少なく、短い検証で閉じるならメインセッションで直接実装する。
2. **調査が重い**: repository 全体の探索や複数の独立質問があるなら `investigator` を並列利用し、親へは要約と根拠だけ戻す。
3. **独立した書き込み単位が複数**: 互いに同じファイル・schema・未確定 interface を触らない場合だけ `worktree-worker` を並列利用する。
4. **依存するレビュー単位が複数**: 並列 worker ではなく、下位から上位へ GitHub Stacked PR を構成する。`stacked-pr` Skill の手順を使う。
5. **長期化する**: 複数セッション、複数 PR、長い migration、または context compaction を跨ぐ見込みなら `long-task` Skill の durable state を開始する。

必要なら `task-planner` を先に使い、依存関係だけを整理する。明白な小タスクでは planner を呼ばない。

## 2. コンテキストを節約する

- main context は「要求、意思決定、現在の実装、統合判断」に集中させる。
- 大量検索、大量ログ、広域調査、独立レビューは subagent に逃がす。
- subagent には質問を狭く与え、返却は結論・根拠・影響・未解決点に限定する。
- 大きな出力をそのまま main context に転載しない。
- unrelated な新規タスクを同一長期セッションに混ぜない。
- repository から確認できた、将来も繰り返し必要になる project 固有の非自明な事実だけを `.agentic/PROJECT.md` に短く反映する。汎用方針や一時的な状態は書かない。

## 3. 並列化は「安全に独立して進められるか」で決める

並列化してよい代表例:
- 独立した調査質問
- 実装後の reviewer / verifier
- 明確に分離されたモジュール
- 機械的 migration の独立ファイル群

逐次にする代表例:
- 同じファイルを触る変更
- DB schema や共有型の競合
- interface がまだ確定していない producer / consumer
- Stacked PR の上下レイヤー
- 最終 integration

worktree worker を使う場合、各 worker が親の checkout を直接変更しないことを前提にする。結果を統合する前に diff と検証結果を確認する。

## 4. PR トポロジーを自動選択する

- 1つの焦点ある差分でレビューできる → 1 PR
- 相互依存しない複数差分 → 独立 PR / worktree
- 基盤 → consumer の順に依存する複数差分 → Stacked PR

「大きいから stack」ではなく「依存しつつ別々にレビュー可能だから stack」を選ぶ。

## 5. 実装後の品質ループ

1. 最小の関連検証を実行する。
2. substantive な変更では fresh-context `reviewer` を使う。
3. `verifier` で独立検証する。小さな変更では重複コストが高ければ省略可。
4. 指摘を修正して必要な検証を再実行する。
5. PR 単位がレビュー可能であることを確認する。

## 6. 長期タスクの checkpoint

次のタイミングで durable state を更新する:
- 設計や受入条件が確定したとき
- PR / stack layer を完了したとき
- 大きな blocker が発生したとき
- セッション終了や context 圧縮が近いと判断したとき

詳細は `long-task` Skill を参照する。

## 追加資料

- `references/parallelism.md` — 並列化判断
- `references/review-topology.md` — PR / stack の選択
- `references/context-policy.md` — context の運用
