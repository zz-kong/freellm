#!/bin/bash
# publish-docs.sh - Build and optionally deploy documentation
#
# Usage:
#   bash scripts/publish-docs.sh              # build only
#   bash scripts/publish-docs.sh --deploy     # deploy to GitHub Pages
#   bash scripts/publish-docs.sh --cloudflare # deploy via wrangler

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
DOCS_DIR="$BASE_DIR/docs"
DATA_DIR="$BASE_DIR/data"
MODELS_FILE="$DATA_DIR/models.json"
SITE_DIR="$DOCS_DIR/site"
DEPLOY="no"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --deploy)     DEPLOY="github"; shift ;;
        --cloudflare) DEPLOY="cloudflare"; shift ;;
        --help)       cat <<'EOF'
Usage: bash scripts/publish-docs.sh [--deploy|--cloudflare]

Options:
  --deploy          Deploy to GitHub Pages (requires git)
  --cloudflare      Deploy to Cloudflare Pages (requires wrangler)
EOF
       exit 0 ;;
    *) echo "Unknown: $1"; exit 1 ;;
    esac
done

mkdir -p "$SITE_DIR"

echo "=== Building Documentation Site ==="

# Generate HTML from data/models.json + verified.json
python3 - <<'PYEOF'
import json, os, datetime

BASE = "/data/data/com.termux/files/home/freellm"
models = json.load(open(os.path.join(BASE, "data/models.json")))
verified = json.load(open(os.path.join(BASE, "data/verified.json"))).get("providers", {})
xfindings = open(os.path.join(BASE, "docs/x-findings.md")).read()

verified_count = sum(1 for m in models if m.get("status") in ("verified", "active"))
unverified = sum(1 for m in models if m.get("status") not in ("verified", "active", "expired"))
expired = sum(1 for m in models if m.get("status") == "expired")

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

# Build provider cards
cards = ""
for m in models:
    provider = m.get("provider", "?")
    base_url = m.get("base_url", "?")
    status = m.get("status", "?")
    ctx = m.get("rate_limits", {}).get("requests_per_minute", "?") or "?"
    auth = m.get("auth", "?")
    caps = m.get("capabilities", {})
    cap_str = "Tool" if caps.get("tool_calling") else ""
    if caps.get("vision"): cap_str += ", Vision"
    
    # Status icon
    if status == "verified":
        icon = "✅"
    elif status == "active":
        icon = "🟢"
    elif status == "expired":
        icon = "❌"
    else:
        icon = "⚪"
    
    cards += f"""    <div class="card" data-name="{provider.lower()}" data-provider="{provider.lower()}">
      <div class="card-header">
        <span class="card-name">{provider}</span>
        <span class="badge badge-{status}">{icon} {status}</span>
      </div>
      <div class="card-body">
        <p><strong>Base URL:</strong> <code>{base_url}</code></p>
        <p><strong>Auth:</strong> {auth} | <strong>Rate:</strong> {ctx} RPM</p>
        <p><strong>Capabilities:</strong> {cap_str or "N/A"}</p>
      </div>
    </div>"""

# Verified providers detail
verified_detail = ""
for std, vdata in verified.items():
    priv = vdata.get("privacy", {})
    quote = priv.get("quote", "")
    claim = vdata.get("x_claim_verdict", "")
    verified_detail += f"""
    <details>
      <summary><strong>{std}</strong> — {vdata.get('status', 'unverified')}</summary>
      {f'<p><strong>Privacy:</strong> {priv.get("detail", priv.get("quote", "Not verified"))}</p>' if priv.get('detail') else ''}
      {f'<blockquote>{quote}</blockquote>' if quote else ''}
      {f'<p><strong>Claim verdict:</strong> {claim}</p>' if claim else ''}
    </details>"""

