#!/usr/bin/env bash
set -euo pipefail
owner="${1:-}"
repo="${2:-agentic-engineering}"
if [[ -z "$owner" ]]; then
  echo "Usage: $0 <github-owner> [repo-name]" >&2
  exit 2
fi
root="$(cd "$(dirname "$0")/.." && pwd)"
python3 - "$root/plugins/agentic-engineering/.claude-plugin/plugin.json" "$owner" "$repo" <<'PY'
import json, sys
from pathlib import Path
p=Path(sys.argv[1]); owner=sys.argv[2]; repo=sys.argv[3]
d=json.loads(p.read_text())
d['homepage']=f'https://github.com/{owner}/{repo}'
p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n')
PY
printf 'Configured plugin homepage: https://github.com/%s/%s\n' "$owner" "$repo"
