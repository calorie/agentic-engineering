# agentic-engineering

Claude Code のコンテキスト管理、並列実行、長期タスク、レビュー、GitHub Stacked PR を複数リポジトリへ中央配布するための **Claude Code Marketplace / Plugin** です。

- Plugin / Marketplace: https://github.com/calorie/agentic-engineering
- 推奨 Project Template: https://github.com/calorie/agentic-repo-template

## 最短で使う

新規プロジェクトでは、個別に Plugin を組み込むより `agentic-repo-template` から開始することを推奨します。

Template から作成したリポジトリで:

```bash
./scripts/setup-agentic.sh
claude
```

以後は通常どおり、やりたいことだけを Claude Code に依頼します。

```text
ユーザー検索機能を追加して。名前とメールアドレスで検索できるようにする。
```

並列化、worktree、長期タスクの state、レビュー context、Stacked PR の利用判断は Plugin 側の orchestration policy が行います。

## Plugin だけをインストールする

Claude Code から Marketplace を登録して Plugin をインストールします。

```bash
claude plugin marketplace add calorie/agentic-engineering
claude plugin install agentic-engineering@agentic-engineering
```

特定リポジトリだけで共有したい場合は project scope を使用できます。

```bash
claude plugin install agentic-engineering@agentic-engineering --scope project
```

既存セッションへ即時反映されない場合は `/reload-plugins` を実行するか、新しい Claude Code セッションを開始してください。

## Template Repository との関係

`agentic-repo-template` は project 側の薄い設定だけを持ちます。

```text
agentic-engineering
  └─ 中央管理
     ├─ Skills
     ├─ Agents
     ├─ Hooks
     └─ orchestration policy

agentic-repo-template / 派生 project
  ├─ CLAUDE.md
  ├─ AGENTS.md
  ├─ .claude/settings.json
  ├─ .agentic/PROJECT.md
  └─ .agent/tasks/
```

Template の `.claude/settings.json` はこの Marketplace (`calorie/agentic-engineering`) を参照し、Plugin を project で有効化する設定を持っています。

外部 Marketplace の Plugin は各開発環境で初回インストールが必要です。Template から作成した project では `./scripts/setup-agentic.sh` が Marketplace 登録、Plugin install、GitHub Stacked PR extension の setup、診断まで行います。Organization の managed plugin として配布している場合は Plugin install を省略できます。

## 何を中央管理するか

各 project に巨大な `.claude/` をコピーせず、次を versioning します。

- substantive task の自動オーケストレーション
- root context を control-plane に限定する context firewall
- 調査・レビュー・検証の fresh subagent 化
- 独立実装の worktree 分離
- 長期タスクの durable state と compact / session state 復元
- project build/test/toolchain の自動 discovery
- GitHub native Stacked PR の自動選択
- SessionStart / UserPromptSubmit / PreCompact / PostCompact / SessionEnd hooks

## Context management

利用者が通常 `/clear` や `/compact` のタイミングを管理しなくてよいことを目標にしています。

root session は control-plane として扱い、大量の探索・実装試行・検証ログを fresh subagent / workflow / worktree へ逃がします。長期タスクでは durable state を `.agent/tasks/` に残し、auto-compaction やセッション境界をまたいで復元します。

Claude Code Plugin API は任意の top-level prompt の直前に現在 session を強制的に `/clear` する API を提供していないため、「毎要求を物理的に必ず新 context にする」のではなく、**root context を汚さない execution model** で対応します。

## GitHub Stacked PR

依存関係のある複数の review unit に分割する価値がある場合だけ、GitHub native `gh stack` を使用します。独立タスクは別 worktree / PR、単一の小変更は通常の単一 PR とします。

Template の setup script は GitHub CLI が利用可能な場合に `github/gh-stack` を最新版へ更新します。

## Team / Enterprise

Organization 管理下では、Claude の Organization settings からこの Marketplace / Plugin を配布し、必要に応じて **Required** または **Installed by default** にしてください。

中央 Plugin を managed distribution すれば、各 project repository に Skills / Agents / Hooks を複製する必要はありません。

詳細: `docs/ORG-ROLLOUT.md`

## Plugin 開発

構成:

```text
agentic-engineering/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── agentic-engineering/
        ├── .claude-plugin/plugin.json
        ├── agents/
        ├── hooks/hooks.json
        ├── scripts/
        └── skills/
```

validation:

```bash
python3 scripts/validate.py
```

ローカル版を直接試す:

```bash
claude --plugin-dir ./plugins/agentic-engineering
```

## Versioning

Plugin 名 `agentic-engineering` と Marketplace 名 `agentic-engineering` は互換性のため固定します。

Plugin の動作を変更するときは `plugins/agentic-engineering/.claude-plugin/plugin.json` と `.claude-plugin/marketplace.json` の version を同時に更新し、`CHANGELOG.md` を更新します。

## Dependency policy

- Plugin runtime は Python standard library のみを使用し、追加 package dependency を持ちません。
- GitHub Actions は最新安定版を full commit SHA で pin し、Dependabot で追従します。
- project 固有の package dependency は project constraint と互換な最新 stable を選択し、lockfile を更新する方針です。

## Security

Claude Code Plugin は hooks やツール経由でローカル環境上の処理を実行できます。インストール前にこの repository の内容を確認し、信頼できる source として扱える場合だけ導入してください。
