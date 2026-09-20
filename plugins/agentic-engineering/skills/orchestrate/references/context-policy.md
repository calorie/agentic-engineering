# Context policy

- root/main conversation は control-plane。残すのは要求、制約、決定、統合判断、最終結果。
- substantive な新規タスクは fresh execution context を優先し、無関係な前タスクの実装履歴を再利用しない。
- repository-wide discovery は investigator / Dynamic Workflow に委譲する。
- 大量 fan-out は Dynamic Workflow を使い、中間結果を main conversation に戻さない。
- test/build の長い stdout は結論と失敗箇所だけ残す。
- project 固有の恒久知識は `.agentic/PROJECT.md` へ短く記録する。
- 長期タスクの進捗は `.agent/tasks/<task>/STATE.md` を正本にする。
- chat transcript を durable state とみなさない。
- auto-compaction は通常運用の safety net。ユーザーへ `/clear` / `/compact` を要求しない。
- compaction 後や新セッションでは STATE / SPEC / 自動保存された COMPACT / RUNTIME から再開し、会話を完全再構築しようとしない。
