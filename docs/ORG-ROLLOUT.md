# 組織向け中央配布

agentic-engineering 0.4 は **native proactive orchestration + shared engineering policy** を組織へ配布する。

## Execution baseline

Claude Code:
- ultracode / Dynamic Workflows を primary execution engine とする。
- account/model/admin policy が workflows または xhigh を制限する場合、その制限が優先される。

Codex:
- project config で `model_reasoning_effort = "ultra"` を要求する。
- Ultra 対応 account/model では proactive task delegation を primary execution engine とする。

Agentic Engineering が agent count や固定 worker graph を組織標準として hardcode しない。

## Central policy

中央 Plugin に置く:

- project discovery policy
- parallel-write safety boundaries
- durable engineering state protocol
- verification requirements
- dependency/version policy
- GitHub review topology / Stacked PR policy
- runtime adapter / safe fallback

各 project に置く:

- `AGENTS.md`
- `CLAUDE.md` / `.claude/settings.json`
- `.codex/config.toml`
- `.agentic/PROJECT.md`
- project-specific architecture / test / migration facts

## Distribution

Claude Code organization management では Marketplace を接続し、必要に応じて Plugin を Required / Installed by default として配布する。

Codex / ChatGPT workspace では対応する Plugin Marketplace / directory policy で配布する。Codex IDE extension は Plugin 非対応のため `AGENTS.md` が fallback policy になる。

## Stability

- Plugin slug を維持する。
- portable / Claude / Codex manifests の version を揃える。
- policy changes は PR + CI + CHANGELOG + version bump を通す。
- generic policy を project ごとに複製しない。
- runtime-native capability が進化したら custom orchestration を増やすのではなく adapter を薄くする。
- project-specific facts を中央 Plugin に hardcode しない。
