# 組織向け中央配布

## 推奨

中央 repository を private/internal の `agentic-engineering` として管理し、Claude の Organization settings > Plugins から GitHub sync します。

1. Marketplace repository を接続する。
2. `agentic-engineering` plugin を **Required** にする（強制したくない場合は Installed by default）。
3. 自動同期を有効にする。
4. Plugin の変更は PR + CI + version bump を通して default branch へ merge する。
5. Template Repository は generic な project overlay だけ保持する。

この構成では、各 project repo に Skill / Agent / Hook のコピーが不要です。中央 Plugin の更新が distribution point になります。

## 安定運用

- Plugin slug は変更しない。
- 破壊的な policy 変更は major/minor version と CHANGELOG で明示する。
- hook は短時間・fail-open を基本とする。
- project-specific な build/test/architecture 情報を中央 Plugin に入れない。
- central policy と project overlay の責務を混ぜない。
