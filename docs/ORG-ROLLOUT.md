# 組織向け中央配布

## 推奨構成

公開 Marketplace / Plugin は次を利用できます。

- https://github.com/calorie/agentic-engineering

組織内でそのまま利用する場合は、Claude の Organization settings > Plugins から Marketplace を接続し、`agentic-engineering` を **Required** または **Installed by default** にします。

1. Marketplace repository `calorie/agentic-engineering` を接続する。
2. `agentic-engineering` Plugin を Required にする。強制したくない場合は Installed by default にする。
3. 自動同期を有効にする。
4. project repository には generic Skill / Agent / Hook を複製しない。
5. project 固有の build/test/architecture 情報だけを project 側に保持する。

この構成では中央 Plugin の更新が distribution point になります。

## Fork / private marketplace を使う場合

組織固有の policy を中央 Plugin 自体へ組み込みたい場合は、この repository を fork するか private/internal Marketplace として管理できます。

その場合も Plugin slug と Marketplace 名は可能な限り維持し、project 側の `.claude/settings.json` だけ配布先に合わせて変更してください。

Template Repository では次の helper を利用できます。

```bash
./scripts/configure-central-plugin.sh <github-owner> [plugin-repo]
```

## 安定運用

- Plugin slug は変更しない。
- policy 変更は version bump と CHANGELOG で追跡する。
- hook は短時間・fail-open を基本とする。
- project-specific な build/test/architecture 情報を中央 Plugin に入れない。
- central policy と project overlay の責務を混ぜない。
- GitHub Actions と外部依存は project constraint と互換な最新 stable を追従する。
