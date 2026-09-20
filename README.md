# agentic-engineering

Claude Code と Codex のコンテキスト管理、並列実行、長期タスク、レビュー、GitHub Stacked PR を複数リポジトリへ中央配布するための **Agent Plugin / Marketplace** です。

- Plugin / Marketplace: https://github.com/calorie/agentic-engineering
- 推奨 Project Template: https://github.com/calorie/agentic-repo-template

## 目的

利用者は通常、やりたいことだけを入力します。

```text
ユーザー検索機能を追加して。名前とメールアドレスで検索できるようにする。
```

Plugin / AGENTS.md 側が task shape に応じて次を判断します。

- main/root context をどこまで使うか
- 調査やレビューを fresh subagent へ逃がすか
- worktree / 独立 checkout で並列実装できるか
- 長期タスク state が必要か
- 単一 PR / 独立 PR / Stacked PR のどれにするか
- どの検証をどの context で行うか

利用者に `/clear`、`/compact`、subagent 数、並列数の管理を通常要求しません。

## 推奨: Template Repository から始める

新規 project は [calorie/agentic-repo-template](https://github.com/calorie/agentic-repo-template) から作成するのが最短です。

派生 repository で一度だけ:

```bash
./scripts/setup-agentic.sh
```

その後、使用する runtime を起動します。

```bash
claude
# または
codex
```

setup script は、インストール済みの runtime に対して中央 Marketplace / Plugin を設定し、GitHub CLI があれば `gh stack` も準備します。

## Claude Code に直接インストール

```bash
claude plugin marketplace add calorie/agentic-engineering
claude plugin install agentic-engineering@agentic-engineering
```

特定 repository の project scope に入れる場合:

```bash
claude plugin install agentic-engineering@agentic-engineering --scope project
```

既存 session へ即時反映されない場合は `/reload-plugins` または新しい session を開始します。

## Codex に直接インストール

Codex CLI では native Marketplace を利用します。

```bash
codex plugin marketplace add calorie/agentic-engineering \
  --sparse .agents/plugins \
  --sparse plugins/agentic-engineering

codex plugin add agentic-engineering@agentic-engineering
```

インストール後は **新しい Codex session** を開始してください。

Codex の unmanaged plugin hooks は初回実行前にレビュー / trust が必要です。表示された確認をレビューするか、Codex 内の `/hooks` で状態を確認してください。

### Codex IDE extension

Codex IDE extension は現時点では Plugin をサポートしていません。

その場合でも project の `AGENTS.md` は有効なので、context discipline、parallel-write isolation、PR topology、dependency policy などの共通契約は適用されます。Plugin の hooks / bundled Skills による完全な自動化を使う場合は Codex CLI または Plugin 対応環境を利用してください。

## 3層構造

```text
portable policy / assets
plugins/agentic-engineering/
├── plugin.json                  # Agent Plugins 1.0
├── skills/                      # Claude / Codex 共通
├── scripts/                     # 共通 hook implementation
├── hooks/
│   ├── hooks.json               # Claude Code adapter
│   └── hooks.codex.json         # Codex adapter
├── agents/                      # Claude Code custom agents
├── .claude-plugin/plugin.json   # Claude compatibility
└── .codex-plugin/plugin.json    # Codex compatibility fallback

marketplaces
├── .claude-plugin/marketplace.json
└── .agents/plugins/marketplace.json

project template
├── AGENTS.md                    # runtime 共通 policy
├── CLAUDE.md                    # Claude adapter
├── .claude/settings.json
├── .codex/config.toml           # Codex adapter
├── .agentic/PROJECT.md
└── .agent/tasks/
```

共通 Skill と state protocol を1つに保ち、Claude/Codex 固有部分だけ adapter として分離します。

## Runtime adapter

### Claude Code

- `CLAUDE.md` + Plugin Skills / Agents / Hooks
- investigator / task-planner / reviewer / verifier
- worktree-isolated worker
- 利用可能な場合は大規模 fan-out に runtime-native orchestration を使用

### Codex

- `AGENTS.md` を project guidance として自動読込
- Plugin Skills / Hooks
- 調査は built-in `explorer`
- 実装は `worker` または scoped subagent
- plan / review / verify は fresh subagent
- 複数 writer は Codex-managed Worktree / 独立 checkout がある場合だけ並列化

runtime 固有機能が利用できない場合は、**読み取り並列 + 書き込み逐次**へ安全に縮退します。

## Context management

root session/thread は control-plane として扱います。

```text
User request
    │
    ▼
root control-plane
    │
    ├─ fresh investigation
    ├─ isolated implementation
    ├─ fresh review
    └─ fresh verification
             │
             ▼
      concise result / decision
             │
             ▼
          root context
```

大量の探索結果、ログ、実装試行を root へ戻さず、要求・決定・統合状態だけを残します。

長期タスクは `.agent/tasks/<task>/` を durable state とし、chat history のみを正本にしません。

## Project discovery

project 固有情報は中央 Plugin に hardcode しません。

`.agentic/PROJECT.md` が pending / stale の場合、現在タスクに必要な範囲で次を自動 discovery します。

- package manager / lockfile
- build / test / lint / typecheck
- generated code の source of truth
- CI / task runner
- migration / compatibility 制約
- architecture invariant

Codex では Claude Code 固有の `FileChanged` hook が存在しないため、SessionStart / UserPromptSubmit 時に dependency/toolchain manifest の更新時刻も比較して stale を検出します。

## GitHub Stacked PR

依存関係を持つ複数の review unit に分割する価値がある場合だけ GitHub native `gh stack` を使います。

- 単一の焦点ある差分 → 1 PR
- 独立した差分 → 独立 PR / worktree
- foundation → consumer の依存関係 → Stacked PR

同一 stack の上下 layer を複数 writer で同時に編集することは原則避けます。

## Plugin 開発

validation:

```bash
python3 scripts/validate.py
python3 -m py_compile plugins/agentic-engineering/scripts/*.py
```

Claude Code でローカル版を直接試す:

```bash
claude --plugin-dir ./plugins/agentic-engineering
```

Codex では repository 自体を Marketplace として追加して検証します。

```bash
codex plugin marketplace add ./
codex plugin add agentic-engineering@agentic-engineering
```

## Versioning

Claude / Codex / portable manifest は同一 Plugin version に揃えます。

現在: **0.3.0**

変更時は少なくとも次を同時に確認します。

- `.claude-plugin/marketplace.json`
- `plugins/agentic-engineering/.claude-plugin/plugin.json`
- `plugins/agentic-engineering/plugin.json`
- `plugins/agentic-engineering/.codex-plugin/plugin.json`
- `CHANGELOG.md`

## Dependency policy

- Plugin runtime は Python standard library のみを利用します。
- GitHub Actions は最新安定版を full commit SHA で pin し、Dependabot で追従します。
- project dependency は project constraint と互換な最新 stable を選び、lockfile を更新します。
- pre-release は明示的な理由なしに採用しません。

## Security

Plugin は hooks や tool execution を含みます。導入前に source をレビューし、信頼できる Marketplace からインストールしてください。Codex は unmanaged hooks に対して trust review を要求します。
