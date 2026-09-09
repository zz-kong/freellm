#!/bin/bash
# gather-llm-apis.sh - Discover free LLM APIs via X scan + web search
#
# Replaces the previous version which had a hardcoded JSON blob.
# This version runs the real discovery pipeline:
#   1. Scan x.pcstyle.dev for free-tier announcements
#   2. Extract and verify provider info from posts
#   3. Update data/models.json with real findings
#   4. Update settings.json with verified models
#
# Usage:
#   bash scripts/gather-llm-apis.sh [--force] [--queries queries.txt]

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$BASE_DIR/data"
RAW_DIR="$DATA_DIR/raw"
DOCS_DIR="$BASE_DIR/docs"
MODELS_FILE="$DATA_DIR/models.json"

FORCE=false
QUERIES=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --force)   FORCE=true; shift ;;
        --queries) QUERIES="$2"; shift 2 ;;
        *)         echo "Unknown: $1"; exit 1 ;;
    esac
done

mkdir -p "$RAW_DIR/x" "$DOCS_DIR" "$BASE_DIR/logs"

echo "=== Free LLM API Discovery ==="
echo "Timestamp: $(date -Iseconds)"
echo ""

# Step 1: Run X scan if force or no data
if [ "$FORCE" = true ] || [ ! -f "$DATA_DIR/x-posts.json" ]; then
    echo "Step 1: Scanning X for free LLM API announcements..."
    
    if [ -n "$QUERIES" ]; then
        bash "$SCRIPT_DIR/x-scan.sh" --queries "$QUERIES" --sleep 25 --budget 600
    else
        bash "$SCRIPT_DIR/x-scan.sh" --sleep 25 --budget 600
    fi
    echo ""
else
    echo "Step 1: X data already exists, skipping (use --force to re-scan)"
fi

# Step 2: Extract leads from X posts
echo "Step 2: Extracting provider leads..."
python3 "$SCRIPT_DIR/x-extract.py" 2>/dev/null
echo ""

# Step 3: Build provider database from X findings
echo "Step 3: Building provider database..."
python3 "$SCRIPT_DIR/gather-x-apis.py"
echo ""

# Step 4: Update settings with verified models
echo "Step 4: Updating settings.json..."
python3 "$SCRIPT_DIR/update-settings.py"
echo ""

echo "=== Discovery Complete ==="
echo "  Models:      $MODELS_FILE"
echo "  Documentation: $DOCS_DIR/models.md"
echo "  X findings:  $DOCS_DIR/x-findings.md"
echo "  Settings:    $BASE_DIR/settings.json"

# Summary
if [ -f "$MODELS_FILE" ]; then
    n=$(jq 'length' "$MODELS_FILE" 2>/dev/null || echo 0)
    echo "  Total providers: $n"
fi
