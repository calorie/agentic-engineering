---
name: project-bootstrap
description: Use this skill automatically before the first substantive development task when .agentic/PROJECT.md is pending, or when .agentic/PROFILE_STALE exists. It discovers only durable project-specific build, test, dependency, generated-code, and architecture facts so future tasks start with sufficient context without bloating CLAUDE.md.
version: 0.2.0
---

# プロジェクト自動発見

人間へ初期設定を要求せず、最初の実質的な開発タスクの直前に一度だけ軽量 discovery を行う。stale marker がある場合も同様に差分だけ再確認する。

## 調査対象

- package / lock manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, Gradle, Bundler, Composer 等)
- task runner / Makefile / CI workflows
- README や開発ドキュメントにある実際の build / test / lint / typecheck コマンド
- generated code の source of truth
- 実装で繰り返し必要になる architecture invariant / compatibility constraint

## 出力規則

- `.agentic/PROJECT.md` には **確実に確認でき、将来も繰り返し必要になる事実だけ** を短く書く。
- ファイル一覧、一般論、長い説明、現在タスクだけの状態は書かない。
- `<!-- agentic-profile: pending -->` を `<!-- agentic-profile: ready -->` に更新する。
- `.agentic/PROFILE_STALE` があれば削除する。
- 不明な項目を推測で埋めない。

## 依存更新基盤

`.github/dependabot.yml` がある場合、検出した package ecosystem について project 構造が明確なときだけ適切な update entry を追加・維持する。monorepo の directory を推測しない。
新規依存を追加するタスクでは、package manager / official registry で最新安定版を確認し、project の互換性制約を満たす最新版を選び lockfile を更新する。
