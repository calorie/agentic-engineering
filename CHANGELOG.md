# Changelog

## 0.4.0

- Claude Code は ultracode / Dynamic Workflows を primary execution engine とする native-first architecture に変更
- Codex は project-level `model_reasoning_effort = "ultra"` を前提とし、proactive multi-agent delegation を primary execution engine とする方針へ変更
- Plugin が固定 agent graph / agent count を先に決める挙動を廃止
- bundled Claude custom agents を fallback specialist に変更
- execution topology と Git/review topology を明確に分離
- long-task state を durable engineering state に限定し、runtime-native workflow state の重複保存を抑制
- root context には要求・決定・integration・verification evidence だけを残す方針へ簡素化
- Claude/Codex の native orchestration が使えない場合のみ safe fallback を利用

## 0.3.0

- Codex CLI / ChatGPT desktop Codex 向けの native Marketplace を追加
- portable Agent Plugins 1.0 manifest を追加
- Codex compatibility manifest と Codex 対応 lifecycle hooks を追加
- orchestrate Skill を Claude Code / Codex の runtime adapter 方式へ変更
- Codex built-in explorer / worker と fresh subagent を使う安全な縮退戦略を追加
- project profile の stale 判定を manifest 更新時刻からも検出するよう改善
- Claude/Codex の manifest・version・hook 互換性を CI validation 対象に追加

## 0.2.0

- root session を control-plane 化し、manual `/clear` / `/compact` を通常運用から排除する context firewall を追加
- project-bootstrap と manifest freshness tracking を追加
- auto compaction summary / session runtime snapshot の durable local state を追加
- GitHub Actions を checkout v7.0.1 / setup-python v7.0.0 の immutable SHA pin へ更新
- Dependabot による GitHub Actions 更新を追加
- `gh-stack` setup を latest stable への強制更新に変更

## 0.1.0

- 初期版
- 自動オーケストレーション Skill
- investigator / reviewer / verifier / worktree-worker / task-planner agents
- 長期タスク状態管理
- GitHub native Stacked PR workflow
- SessionStart / UserPromptSubmit / PreCompact hooks
