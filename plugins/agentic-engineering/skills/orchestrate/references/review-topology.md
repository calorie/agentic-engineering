# Review topology

## 単一 PR

1つの目的、1つの理解可能な diff、1つの verification story で閉じる場合。

## 独立 PR

互いを base にする必要がなく、どちらから先に merge しても意味が保たれる場合。別 worktree / worker に向く。

## Stacked PR

下位変更を上位変更が必要とし、かつ各層を独立にレビューする価値がある場合。

典型:
1. schema / interface
2. backend implementation
3. consumer / UI
4. integration coverage

stack 内の dependent layer を同時編集して速度を稼ごうとしない。下位変更は上位へ cascade するため、stack 内は短い sequential loop を保つ。
