---
name: orchestrate
description: Use this skill for substantive software-engineering requests. It keeps engineering policy runtime-neutral while delegating execution topology to the runtime's native proactive multi-agent engine: Claude Code ultracode/Dynamic Workflows or Codex Ultra. It owns project constraints, durable engineering state, verification requirements, Git/PR topology, and compatibility boundaries for methodology plugins such as Superpowers rather than prescribing agent counts or fixed worker graphs.
version: 0.4.2
---

# Native-first engineering orchestration

The runtime owns **how work is executed**. Agentic Engineering owns **what constraints and completion standards the work must satisfy**.

Do not build a static agent graph when the runtime already provides proactive orchestration.

## 0. Runtime contract

### Claude Code

Assume **ultracode** is enabled.

- Dynamic Workflows are the primary execution engine for substantive tasks.
- Let Claude decide whether a task warrants a workflow, how many agents to use, whether work should happen in stages or in parallel, and which verification passes are useful.
- Do not pre-allocate investigator / planner / worker / reviewer / verifier agents before Claude has made its native workflow decision.
- Custom agents bundled by this Plugin are fallback/specialist tools only when Dynamic Workflows are unavailable or a narrow deterministic role is materially useful.
- Do not reproduce workflow progress in the root conversation. Keep only requirements, engineering decisions, integration state, and final results.

### Codex

Assume project configuration requests **Ultra** reasoning.

- Codex Ultra's proactive multi-agent behavior is the primary execution engine for substantive tasks.
- Let Codex decide when to delegate, how many subagents to use, and which built-in or scoped roles to employ.
- Do not require the user to ask for subagents.
- Do not statically mirror Claude's Dynamic Workflow graph. Use Codex-native delegation.
- If Ultra is unavailable for the current account/model, explicitly request delegation for independent work when beneficial and otherwise fall back safely.

### Safe fallback

If native proactive orchestration is unavailable:

- parallelize read-only investigation when useful;
- allow parallel writes only with isolated checkout/worktree and disjoint ownership;
- otherwise keep writes sequential;
- use bundled custom agents only as a fallback.

## 1. Superpowers compatibility

If Superpowers skills are installed, treat Superpowers as a **methodology provider**, not as a second scheduler.

### Prefer Superpowers methodology skills

Use relevant methodology skills inside the native runtime's execution topology when they add value:

- `test-driven-development`;
- `systematic-debugging`;
- `verification-before-completion`;
- `receiving-code-review`;
- `diagnosing-superpowers`.

### Use with deduplication

Use these only when they add information or discipline not already provided by the native workflow:

- `brainstorming` for material product/design ambiguity;
- `writing-plans` for outcomes, dependencies, interfaces, and verification—not a fixed worker graph;
- `requesting-code-review` only when equivalent independent review evidence does not already exist;
- `using-git-worktrees` for workspace safety while preferring an existing runtime-managed worktree;
- `finishing-a-development-branch` for verification/environment checks while preserving Agentic Engineering's PR-topology decision.

Do not manufacture human approval checkpoints for a clear request solely because a methodology skill normally includes them.

### Do not nest a second scheduler

Under Claude ultracode / Dynamic Workflows or Codex Ultra, do not use the following Superpowers skills to take over execution topology:

- `subagent-driven-development`;
- `dispatching-parallel-agents`;
- `executing-plans`.

Preserve useful principles from those skills—fresh context, isolated work, task-level verification, review gates—but let the native runtime implement them.

Use a Superpowers execution-topology skill directly only when native proactive orchestration is unavailable or the user explicitly requests that specific workflow.

See `references/superpowers-compatibility.md` for the detailed contract.

## 2. Discover project facts, not execution plans

If `.agentic/PROJECT.md` is pending or stale, apply `project-bootstrap` before making assumptions.

Discover only durable project facts needed for correct execution:

- build / test / lint / typecheck commands;
- generated-code sources of truth;
- migration and compatibility constraints;
- architecture invariants;
- package-manager and dependency constraints.

Do **not** persist a fixed worker decomposition. The native runtime should re-plan execution for each task.

## 3. Shared engineering guardrails

Native orchestration may choose any execution topology, subject to these constraints:

- Never allow two writers to concurrently mutate the same checkout.
- Parallel write work requires isolated worktrees/checkouts and genuinely disjoint ownership.
- Shared DB schema, migration ordering, unstable interfaces, or shared generated sources are synchronization boundaries.
- Do not overwrite or revert unrelated user changes.
- Do not declare completion while required verification is failing.
- Keep large logs and intermediate exploration out of the root context.
- Prefer runtime-native progress/resume mechanisms over duplicating transient runtime state.

These are safety/quality constraints, not instructions to maximize or minimize agent count.

## 4. Separate execution topology from review topology

The runtime chooses execution topology.

Agentic Engineering chooses the final Git/review topology:

- one focused reviewable change -> one PR;
- independent reviewable changes -> independent PRs;
- dependent but separately reviewable foundation -> consumer changes -> Stacked PR.

Do not create a stack merely because execution used multiple agents.

For dependent stack layers, preserve dependency order even if the runtime explored them in parallel.

## 5. Durable engineering state

Use `long-task` only when engineering state must survive across sessions, runtimes, PRs, or humans.

Durable state contains:

- stable goal and acceptance criteria;
- externally relevant decisions and rationale;
- completed review units;
- verification status;
- blockers;
- next engineering action.

Do not mirror the runtime's internal agent graph, Superpowers workflow transcript, transient task queue, or workflow scratch state into durable files.

## 6. Verification

Require evidence appropriate to the blast radius, but let the native runtime choose the execution mechanism.

Completion requires:

1. relevant tests/checks were identified;
2. the narrowest useful checks were run;
3. broader checks were run when blast radius warrants them;
4. substantive changes received independent review/verification, either inside the native workflow, through an applicable Superpowers methodology skill, or via a fallback fresh agent;
5. failures were fixed or explicitly reported as blockers.

Do not launch duplicate review/verification merely because the native runtime, Superpowers, and Agentic Engineering can all provide equivalent checks.

## 7. Dependency and automation policy

- New or updated dependencies: latest stable version compatible with project constraints.
- Update lockfiles when the ecosystem supports them.
- GitHub Actions: latest stable release pinned to a full commit SHA, with version comment.
- Do not adopt pre-release versions solely because they are newer.

## 8. User experience

The user should normally provide only the engineering objective.

Do not ask the user to manage:

- agent count;
- parallelism;
- context-window cleanup;
- `/clear` or `/compact`;
- worktree allocation;
- reviewer/verifier creation;
- PR topology.

Escalate to the user only for product ambiguity, authorization, irreversible external action, or an engineering choice whose requirements cannot be inferred safely.

## References

- `references/parallelism.md` - native-first parallelism guardrails
- `references/review-topology.md` - PR / stack selection
- `references/context-policy.md` - runtime vs durable context
- `references/superpowers-compatibility.md` - Superpowers ownership and deduplication rules
