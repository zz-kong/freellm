#!/bin/bash
# gather-llm-apis.sh - Discover free LLM APIs via X scan + web search
#
# Replaces the previous version which had a hardcoded JSON blob.
# This version runs the real discovery pipeline:
<<<<<<< HEAD
#   1. Scan x.pcstyle.dev for free-tier announcements
#   2. Extract and verify provider info from posts
#   3. Update data/models.json with real findings
#   4. Update settings.json with verified models
#
# Usage:
#   bash scripts/gather-llm-apis.sh [--force] [--queries queries.txt]
=======
#   1. Scan x.pcstyle.dev for free-tier announcements (leads, not facts)
#   2. Extract provider info from posts
#   3. Probe public model catalogs keylessly for ground truth (OpenRouter
#      free list + first-party /models) - see scripts/discover-probes.py
#   4. Merge leads + probes + hand-verified facts into data/models.json
#   5. Update settings.json with verified models
#
# Usage:
#   bash scripts/gather-llm-apis.sh [--force] [--queries queries.txt] [--skip-x]
#
# --skip-x skips the X scan/extract steps (no browse-x helper, e.g. CI). The
# pipeline then runs on existing X data plus the keyless live probes, which
# need no credentials at all.
>>>>>>> 382d5fc (minor modifications)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$BASE_DIR/data"
RAW_DIR="$DATA_DIR/raw"
DOCS_DIR="$BASE_DIR/docs"
MODELS_FILE="$DATA_DIR/models.json"

FORCE=false
QUERIES=""
<<<<<<< HEAD
=======
SKIP_X=false
>>>>>>> 382d5fc (minor modifications)

while [[ $# -gt 0 ]]; do
    case "$1" in
        --force)   FORCE=true; shift ;;
        --queries) QUERIES="$2"; shift 2 ;;
<<<<<<< HEAD
=======
        --skip-x)  SKIP_X=true; shift ;;
>>>>>>> 382d5fc (minor modifications)
        *)         echo "Unknown: $1"; exit 1 ;;
    esac
done

mkdir -p "$RAW_DIR/x" "$DOCS_DIR" "$BASE_DIR/logs"

echo "=== Free LLM API Discovery ==="
echo "Timestamp: $(date -Iseconds)"
echo ""

# Step 1: Run X scan if force or no data
<<<<<<< HEAD
if [ "$FORCE" = true ] || [ ! -f "$DATA_DIR/x-posts.json" ]; then
    echo "Step 1: Scanning X for free LLM API announcements..."
    
    if [ -n "$QUERIES" ]; then
        bash "$SCRIPT_DIR/x-scan.sh" --queries "$QUERIES" --sleep 25 --budget 600
    else
        bash "$SCRIPT_DIR/x-scan.sh" --sleep 25 --budget 600
=======
# Pacing is left at x-scan.sh's own default (60s): its measured behaviour
# doc says faster hammering only extends the 429 cooldown.
if [ "$SKIP_X" = true ]; then
    echo "Step 1: X scan skipped (--skip-x)"
    if [ -f "$DATA_DIR/x-leads.json" ]; then
        echo "Step 2: Using existing X leads from a previous run"
    else
        echo "Step 2: No X data at all - pipeline runs on verified.json + live probes"
    fi
    echo ""
elif [ "$FORCE" = true ] || [ ! -f "$DATA_DIR/x-posts.json" ]; then
    echo "Step 1: Scanning X for free LLM API announcements..."

    if [ -n "$QUERIES" ]; then
        bash "$SCRIPT_DIR/x-scan.sh" --queries "$QUERIES" --budget 600
    else
        bash "$SCRIPT_DIR/x-scan.sh" --budget 600
    fi
    scan_rc=$?
    if [ "$scan_rc" -eq 1 ]; then
        # rc=1 = setup failure (browse-x helper missing) - not worth continuing
        echo "ERROR: x-scan.sh failed to start (browse-x skill missing?)" >&2
        exit 1
    elif [ "$scan_rc" -ne 0 ]; then
        # rc=3 = some queries hit quota; data merged from previous runs is still usable
        echo "WARNING: x-scan.sh incomplete (rc=$scan_rc) - continuing with merged data" >&2
>>>>>>> 382d5fc (minor modifications)
    fi
    echo ""
else
    echo "Step 1: X data already exists, skipping (use --force to re-scan)"
fi

<<<<<<< HEAD
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
=======
# Step 2: Extract leads from X posts (hard fail when X data exists to extract)
if [ "$SKIP_X" != true ]; then
    echo "Step 2: Extracting provider leads..."
    if ! python3 "$SCRIPT_DIR/x-extract.py"; then
        echo "ERROR: x-extract.py failed" >&2
        exit 1
    fi
    echo ""
fi

# Step 3: Keyless live probes (public model catalogs - no credentials sent).
# Failure is non-fatal: stale/absent probes.json only means no live enrichment.
echo "Step 3: Live discovery probes (keyless)..."
if ! python3 "$SCRIPT_DIR/discover-probes.py"; then
    echo "WARNING: probes failed/unavailable - continuing without live enrichment" >&2
fi
echo ""

# Step 4: Build provider database from X findings + probes + verified facts
echo "Step 4: Building provider database..."
if ! python3 "$SCRIPT_DIR/gather-x-apis.py"; then
    echo "ERROR: gather-x-apis.py failed" >&2
    exit 1
fi
echo ""

# Step 5: Update settings with verified models
echo "Step 5: Updating settings.json..."
if ! python3 "$SCRIPT_DIR/update-settings.py"; then
    echo "ERROR: update-settings.py failed" >&2
    exit 1
fi
>>>>>>> 382d5fc (minor modifications)
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
