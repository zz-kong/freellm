#!/usr/bin/env bash
# x-scan.sh - gather free-LLM-API chatter from X via x.pcstyle.dev (browse-x skill)
#
# Usage:
#   bash scripts/x-scan.sh                        # default query set
#   bash scripts/x-scan.sh --queries f.txt        # one query per line, '#' = comment
#   bash scripts/x-scan.sh --status URL           # deep-dive one status (thread)
#   bash scripts/x-scan.sh --budget 900           # hard wall-clock cap (seconds)
#
# Measured behaviour of x.pcstyle.dev on the ANONYMOUS path (2026-09-08):
#   - `from:handle`  -> returns 0 results. Use `@handle` or a bare handle instead.
#   - `since:DATE`   -> honoured.
#   - `min_faves:N`  -> honoured.
#   - `until:DATE`   -> NOT honoured (future-dated posts still returned); filter client-side.
#   - quota          -> roughly 5 live searches, then HTTP 429 with Retry-After 3..31s;
#                       hammering it extends the cooldown. A single retry that waits
#                       out Retry-After is the only thing that works reliably.
#   - always write responses to FILES; command substitution can corrupt payloads that
#     contain control characters and break jq.
# Run it detached for scheduled use:
#   nohup bash scripts/x-scan.sh > logs/x-scan.log 2>&1 &
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
RAW_DIR="$BASE_DIR/data/raw/x"
OUT="$BASE_DIR/data/x-posts.json"

BX=""
for c in \
  "$HOME/.pi/agent/skills/browse-x/scripts/browse-x.ts" \
  "$BASE_DIR/../.pi/agent/skills/browse-x/scripts/browse-x.ts"; do
  if [ -f "$c" ]; then BX="$c"; break; fi
done
if [ -z "$BX" ]; then
  echo "error: browse-x.ts not found (install the browse-x skill)" >&2
  exit 1
fi
BX_DIR="$(cd "$(dirname "$BX")/.." && pwd)"   # skill root (parent of scripts/)

SLEEP="${X_SCAN_SLEEP:-60}"     # pacing between live searches
LIMIT="${X_SCAN_LIMIT:-8}"
BUDGET="${X_SCAN_BUDGET:-900}"  # hard cap on total runtime
RETRY_MAX="${X_SCAN_RETRY:-0}"  # 429s also burn quota -> default is fail fast, no retry
COOLDOWN="${X_SCAN_COOLDOWN:-0}"  # only used when RETRY_MAX > 0
MODE="search"; QFILE=""; TARGET=""

while [ $# -gt 0 ]; do
  case "$1" in
    --queries) QFILE="$2"; shift 2 ;;
    --status)  MODE="status"; TARGET="$2"; shift 2 ;;
    --sleep)   SLEEP="$2"; shift 2 ;;
    --limit)   LIMIT="$2"; shift 2 ;;
    --budget)  BUDGET="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

mkdir -p "$RAW_DIR"
TMP="${TMPDIR:-$HOME/tmp}"; mkdir -p "$TMP"; ERRF="$TMP/x_scan_err"; RA="$TMP/x_scan_ra"
START=$(date +%s)
elapsed() { echo $(( $(date +%s) - START )); }
out_of_budget() { [ "$(elapsed)" -ge "$BUDGET" ]; }

# one attempt; writes body to $1, returns 0 ok / 3 rate limited / 1 other
bx_try() {
  local dst="$1"; shift
  local rc
  ( cd "$BX_DIR" && timeout 120 bun "$BX" "$@" 2>"$ERRF" ) > "$dst"
  rc=$?
  # Success = exit 0, non-empty body, and not an error payload. (Search/profile bodies
  # carry "resource"; status bodies carry "format"/"markdown" - don't key on one shape.)
  # NOTE: grep the file directly. `head -c 400 | grep -q` breaks under `set -o pipefail`
  # because grep exits at the first match and head dies of SIGPIPE (status 141).
  if [ "$rc" -eq 0 ] && [ -s "$dst" ] && ! grep -q -m1 -F '"code":"rate_limited"' "$dst" \
     && grep -q -m1 -e '"resource"' -e '"markdown"' -e '"format"' "$dst"; then
    return 0
  fi
  if grep -q -m1 -i '429' "$ERRF" 2>/dev/null; then
    grep -i 'retry-after:' "$ERRF" | head -1 | tr -dc '0-9' > "$RA"
    return 3
  fi
  return 1
}

