# gh stack command reference

| Purpose | Command |
|---|---|
| Start a stack | `gh stack init <branch>` |
| Add an upper layer | `gh stack add <branch>` |
| View the stack | `gh stack view` |
| Move between layers | `gh stack up` / `gh stack down` / `gh stack top` / `gh stack bottom` |
| Check out a specific layer | `gh stack checkout <branch>` |
| Create/update pull requests | `gh stack submit` |
| Synchronize the stack | `gh stack sync` |
| Synchronize and prune merged branches | `gh stack sync --prune` |
| Cascade rebase | `gh stack rebase` |
| Rebase only layers above the current one | `gh stack rebase --upstack` |
| Push | `gh stack push` |
| Modify stack structure | `gh stack modify` |
