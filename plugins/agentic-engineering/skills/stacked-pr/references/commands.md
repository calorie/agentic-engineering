# gh stack コマンド早見表

| 目的 | コマンド |
|---|---|
| stack 開始 | `gh stack init <branch>` |
| 上位 layer 追加 | `gh stack add <branch>` |
| stack 表示 | `gh stack view` |
| layer 移動 | `gh stack up` / `gh stack down` / `gh stack top` / `gh stack bottom` |
| 特定 layer | `gh stack checkout <branch>` |
| PR 作成・更新 | `gh stack submit` |
| 全体同期 | `gh stack sync` |
| merged branch 整理付き同期 | `gh stack sync --prune` |
| cascade rebase | `gh stack rebase` |
| 現在位置より上だけ | `gh stack rebase --upstack` |
| push | `gh stack push` |
| 構造変更 | `gh stack modify` |
