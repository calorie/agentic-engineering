---
name: stacked-pr
description: Use GitHub native stacked pull requests when changes are dependent but independently reviewable. Do not stack independent work or a single focused change.
version: 0.5.3
---

# GitHub Stacked Pull Requests

Review topology must be selected from the full objective before broad implementation.

Use a stack when:

- each layer has a clear reviewable responsibility;
- an upper layer depends on a lower layer;
- each layer has a meaningful verification story.

Do not use a stack for independent work or a single focused change.

When stack conditions are met:

1. define the layer dependency order;
2. initialize the lowest layer from the default branch;
3. implement and locally verify that layer until its contract is stable;
4. add the next dependent layer on top without waiting for the lower PR to merge;
5. continue until the planned review DAG is represented by the stack.

Do not turn a planned dependent sequence into a series of PRs all based on the default branch merely because the layers are implemented sequentially.

## Commands

```bash
gh stack init <branch>
gh stack add <branch>
gh stack submit
gh stack rebase --upstack
gh stack push
gh stack sync
```

Keep every stack branch in the same repository.

Fix lower-layer problems in the lower layer, then rebase the upstack. Do not implement dependent upper/lower layers concurrently merely to increase agent utilization.

Install or refresh the extension only when environment changes are permitted:

```bash
gh extension install github/gh-stack --force
```

## Merge boundary

Prepare, submit, rebase, and update the stack autonomously. Do not merge the stack or any pull request into the default branch until the user gives explicit approval immediately before merge.
