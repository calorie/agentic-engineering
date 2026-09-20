# 並列化判断リファレンス

## 目的

同時実行数ではなく、統合済み変更の throughput を最大化する。

## 判定表

| 状況 | 既定 |
|---|---|
| 読み取り中心の独立調査 | 並列 |
| fresh review と verification | 実装後に並列可 |
| 異なるモジュール、interface 確定済み | worktree 並列 |
| 同一ファイル | 逐次 |
| 共有 schema / migration | 逐次 |
| producer-consumer で契約未確定 | 契約確定まで逐次 |
| Stacked PR の依存レイヤー | 逐次 |
| 大量の独立した機械変更 | worktree worker / batch 系を検討 |

CPU・メモリ・I/O を大量消費する build/test を全 worker で同時に走らせる必要はない。リソース飽和が見える場合、worker 数ではなく重い検証の concurrency を下げる。
