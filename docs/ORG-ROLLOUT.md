# 組織向け中央配布

agentic-engineering は **Claude Code と Codex の両方**へ同じ engineering policy を中央配布することを目的とする。

公開 Marketplace:

- https://github.com/calorie/agentic-engineering

## Claude Code

Anthropic 側の Organization plugin management で Marketplace を接続し、必要に応じて `agentic-engineering` を Required / Installed by default として配布する。

## Codex / ChatGPT

OpenAI workspace の plugin management では、この repository の Codex Marketplace (`.agents/plugins/marketplace.json`) または対応する Marketplace 形式を import / sync する。

管理対象環境では:

1. Marketplace source を許可する。
2. `agentic-engineering` の installation policy を組織方針に合わせる。
3. Plugin に含まれる Skills と Hooks をレビューする。
4. Hooks を trusted managed configuration として配布する場合は、各 developer が同じ source を利用するようにする。
5. project の `AGENTS.md` と中央 Plugin の責務を混ぜない。

Codex IDE extension は現時点で Plugin 非対応なので、IDE では `AGENTS.md` が fallback policy になる。

## 共通原則

中央 Plugin に置く:

- orchestration policy
- Skills
- context / long-task protocol
- review / verification policy
- runtime adapter
- GitHub Stacked PR policy

project に置く:

- `AGENTS.md`
- Claude adapter (`CLAUDE.md`, `.claude/settings.json`)
- Codex adapter (`.codex/config.toml`)
- `.agentic/PROJECT.md`
- project 固有の architecture / test / migration constraints

## Fork / private marketplace

組織固有 policy を Plugin 本体に組み込む場合は repository を fork / private mirror して中央管理できる。

その場合:

- Plugin 名は可能な限り `agentic-engineering` のまま維持する。
- Claude と Codex の Marketplace source を同じ fork に向ける。
- portable / Claude / Codex manifests の version を揃える。
- policy 変更は PR + CI + CHANGELOG + version bump を通す。

## 安定運用

- generic policy を各 project へコピーしない。
- hook は短時間・fail-open を基本とする。
- project 固有情報を中央 Plugin に hardcode しない。
- runtime 固有機能に依存しすぎず、安全な fallback を持つ。
- GitHub Actions と外部依存は project constraint と互換な最新 stable を追従する。
