# Changelog

## 0.2.0

- root session を control-plane 化し、manual `/clear` / `/compact` を通常運用から排除する context firewall を追加
- project-bootstrap と manifest freshness tracking を追加
- auto compaction summary / session runtime snapshot の durable local state を追加
- GitHub Actions を checkout v7.0.1 / setup-python v7.0.0 の immutable SHA pin へ更新
- Dependabot による GitHub Actions 更新を追加
- `gh-stack` setup を latest stable への強制更新に変更

## 0.1.0

- 初期版。
- 自動オーケストレーション Skill。
- investigator / reviewer / verifier / worktree-worker / task-planner agents。
- 長期タスク状態管理。
- GitHub native Stacked PR workflow。
- SessionStart / UserPromptSubmit / PreCompact hooks。
