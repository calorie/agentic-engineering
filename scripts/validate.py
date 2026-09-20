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

market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
manifest = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
load_json(PLUGIN / "hooks" / "hooks.json")

if market.get("name") != "agentic-engineering":
    errors.append("marketplace name must be agentic-engineering")
if manifest.get("name") != "agentic-engineering":
    errors.append("plugin name must be agentic-engineering")

mv = market.get("plugins", [{}])[0].get("version")
pv = manifest.get("version")
if mv != pv:
    errors.append(f"version mismatch: marketplace={mv} plugin={pv}")

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
        errors.append(f"invalid/missing agent name: {agent}")

if errors:
    print("FAIL")
    for err in errors:
        print("-", err)
    sys.exit(1)
print("PASS: agentic-engineering plugin structure")