# Markdown body from x-findings
md_body = xfindings.replace("`", "&grave;")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Free LLM APIs</title>
  <style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; background:#f5f5f5; color:#1a1a1a; line-height:1.6; }}
    .container {{ max-width:960px; margin:0 auto; padding:2rem; }}
    h1 {{ font-size:2rem; margin-bottom:0.5rem; }}
    .subtitle {{ color:#666; margin-bottom:2rem; }}
    .stats {{ display:flex; gap:1rem; margin:1.5rem 0; flex-wrap:wrap; }}
    .stat {{ background:#fff; padding:1rem 1.5rem; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,0.1); }}
    .stat-num {{ font-size:1.5rem; font-weight:bold; }}
    .stat-label {{ color:#666; font-size:0.85rem; }}
    .search {{ margin:1.5rem 0; }}
    .search input {{ width:100%; padding:0.75rem 1rem; font-size:1rem; border:2px solid #ddd; border-radius:8px; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:1rem; margin:1.5rem 0; }}
    .card {{ background:#fff; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,0.1); overflow:hidden; }}
    .card-header {{ padding:0.75rem 1rem; background:#fafafa; border-bottom:1px solid #eee; display:flex; justify-content:space-between; align-items:center; }}
    .card-name {{ font-weight:600; }}
    .badge {{ font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:12px; }}
    .badge-verified {{ background:#dcfce7; color:#166534; }}
    .badge-active {{ background:#dbeafe; color:#1e40af; }}
    .badge-expired {{ background:#fee2e2; color:#991b1b; }}
    .badge-unverified {{ background:#f3f4f6; color:#6b7280; }}
    .card-body {{ padding:1rem; }}
    .card-body p {{ margin:0.25rem 0; font-size:0.9rem; }}
    .card-body code {{ background:#f3f4f6; padding:0.1rem 0.3rem; border-radius:3px; font-size:0.8rem; }}
    .verified-section {{ margin:2rem 0; padding:1rem; background:#fff; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,0.1); }}
    details {{ margin:0.5rem 0; }}
    summary {{ cursor:pointer; padding:0.5rem; background:#fafafa; border-radius:4px; }}
    blockquote {{ margin:0.5rem 0; padding:0.5rem 1rem; background:#f9f9f9; border-left:3px solid #ccc; font-size:0.9rem; }}
    .md-section {{ margin:2rem 0; padding:1rem; background:#fff; border-radius:8px; }}
    .md-section pre {{ white-space:pre-wrap; font-size:0.85rem; }}
    footer {{ text-align:center; margin-top:3rem; color:#999; font-size:0.85rem; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Free LLM APIs</h1>
    <p class="subtitle">Curated list · Generated {now} · {len(models)} providers</p>
    
    <div class="stats">
      <div class="stat"><div class="stat-num">{verified_count}</div><div class="stat-label">Verified</div></div>
      <div class="stat"><div class="stat-num">{unverified}</div><div class="stat-label">Unverified</div></div>
      <div class="stat"><div class="stat-num">{expired}</div><div class="stat-label">Expired</div></div>
      <div class="stat"><div class="stat-num">{len(models)}</div><div class="stat-label">Total</div></div>
    </div>
    
    <div class="search">
      <input type="text" id="search" placeholder="Search providers...">
    </div>
    
    <div class="cards" id="cards">
{cards}
    </div>
    
    <div class="verified-section">
      <h2>Verified Provider Details</h2>
      <p>Providers confirmed against official source documentation:</p>
      {verified_detail if verified_detail else '<p>No verified providers yet.</p>'}
    </div>
    
    <div class="md-section">
      <h2>X Scan Findings</h2>
      <pre>{md_body[:12000]}</pre>
    </div>
    
    <footer>
      <p>Generated by Free LLM API Discovery · Data from X + official provider docs</p>
    </footer>
  </div>
  
  <script>
    document.getElementById("search").addEventListener("input", function() {{
      var q = this.value.toLowerCase();
      document.querySelectorAll(".card").forEach(function(c) {{
        var name = c.querySelector(".card-name").textContent.toLowerCase();
        c.style.display = name.includes(q) ? "" : "none";
      }});
    }});
  </script>
</body>
</html>"""

with open(os.path.join(BASE, "docs/site/index.html"), "w") as f:
    f.write(html)
print(f"HTML site: {len(html)} bytes -> docs/site/index.html")

PYEOF

echo "HTML site generated: $SITE_DIR"
echo ""

# Deployment section
if [ "$DEPLOY" = "no" ]; then
    echo "=== Build Complete ==="
    echo "Site location: $SITE_DIR"
    echo ""
    echo "To deploy:"
    echo "  bash scripts/publish-docs.sh --deploy        (GitHub Pages)"
    echo "  bash scripts/publish-docs.sh --cloudflare    (Cloudflare Pages)"
    exit 0
fi

echo "=== Deploying to $DEPLOY ==="
echo ""

case "$DEPLOY" in
    github)
        if ! command -v git &>/dev/null; then
            echo "ERROR: git not installed. Install with: pkg install git"
            exit 1
        fi
        
        # Initialize git repo if needed
        if [ ! -d ".git" ]; then
            echo "Initializing git repository..."
            git init -b main >/dev/null 2>&1
            git add . >/dev/null 2>&1
            git commit -m "init: freellm project" >/dev/null 2>&1
            echo "Repository initialized."
        fi
        
        echo ""
        echo "GitHub Pages deployment:"
        echo ""
        echo "Option A: Manual push to docs/ folder"
        echo "  cp -r docs/site/* .  # copy to repo root"
        echo "  git add . && git commit -m 'deploy site' && git push"
        echo ""
        echo "  Then: Settings → Pages → Build and deployment → Source: 'Deploy from a branch'"
        echo "        Branch: main, Folder: / (root)"
        echo ""
        echo "Option B: gh-pages branch"
        echo "  git checkout --orphan gh-pages"
        echo "  git rm -rf . >/dev/null 2>&1 || true"
        echo "  cp -r docs/site/* . >/dev/null 2>&1"
        echo "  git add . && git commit -m 'Deploy site'"
        echo "  git push origin gh-pages --force"
        echo ""
        echo "Option C: If you have a GitHub remote configured:"
        echo "  git remote -v | head -2"
        echo "  gh repo create 2>/dev/null || echo 'Install gh CLI: pkg install gh'"
        ;;
    cloudflare)
        if command -v wrangler &>/dev/null; then
            echo "Wrangler found. Deploying..."
            cd "$SITE_DIR"
            wrangler pages deploy . --project-name freellm 2>/dev/null
            cd "$BASE_DIR"
        else
            echo "Wrangler not found."
            echo ""
            echo "Install: npm install -g wrangler"
            echo "Or use Cloudflare Dashboard:"
            echo "  1. Go to Cloudflare → Pages → Create project"
            echo "  2. Connect to Git repo, set build output: docs/site"
            echo "  3. Or drag-drop the folder: $SITE_DIR"
        fi
        ;;
esac
