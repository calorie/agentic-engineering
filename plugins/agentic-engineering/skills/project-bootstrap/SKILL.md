---
name: project-bootstrap
description: Use this skill automatically before the first substantive development task when .agentic/PROJECT.md is pending, or when .agentic/PROFILE_STALE exists. It discovers only durable project-specific build, test, dependency, generated-code, and architecture facts so future tasks start with sufficient context without bloating CLAUDE.md.
version: 0.4.1
---

# Project bootstrap

Do not require manual initialization from the user. Run one lightweight discovery pass immediately before the first substantive engineering task. If the stale marker exists, re-check only the relevant changed facts.

## Inspect

- package and lock manifests such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, Gradle, Bundler, and Composer files;
- task runners, Makefiles, and CI workflows;
- actual build, test, lint, and typecheck commands documented in README or development docs;
- generated-code sources of truth;
- architecture invariants and compatibility constraints that repeatedly affect implementation.

## Output rules

- Write only facts that are confirmed, durable, project-specific, and likely to matter repeatedly into `.agentic/PROJECT.md`.
- Do not write file inventories, generic advice, long explanations, or state relevant only to the current task.
- Replace `<!-- agentic-profile: pending -->` with `<!-- agentic-profile: ready -->`.
- Remove `.agentic/PROFILE_STALE` when the refresh is complete.
- Never guess unknown fields.

## Dependency-update baseline

If `.github/dependabot.yml` exists, add or maintain update entries only when the detected package ecosystem and project directory structure are clear. Do not guess monorepo directories.

When a task adds a dependency, check the package manager or official registry, select the latest stable version compatible with project constraints, and update the lockfile.
