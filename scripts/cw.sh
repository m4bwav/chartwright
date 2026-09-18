#!/bin/sh
# macOS/Linux launcher: scripts/cw.sh <command> [args]
d=$(cd "$(dirname "$0")" && pwd)
if command -v python3 >/dev/null 2>&1; then py=python3; else py=python; fi
exec "$py" "$d/cw.py" "$@"
