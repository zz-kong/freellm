#!/bin/bash
# update-settings.sh - Wrapper for update-settings.py
#
# Kept as a shim so README/CI examples using `bash scripts/update-settings.sh`
# keep working. All logic lives in update-settings.py (the single canonical
# schema writer - the old bash copy wrote an incompatible format).
#
# Usage:
#   bash scripts/update-settings.sh [--settings <path>]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/update-settings.py" "$@"
