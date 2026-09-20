#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "agentic-engineering"
errors: list[str] = []


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"JSON error {path}: {exc}")
        return {}


claude_market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
codex_market = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
claude_manifest = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
codex_manifest = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
portable_manifest = load_json(PLUGIN / "plugin.json")
claude_hooks = load_json(PLUGIN / "hooks" / "hooks.json")
codex_hooks = load_json(PLUGIN / "hooks" / "hooks.codex.json")

for label, obj in [
    ("Claude marketplace", claude_market),
    ("Codex marketplace", codex_market),
    ("Claude manifest", claude_manifest),
    ("Codex manifest", codex_manifest),
    ("portable manifest", portable_manifest),
]:
    if obj.get("name") != "agentic-engineering":
        errors.append(f"{label} name must be agentic-engineering")

claude_market_version = claude_market.get("plugins", [{}])[0].get("version")
versions = {
    "Claude marketplace": claude_market_version,
    "Claude manifest": claude_manifest.get("version"),
    "Codex manifest": codex_manifest.get("version"),
    "portable manifest": portable_manifest.get("version"),
}
if len({v for v in versions.values() if v is not None}) != 1:
    errors.append("version mismatch: " + ", ".join(f"{k}={v}" for k, v in versions.items()))

if portable_manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
    errors.append("portable plugin must use Agent Plugins 1.0 schema")

openai_ext = portable_manifest.get("extensions", {}).get("com.openai", {})
portable_hooks = openai_ext.get("hooks")
if not isinstance(portable_hooks, list) or portable_hooks != ["./hooks/hooks.codex.json"]:
    errors.append("portable OpenAI hooks must be a list pointing to ./hooks/hooks.codex.json")

codex_plugins = codex_market.get("plugins", [])
if not codex_plugins:
    errors.append("Codex marketplace must contain agentic-engineering plugin")
else:
    source = codex_plugins[0].get("source", {})
    if source.get("path") != "./plugins/agentic-engineering":
        errors.append("Codex marketplace local plugin path is invalid")

codex_events = set(codex_hooks.get("hooks", {}))
unsupported_codex_events = codex_events - {
    "PreToolUse", "PermissionRequest", "PostToolUse", "PreCompact", "PostCompact",
    "UserPromptSubmit", "SubagentStop", "Stop", "Interrupt", "SessionStart",
    "SubagentStart", "SessionEnd",
}
if unsupported_codex_events:
    errors.append(f"unsupported Codex hook events: {sorted(unsupported_codex_events)}")

if "FileChanged" not in claude_hooks.get("hooks", {}):
    errors.append("Claude hook set should retain FileChanged profile invalidation")

for skill in (PLUGIN / "skills").glob("*/SKILL.md"):
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"missing frontmatter: {skill}")
    if "\nname:" not in text or "\ndescription:" not in text:
        errors.append(f"missing name/description: {skill}")

for agent in (PLUGIN / "agents").glob("*.md"):
    text = agent.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"missing frontmatter: {agent}")
    match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", text, re.M)
    if not match:
        errors.append(f"invalid/missing Claude agent name: {agent}")

if errors:
    print("FAIL")
    for err in errors:
        print("-", err)
    sys.exit(1)

print("PASS: agentic-engineering Claude/Codex plugin structure")
