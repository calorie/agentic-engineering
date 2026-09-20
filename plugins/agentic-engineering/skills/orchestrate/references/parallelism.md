# Native-first parallelism

## Principle

Do not optimize agent count. Optimize **correct merged throughput**.

Claude Code ultracode/Dynamic Workflows and Codex Ultra own task decomposition, fan-out, staging, and agent count. Agentic Engineering supplies only the boundaries the runtime must not violate.

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

Let Dynamic Workflows generate the harness. Do not replace it with a fixed set of Plugin subagents.

### Codex Ultra

Let proactive multi-agent delegation choose subagents. Do not require explicit user delegation and do not recreate Claude-specific workflow structure.

## Resource contention

Source isolation does not imply CPU, memory, database, emulator, port, or CI isolation.

If parallel workers contend on a scarce resource, reduce concurrency for the scarce operation rather than disabling useful parallel exploration.
