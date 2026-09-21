#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
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

for label, obj in [
    ("Claude marketplace", claude_market),
    ("Codex marketplace", codex_market),
    ("Claude manifest", claude_manifest),
    ("Codex manifest", codex_manifest),
    ("portable manifest", portable_manifest),
]:
    if obj.get("name") != "agentic-engineering":
        errors.append(f"{label} name must be agentic-engineering")

versions = {
    "Claude marketplace": claude_market.get("plugins", [{}])[0].get("version"),
    "Claude manifest": claude_manifest.get("version"),
    "Codex manifest": codex_manifest.get("version"),
    "portable manifest": portable_manifest.get("version"),
}
if set(versions.values()) != {"0.5.1"}:
    errors.append("version mismatch: " + ", ".join(f"{k}={v}" for k, v in versions.items()))

if portable_manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
    errors.append("portable plugin must use Agent Plugins 1.0 schema")

openai_ext = portable_manifest.get("extensions", {}).get("com.openai", {})
if "hooks" in openai_ext:
    errors.append("0.5.0 must not declare Plugin hooks")

codex_plugins = codex_market.get("plugins", [])
if not codex_plugins or codex_plugins[0].get("source", {}).get("path") != "./plugins/agentic-engineering":
    errors.append("Codex marketplace local plugin path is invalid")

required_skills = {
    PLUGIN / "skills" / "orchestrate" / "SKILL.md",
    PLUGIN / "skills" / "stacked-pr" / "SKILL.md",
}
for skill in required_skills:
    if not skill.exists():
        errors.append(f"missing required skill: {skill}")

for legacy in ["agents", "hooks", "scripts"]:
    if (PLUGIN / legacy).exists():
        errors.append(f"legacy runtime directory must be removed: {PLUGIN / legacy}")

non_english_pattern = re.compile(r"[\u3040-\u30ff\u3400-\u9fff\uff66-\uff9f]")
try:
    tracked = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-z"]).split(b"\0")
except Exception as exc:
    errors.append(f"could not enumerate tracked files: {exc}")
    tracked = []

for raw_path in tracked:
    if not raw_path:
        continue
    relative = raw_path.decode("utf-8")
    path = ROOT / relative
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    match = non_english_pattern.search(text)
    if match:
        line = text.count("\n", 0, match.start()) + 1
        errors.append(f"non-English text detected: {relative}:{line}")

if errors:
    print("FAIL")
    for err in errors:
        print("-", err)
    sys.exit(1)

print("PASS: minimal 0.5.0 plugin structure")
