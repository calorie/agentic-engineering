---
name: stacked-pr
description: This skill should be used when a change contains multiple dependent but independently reviewable units, when the user mentions stacked PRs, or when orchestration determines that a foundation/interface change should land below one or more consumer changes. It uses GitHub native stacked pull requests through the gh stack extension when available.
version: 0.4.1
---

# GitHub Stacked Pull Requests

Split dependent changes into small, reviewable layers.

## When to use a stack

Use stacked pull requests when:

- each layer has a clear responsibility;
- an upper layer depends on a lower layer;
- each layer is valuable to review independently.

Do not use a stack when:

- the tasks are independent; use separate pull requests instead;
- the change is small and focused; use one pull request;
- splitting the change creates broken intermediate states with no meaningful verification story.

## Preconditions

1. Confirm the repository has a GitHub remote and that `gh` is authenticated.
2. Confirm `gh stack --help` is available.
3. If the extension is missing and environment changes are permitted, install or update the latest stable release with `gh extension install github/gh-stack --force`.
4. Keep every branch in the stack in the same repository. Do not create cross-fork stacks.

## Create a stack

Start the lowest layer from the trunk branch:

```bash
gh stack init <branch>
```

After implementing, verifying, and committing that layer, add the next dependent layer:

```bash
gh stack add <branch>
```

Add only the layers that are actually useful for review. Do not deepen the stack merely to create more review units.

## Submit

When remote pull-request creation is allowed by the task intent and repository policy:

```bash
gh stack submit
```

If permission is unclear, complete the local stack and report that it is ready to submit.

## Modify a lower layer

Return to the correct layer and fix it there instead of adding a workaround above it:

```bash
gh stack checkout <branch>
# edit + commit
gh stack rebase --upstack
gh stack push
```

## Synchronize

Normal synchronization:

```bash
gh stack sync
```

Also prune merged branches when appropriate:

```bash
gh stack sync --prune
```

For conflicts, use `gh stack rebase` interactively, then publish with `gh stack push`.

## Relationship to agent parallelism

Do not normally assign upper and lower layers of the same stack to different writers at the same time. Lower-layer changes cascade upward. Keep dependent work sequential within a stack; parallelize only across genuinely independent stacks.

## Reference

- `references/commands.md` — command reference
