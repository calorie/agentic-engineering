---
name: stacked-pr
description: This skill should be used when a change contains multiple dependent but independently reviewable units, when the user mentions stacked PRs, or when orchestration determines that a foundation/interface change should land below one or more consumer changes. It uses GitHub native stacked pull requests through the gh stack extension when available.
version: 0.2.0
---

# GitHub Stacked PR

依存する変更を小さくレビュー可能なレイヤーへ分ける。

## 選択条件

Stacked PR を使う:
- 各レイヤーに明確な責務がある。
- 上位レイヤーが下位レイヤーへ依存する。
- 各レイヤーを単体でレビューする価値がある。

使わない:
- 独立タスク。別 PR にする。
- 1つの小さい変更。単一 PR にする。
- 分割すると中間状態が壊れ、各レイヤーに検証可能性がない。

## 前提確認

1. GitHub remote と `gh` authentication を確認する。
2. `gh stack --help` が利用可能か確認する。
3. 未導入で、環境変更が許可されるなら `gh extension install github/gh-stack --force` で latest stable release を導入・更新する。
4. Stack の全 branch は同一 repository 内に置く。cross-fork stack を作らない。

## 作成

trunk 上で最下位レイヤーを開始する:

```bash
gh stack init <branch>
```

実装・検証・commit 後、次の dependent layer を追加する:

```bash
gh stack add <branch>
```

同様に必要な層だけ積む。レビュー単位を増やすためだけに stack を深くしない。

## 提出

remote への PR 作成がタスク意図と repository policy で許可される場合:

```bash
gh stack submit
```

許可が不明なら local stack を完成させ、提出直前で状態を報告する。

## 下位レイヤーの修正

正しい layer に戻って修正し、上位で workaround しない。

```bash
gh stack checkout <branch>
# edit + commit
gh stack rebase --upstack
gh stack push
```

## 同期

通常の同期:

```bash
gh stack sync
```

merged branch も整理する場合:

```bash
gh stack sync --prune
```

競合時は `gh stack rebase` で対話的に解消し、`gh stack push` で反映する。

## Agent 並列化との関係

同じ stack の上下 layer は原則として別 worker に同時実装させない。下位の変更が上位へ cascade するため、stack 内は sequential、独立 stack 間は parallel を基本とする。

## 追加資料

- `references/commands.md` — コマンド早見表