# attempt, then on 429 wait out Retry-After (bounded) and retry RETRY_MAX times
bx() {
  local dst="$1"; shift
  local tries=0 ra rc
  while :; do
    bx_try "$dst" "$@"; rc=$?
    if [ "$rc" -eq 0 ]; then return 0; fi
    tries=$((tries+1))
    if [ "$rc" -ne 3 ] || [ "$tries" -gt "$RETRY_MAX" ] || out_of_budget; then return "$rc"; fi
    ra="$(cat "$RA" 2>/dev/null)"; case "$ra" in ''|*[!0-9]*) ra=0;; esac
    [ "$ra" -lt "$COOLDOWN" ] && ra="$COOLDOWN"
    [ "$ra" -gt 300 ] && ra=300
    echo "    429 -> waiting ${ra}s (retry $tries/$RETRY_MAX)"
    sleep "$((ra+2))"
  done
}

slug() { printf '%s' "$1" | tr -cs 'a-zA-Z0-9' '-' | sed 's/^-*//;s/-*$//' | cut -c1-48 | tr 'A-Z' 'a-z'; }

if [ "$MODE" = "status" ]; then
  f="$RAW_DIR/status-$(slug "$(basename "$TARGET")").json"
  echo "deep-diving $TARGET"
  if bx "$f" "$TARGET" --thread full --json && [ -s "$f" ]; then
    echo "saved -> $f"
    python3 - "$f" <<'PY'
import json,sys,re
d=json.load(open(sys.argv[1]))
md=d.get('markdown') or ''
print(f"thread posts: {len(re.findall(r'^## Post', md, re.M))}")
print((d.get('text') or md)[:700])
PY
    exit 0
  fi
  echo "failed (rc=$?) - see stderr above" >&2; exit 3
fi

if [ -z "$QFILE" ]; then
  QFILE="$(mktemp)"
  printf '%s\n' \
    "free LLM API" \
    "@GroqCloud free" \
    "@OpenRouterAI free" \
    "@GoogleAIStudio free" \
    "@ollama free" \
    "free tier API no credit card" \
    "free API credits limited time" \
    "free API data training privacy" \
    > "$QFILE"
fi

echo "=== X scan via x.pcstyle.dev ==="
echo "helper=$BX  sleep=${SLEEP}s limit=$LIMIT budget=${BUDGET}s"
echo

n=0; ok=0; rl=0; skip=0
while IFS= read -r q; do
  case "$q" in ''|'#'*) continue ;; esac
  if out_of_budget; then echo "[$skip skipped: budget ${BUDGET}s exhausted]"; skip=$((skip+1)); continue; fi
  n=$((n+1))
  f="$RAW_DIR/$(slug "$q").json"
  printf '[%02d] %-40s ' "$n" "$q"
  bx "$f" search "$q" --limit "$LIMIT" --feed latest --json; rc=$?
  if [ "$rc" -eq 0 ] && [ -s "$f" ]; then
    c="$(jq -r '.posts | length' "$f" 2>/dev/null || echo '?')"
    echo "-> ${c} posts  ($(elapsed)s)"
    [ "$c" != "?" ] && ok=$((ok+1))
  else
    echo "-> blocked/error (rc=$?), recorded for next run ($(elapsed)s)"
    printf '%s\t%s\n' "$(date -u +%FT%TZ)" "$q" >> "$RAW_DIR/_misses.tsv"
    rl=$((rl+1))
  fi
  sleep "$SLEEP"
done < "$QFILE"

python3 - "$RAW_DIR" "$OUT" <<'PY'
import json,glob,os,sys
raw_dir,out=sys.argv[1],sys.argv[2]
posts={}
for f in sorted(glob.glob(os.path.join(raw_dir,'*.json'))):
    q=os.path.basename(f)[:-5]
    try: d=json.load(open(f))
    except Exception: continue
    for p in (d.get('posts') or []):
        i=p.get('id')
        if not i: continue
        e=posts.setdefault(i,dict(p))
        qs=e.setdefault('_queries',[])
        if q not in qs: qs.append(q)
json.dump(sorted(posts.values(),key=lambda p:-(p.get('created_timestamp') or 0)),
          open(out,'w'),indent=1,ensure_ascii=False)
print(f"merged {len(posts)} unique posts -> {out}")
PY
echo "queries attempted=$n saved=$ok blocked=$rl  total=$(elapsed)s"
if [ "$rl" -gt 0 ]; then
  echo "blocked queries logged to $RAW_DIR/_misses.tsv - re-run later (quota refills)"
  exit 3
fi
