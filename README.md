# agentic-engineering

Claude Code **ultracode** と Codex **Ultra** の native proactive multi-agent orchestration を活かしながら、project constraints、durable engineering state、verification、Git/PR topology を runtime 横断で統一する Agent Plugin / Marketplace です。

- Marketplace: https://github.com/calorie/agentic-engineering
- Project Template: https://github.com/calorie/agentic-repo-template
- Current version: **0.4.0**

## 0.4 architecture

0.4 では Agentic Engineering 自身が execution engine になることをやめました。

```text
Engineering objective
       │
       ▼
agentic-engineering
  project facts / constraints
  durable engineering state
  verification requirements
  Git / PR topology
       │
       ├───────────────┐
       ▼               ▼
Claude Code          Codex
ultracode            Ultra
Dynamic Workflows    proactive multi-agent
       │               │
       └──── native execution topology ────┘
```

**Execution topology** は runtime native orchestration が決めます。

- agent 数
- task decomposition
- fan-out
- staged execution
- runtime verification passes
- transient workflow state

**Engineering policy** は Agentic Engineering が決めます。

- project-specific constraints
- safe parallel-write boundaries
- durable cross-session state
- dependency/version policy
- required verification evidence
- single PR / independent PR / Stacked PR

## Claude Code

この project は ultracode を前提とします。

Template は `.claude/settings.json` で ultracode を要求し、setup/doctor は current CLI が `--effort ultracode` を受け付けることを確認します。

ultracode では xhigh reasoning に加え、substantive task について Claude が Dynamic Workflow を使うか自動判断します。Plugin は investigator / planner / worker / reviewer / verifier を固定で先に割り当てません。

bundled custom agents は fallback specialist です。

直接インストール:

```bash
claude plugin marketplace add calorie/agentic-engineering
claude plugin install agentic-engineering@agentic-engineering
```

明示的に ultracode session を開始する場合:

```bash
claude --effort ultracode
```

## Codex

Template の `.codex/config.toml` は次を要求します。

```toml
model_reasoning_effort = "ultra"

[agents]
enabled = true
```

Codex Ultra は maximum reasoning に加えて automatic task delegation を有効にするため、Claude ultracode と同様に runtime 自身へ execution topology を任せます。

直接インストール:

```bash
codex plugin marketplace add calorie/agentic-engineering \
  --sparse .agents/plugins \
  --sparse plugins/agentic-engineering

codex plugin add agentic-engineering@agentic-engineering
```

Codex IDE extension は Plugin 非対応です。その surface では `AGENTS.md` が fallback policy になります。完全な Plugin / Hooks / Skills を使う場合は Codex CLI または対応する Codex surface を使ってください。

## Template から使う

新規 repository:

```bash
./scripts/setup-agentic.sh
```

その後は通常どおり:

```bash
claude
# or
codex
```

ユーザーは通常 engineering objective だけを入力します。

```text
ユーザー検索機能を追加して。名前とメールアドレスで検索できるようにする。
```

agent 数、parallelism、worktree allocation、context cleanup、reviewer creation、PR topology を毎回指定する必要はありません。

## Parallel write guardrail

Native runtime に大半を任せますが、次は共通制約です。

- same checkout に複数 writer を同時に置かない
- parallel write は isolated worktree / checkout + disjoint ownership がある場合だけ
- DB schema / ordered migration / unstable shared interface は synchronization boundary
- dependent Stacked PR layers は dependency order を維持
- unrelated user changes を revert しない

## Durable state

Runtime-native workflow state と engineering state を分離します。

Runtime に任せる:

- Claude Dynamic Workflow agent graph / checkpoints
- Codex Ultra subagent execution / thread state
- transient logs / scratch queue

Repository に残す:

```text
.agentic/PROJECT.md
.agent/tasks/<task>/
├── SPEC.md
├── STATE.md
└── DECISIONS.md
```

`COMPACT.md` / `RUNTIME.md` は fallback diagnostics です。runtime が既に保持している transient state を重複保存しません。

## Review topology

複数 agent が動いたかどうかと PR 分割は独立です。

- one focused reviewable change -> one PR
- independent reviewable changes -> independent PRs
- dependent but separately reviewable changes -> GitHub Stacked PR

## Dependency policy

- latest stable compatible dependency
- lockfile update when supported
- GitHub Actions latest stable release pinned by full commit SHA
- Dependabot for continuing updates
- pre-release only with an explicit reason

## Plugin structure

```text
agentic-engineering/
├── .claude-plugin/marketplace.json
├── .agents/plugins/marketplace.json
└── plugins/agentic-engineering/
    ├── plugin.json
    ├── .claude-plugin/plugin.json
    ├── .codex-plugin/plugin.json
    ├── skills/
    ├── agents/                  # Claude fallback specialists
    ├── hooks/
    └── scripts/
```

## Validation

```bash
python3 scripts/validate.py
python3 -m py_compile plugins/agentic-engineering/scripts/*.py
```

## Versioning

Claude Marketplace、Claude manifest、portable manifest、Codex manifest の version を同時に更新します。

## Security

Plugin hooks はローカルコマンドを実行できます。信頼できる Marketplace のみ利用してください。Codex の unmanaged hooks は初回に trust review が必要です。
