# agentic-engineering

Claude Code の開発オーケストレーションを複数リポジトリへ中央配布するための **Marketplace 兼 Plugin リポジトリ**です。

## 目的

各プロジェクトに巨大な `.claude/` 設定をコピーせず、次を中央で versioning します。

- substantive task の自動オーケストレーション
- main context を守る調査・レビュー・検証の subagent 化
- 独立実装の worktree 分離
- 長期タスクの durable state
- GitHub native Stacked PR の自動選択
- session start / prompt / compact 時の軽量 hook

プロジェクト側には `CLAUDE.md`、`AGENTS.md`、`.agentic/PROJECT.md`、Plugin 参照設定だけを残します。

## 構造

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

## 中央配布

### Claude Code CLI / 個人・小規模チーム

GitHub にこの repository を公開またはアクセス可能な形で配置した後:

```bash
claude plugin marketplace add <owner>/agentic-engineering
claude plugin install agentic-engineering@agentic-engineering
```

Template Repository の `.claude/settings.json` には `extraKnownMarketplaces` と `enabledPlugins` を入れておきます。

### Team / Enterprise

Organization settings の Plugins からこの GitHub repository を Marketplace として接続し、`agentic-engineering` を **Required** または **Installed by default** にします。自動同期を有効にすると、中央 repository の更新を組織へ継続配布できます。

詳細は `docs/ORG-ROLLOUT.md` を参照してください。

## 開発

```bash
python3 scripts/validate.py
```

ローカルで直接試す場合:

```bash
claude --plugin-dir ./plugins/agentic-engineering
```

## Versioning

Plugin 名 `agentic-engineering` は公開後に変更しません。更新時は `plugin.json` と `marketplace.json` の version を同時に上げ、CHANGELOG を更新します。

## Repository owner の初期設定

中央 repository を GitHub に作成したら、任意ですが manifest の homepage を実 URL に置換できます。

```bash
./scripts/configure-owner.sh <github-owner>
```

## Context firewall

0.2.0 以降は root session を control-plane として扱い、substantive task の execution を fresh context へ寄せます。auto-compaction 前後と session 終了時には active long task の local state を hooks が保存します。Plugin 単独では Claude Code の現在 session を任意 prompt で `/clear` できないため、manual clear を要求せず context 汚染を構造的に抑える方針です。

## Dependency freshness

GitHub Actions は latest stable release の full SHA pin + Dependabot を標準とします。Plugin 自体は Python standard library のみを使用し、追加 runtime package dependency を持ちません。
