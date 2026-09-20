# Review topology

## Single pull request

Use one pull request when the change has one purpose, one understandable diff, and one verification story.

## Independent pull requests

Use independent pull requests when neither change needs the other as a base and either can merge first without losing meaning. These are good candidates for separate worktrees or workers.

## Stacked pull requests

Use a stack when an upper change depends on a lower change and each layer is still valuable to review independently.

Typical layers:

1. schema / interface
2. backend implementation
3. consumer / UI
4. integration coverage

Do not try to gain speed by concurrently editing dependent layers in the same stack. Lower-layer changes cascade upward, so keep a short sequential loop within a stack.
