---
name: stacked-pr
description: Use GitHub native stacked pull requests when changes are dependent but independently reviewable. Do not stack independent work or a single focused change.
version: 0.5.2
---

# GitHub Stacked Pull Requests

Use a stack only when:

- each layer has a clear reviewable responsibility;
- an upper layer depends on a lower layer;
- each layer has a meaningful verification story.

Do not use a stack for independent work or a single focused change.

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
