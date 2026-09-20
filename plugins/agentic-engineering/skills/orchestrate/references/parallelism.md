# Native-first parallelism

## Principle

Do not optimize agent count. Optimize **correct merged throughput**.

Claude Code ultracode/Dynamic Workflows and Codex Ultra own task decomposition, fan-out, staging, and agent count. Agentic Engineering supplies only the boundaries the runtime must not violate.

If Superpowers is installed, its methodology can refine task execution, but Superpowers execution-topology skills must not become a second scheduler under an already active native workflow.

## Hard boundaries

| Situation | Constraint |
|---|---|
| Independent read-only investigation | Native runtime may parallelize freely |
| Independent implementation in isolated worktrees/checkouts | Native runtime may parallelize |
| Same checkout with multiple writers | Do not parallelize writes |
| Same file or generated source | Serialize writes |
| Shared DB schema / ordered migration | Serialize mutation order |
| Producer/consumer with unstable interface | Stabilize contract before parallel writes |
| Dependent Stacked PR layers | Preserve dependency order |
| Independent review / adversarial verification | Native runtime may parallelize |

## Runtime mapping

### Claude Code ultracode

Let Dynamic Workflows generate the harness. Do not replace it with a fixed set of Plugin subagents or a nested Superpowers scheduler.

### Codex Ultra

Let proactive multi-agent delegation choose subagents. Do not require explicit user delegation and do not recreate Claude-specific or Superpowers-specific worker graphs.

## Superpowers mapping

Methodology-oriented Superpowers skills may run inside native parallel execution.

Examples:

- TDD loops may run independently in isolated worktrees/checkouts.
- Systematic debugging may use parallel read-only evidence gathering.
- Verification-before-completion may gate completion without owning the worker graph.

Do not nest:

- `subagent-driven-development`;
- `dispatching-parallel-agents`;
- `executing-plans`;

under an already active Dynamic Workflow or Codex Ultra delegation graph.

## Resource contention

Source isolation does not imply CPU, memory, database, emulator, port, or CI isolation.

If parallel workers contend on a scarce resource, reduce concurrency for the scarce operation rather than disabling useful parallel exploration.
