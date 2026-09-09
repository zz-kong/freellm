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
<<<<<<< HEAD
python3 - <<'PYEOF'
import json, os, datetime

BASE = "/data/data/com.termux/files/home/freellm"
models = json.load(open(os.path.join(BASE, "data/models.json")))
verified = json.load(open(os.path.join(BASE, "data/verified.json"))).get("providers", {})
xfindings = open(os.path.join(BASE, "docs/x-findings.md")).read()
=======
export BASE_DIR
python3 - <<'PYEOF'
import json, os, html, datetime, re

BASE = os.environ["BASE_DIR"]
models = json.load(open(os.path.join(BASE, "data/models.json")))
verified = json.load(open(os.path.join(BASE, "data/verified.json"))).get("providers", {})
xfindings = open(os.path.join(BASE, "docs/x-findings.md")).read()
try:
    testres = json.load(open(os.path.join(BASE, "data/test-results.json")))
except FileNotFoundError:
    testres = {}

norm = lambda s: re.sub(r'[^a-z0-9]', '', str(s).lower())

# Map provider -> most recent live test result (data/test-results.json is
# rewritten by test-apis.py; missing file simply means "never tested").
tests_by_provider = {}
for r in testres.get("results", []):
    if r.get("skipped"):
        continue
    tests_by_provider[norm(r.get("provider", ""))] = {
        "when": (testres.get("test_run", {}).get("timestamp") or "")[:10],
        "score": r.get("usability_score"),
        "label": r.get("usability_label", ""),
        "ok": bool(r.get("tests", {}).get("basic_prompt", {})
                     .get("basic_prompt", {}).get("has_choices")),
    }
>>>>>>> 382d5fc (minor modifications)

verified_count = sum(1 for m in models if m.get("status") in ("verified", "active"))
unverified = sum(1 for m in models if m.get("status") not in ("verified", "active", "expired"))
expired = sum(1 for m in models if m.get("status") == "expired")
<<<<<<< HEAD

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
=======
keyless = sum(1 for m in models if m.get("auth") == "none")

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
today = datetime.date.today()

def promo_line(m):
    """(text, filterable_active_bool) for the promo window, or ('', False)."""
    promo = m.get("promo") or {}
    dates = promo.get("end_dates") or []
    if not dates:
        return "", False
    try:
        end = min(datetime.date.fromisoformat(d) for d in dates)
    except ValueError:
        return "time-limited offer", False
    days = (end - today).days
    if days < 0:
        return f"⏳ promo ended {end} ({-days}d ago)", False
    return f"⏳ free until {end} — {days}d left", True

def privacy_chips(m):
    """Privacy badges. Only stated facts get badges; worst-case assumptions
    (unverified leads assume the worst in models.json) are labeled unknown."""
    priv = m.get("privacy") or {}
    chips, known = [], False
    if priv.get("verdict"):
        known = True
        if priv.get("use_for_training"):
            chips.append('<span class="chip chip-danger" title="Confirmed against the provider\'s own terms">🧠 trains on prompts</span>')
        if priv.get("logs_prompts"):
            chips.append('<span class="chip chip-warn">📝 logs prompts</span>')
        if priv.get("third_party_reseller"):
            chips.append('<span class="chip chip-danger">🔀 3rd-party reseller</span>')
        if not (priv.get("use_for_training") or priv.get("logs_prompts")):
            chips.append('<span class="chip chip-ok">🔒 no training/logging stated</span>')
    if not known:
        chips.append('<span class="chip chip-unknown">❓ privacy unconfirmed</span>')
    return "".join(chips), known
>>>>>>> 382d5fc (minor modifications)

# Build provider cards
cards = ""
for m in models:
    provider = m.get("provider", "?")
    base_url = m.get("base_url", "?")
    status = m.get("status", "?")
    ctx = m.get("rate_limits", {}).get("requests_per_minute", "?") or "?"
    auth = m.get("auth", "?")
    caps = m.get("capabilities", {})
<<<<<<< HEAD
    cap_str = "Tool" if caps.get("tool_calling") else ""
    if caps.get("vision"): cap_str += ", Vision"
    
    # Status icon
    if status == "verified":
        icon = "✅"
    elif status == "active":
=======
    cap_tool = bool(caps.get("tool_calling"))
    cap_vision = bool(caps.get("vision"))
    for mm in m.get("models", [])[:8]:   # per-model probe facts can confirm too
        mc = mm.get("capabilities") or {}
        cap_tool = cap_tool or bool(mc.get("tool_calling"))
        cap_vision = cap_vision or bool(mc.get("vision"))
    cap_str = ", ".join(x for x in ("Tool" if cap_tool else "", "Vision" if cap_vision else "") if x)
    max_ctx = max((mm.get("context") or 0) for mm in m.get("models", [{}])) if m.get("models") else 0

    if status == "verified":
        icon = "✅"
    elif status in ("active", "probed"):
>>>>>>> 382d5fc (minor modifications)
        icon = "🟢"
    elif status == "expired":
        icon = "❌"
    else:
        icon = "⚪"
<<<<<<< HEAD
    
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
=======

    promo, promo_active = promo_line(m)
    chips, privacy_ok = privacy_chips(m)

    # Verified freshness
    stale_line = ""
    va = m.get("verified_at")
    if va:
        try:
            age = (today - datetime.date.fromisoformat(va)).days
            stale_line = (f"manually verified {va}" +
                          (f" · <span class='warn'>stale {age}d</span>" if age > 30 else ""))
        except ValueError:
            pass

    # Live probe line
    probed = m.get("probed") or {}
    probe_line = ""
    if probed.get("status"):
        st = html.escape(str(probed["status"]))
        probe_line = f"⚡ live probe {st} ({html.escape(str(probed.get('checked_at','')))[:10]})"

    # Last live usability test
    t = tests_by_provider.get(norm(provider))
    test_line = ""
    if t:
        mark = "✅" if t["ok"] else "⚠️"
        test_line = f"{mark} tested {t['when']} · {html.escape(str(t['label']))}"

    # ALL of these values originate from scraped X posts - escape before HTML
    p_e = html.escape(str(provider), quote=True)
    b_e = html.escape(str(base_url), quote=True)
    s_e = html.escape(str(status), quote=True)
    a_e = html.escape(str(auth), quote=True)
    base_note = (' <span class="warn" title="URL came from a post whose text names this provider - still verify before trusting">⚠ from post</span>'
                 if m.get("base_url_source") == "x_scraped" else "")
    # Base URL is only shown when evidence actually names it: verified,
    # live-probed, or a post URL whose host matches the provider name.
    if base_url and base_url != "?":
        base_html = f'<code>{b_e}</code>{base_note}'
    else:
        base_html = '<span class="warn">❓ not confirmed (no source names this endpoint)</span>'
    ment = m.get("mentioned_urls") or []
    ment_row = ""
    if ment and not (base_url and base_url != "?"):
        ment_row = ('<p class="muted">URLs quoted in posts but not credited '
                    'as this provider\'s endpoint: '
                    + " ".join(f'<code>{html.escape(str(u), quote=True)}</code>' for u in ment[:3])
                    + '</p>')
    # "No training" is only filterable when confirmed from primary sources (verdict),
    # same bar as the privacy chips - unverified X claims must not flip this filter.
    _pv = m.get("privacy") or {}
    notrain = 1 if _pv.get("verdict") and _pv.get("use_for_training") is False else 0
    rows = ""
    if promo: rows += f'<p class="promo">{promo}</p>'
    if test_line: rows += f'<p>{test_line}</p>'
    if probe_line: rows += f'<p class="muted">{probe_line}</p>'
    if stale_line: rows += f'<p class="muted">{stale_line}</p>'

    # Expandable details drawer: the real model list (live-probed ids when we
    # have them), daily limits, cited privacy text, promo claims, and any
    # hand-written notes from verified.json. Everything escaped - most of it
    # originates from scrapes.
    det = []
    mods = m.get("models") or []
    if mods:
        items = []
        for mm in mods[:12]:
            nm = html.escape(str(mm.get("name", "?")))
            c = mm.get("context")
            if isinstance(c, int) and c >= 1000:
                cs = f"{c // 1000}K ctx"
            elif c:
                cs = f"{c} ctx"
            else:
                cs = "ctx ?"
            mark = "" if mm.get("name_verified") else \
                ' <span class="warn" title="id inferred from a post - confirm via /models">inferred</span>'
            mc = mm.get("capabilities") or {}
            mcaps = " ".join(glyph for glyph, on in
                             (("🔧", mc.get("tool_calling")), ("👁", mc.get("vision"))) if on)
            items.append(f'<li><span><code>{nm}</code>{mark} {mcaps}</span>'
                         f'<span class="mctx">{cs}</span></li>')
        det.append('<p class="det-title">Models</p><ul class="model-list">' + "".join(items) + "</ul>")
    rl = m.get("rate_limits") or {}
    lim = []
    if rl.get("requests_per_minute"): lim.append(f"{rl['requests_per_minute']} req/min")
    if rl.get("requests_per_day"): lim.append(f"{rl['requests_per_day']} req/day")
    if lim:
        det.append('<p class="det-title">Limits</p><p>' + html.escape(", ".join(lim)) + "</p>")
    if _pv.get("detail"):
        det.append('<p class="det-title">Privacy detail</p><p>' + html.escape(str(_pv["detail"])) + "</p>")
    if _pv.get("quote"):
        det.append("<blockquote>" + html.escape(str(_pv["quote"])) + "</blockquote>")
    if _pv.get("regional_exception"):
        det.append('<p class="muted">Regional exception: ' + html.escape(str(_pv["regional_exception"])) + "</p>")
    _pm = m.get("promo") or {}
    prow = [html.escape(str(_pm[k])) for k in ("claim", "state") if _pm.get(k)]
    if prow:
        det.append('<p class="det-title">Promo</p><p>' + " — ".join(prow) + "</p>")
    if m.get("notes"):
        det.append('<p class="det-title">Notes</p><p>' + html.escape(str(m["notes"])) + "</p>")
    if m.get("source"):
        det.append('<p class="det-title">Verified against</p><p><code>' + html.escape(str(m["source"])) + "</code></p>")
    details_html = ('<div class="card-details">' + "".join(det) + "</div>" if det else
                    '<div class="card-details"><p class="muted">No extra details on record - add them via data/verified.json.</p></div>')
    card_e = '1' if probed.get('status') in ('ok', 'public_model_list') else '0'
    promo_e = '1' if promo_active else '0'
    cards += f"""    <div class="card" data-name="{p_e.lower()}" data-provider="{p_e.lower()}" data-keyless="{1 if auth=='none' else 0}" data-notrain="{notrain}" data-longctx="{1 if max_ctx >= 128000 else 0}" data-probed="{card_e}" data-promo="{promo_e}">
      <div class="card-header" role="button" tabindex="0" aria-expanded="false" title="click for model list and details">
        <span class="card-name">{p_e}</span>
        <span class="badge badge-{s_e}">{icon} {s_e}</span>
        <span class="caret">▸</span>
      </div>
      <div class="card-body">
        <p><strong>Base URL:</strong> {base_html}</p>
        {ment_row}
        <p><strong>Auth:</strong> {a_e} | <strong>Rate:</strong> {ctx} RPM | <strong>Caps:</strong> {cap_str or "unknown"}</p>
        <p class="chips">{chips}</p>
        {rows}
        {details_html}
      </div>
    </div>"""

# Verified providers detail - renders data/verified.json as written (the
# manual-add surface: what a human checked, against which source, when).
>>>>>>> 382d5fc (minor modifications)
verified_detail = ""
for std, vdata in verified.items():
    priv = vdata.get("privacy", {})
    quote = priv.get("quote", "")
    claim = vdata.get("x_claim_verdict", "")
<<<<<<< HEAD
    verified_detail += f"""
    <details>
      <summary><strong>{std}</strong> — {vdata.get('status', 'unverified')}</summary>
      {f'<p><strong>Privacy:</strong> {priv.get("detail", priv.get("quote", "Not verified"))}</p>' if priv.get('detail') else ''}
      {f'<blockquote>{quote}</blockquote>' if quote else ''}
      {f'<p><strong>Claim verdict:</strong> {claim}</p>' if claim else ''}
    </details>"""

# Markdown body from x-findings
md_body = xfindings.replace("`", "&grave;")
=======
    std_e = html.escape(str(std), quote=True)
    stat = vdata.get('status') or (f"facts checked {vdata['verified_at']}"
                                   if vdata.get('verified_at') else "no status recorded")
    stat_e = html.escape(str(stat), quote=True)
    detail_e = html.escape(str(priv.get("detail", priv.get("quote", "Not verified"))))
    quote_e = html.escape(str(quote))
    claim_e = html.escape(str(claim))
    base_e = html.escape(str(vdata.get('api_base_url', '')), quote=True)
    src_e = html.escape(str(vdata.get('source', '')))
    notes_e = html.escape(str(vdata.get('notes', '')))
    verified_detail += f"""
    <details>
      <summary><strong>{std_e}</strong> — {stat_e}</summary>
      {f'<p><strong>Verified endpoint:</strong> <code>{base_e}</code></p>' if base_e else ''}
      {f'<p><strong>Verified against:</strong> <code>{src_e}</code></p>' if src_e else ''}
      {f'<p><strong>Notes:</strong> {notes_e}</p>' if notes_e else ''}
      {f'<p><strong>Privacy:</strong> {detail_e}</p>' if priv.get('detail') else ''}
      {f'<blockquote>{quote_e}</blockquote>' if quote else ''}
      {f'<p><strong>Claim verdict:</strong> {claim_e}</p>' if claim else ''}
    </details>"""

# Markdown body from x-findings: raw tweet text/authors - full HTML escape,
# it goes into a <pre> verbatim. (Escaping backticks only leaves <script> live.)
md_body = html.escape(xfindings)
>>>>>>> 382d5fc (minor modifications)

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
<<<<<<< HEAD
    .card-header {{ padding:0.75rem 1rem; background:#fafafa; border-bottom:1px solid #eee; display:flex; justify-content:space-between; align-items:center; }}
=======
    .card-header {{ padding:0.75rem 1rem; background:#fafafa; border-bottom:1px solid #eee; display:flex; justify-content:space-between; align-items:center; gap:0.5rem; cursor:pointer; }}
    .card-header:focus-visible {{ outline:2px solid #1f2937; outline-offset:-2px; }}
    .caret {{ color:#999; font-size:0.8rem; transition:transform 0.15s; flex-shrink:0; }}
    .card.open .caret {{ transform:rotate(90deg); }}
    .card-details {{ display:none; border-top:1px dashed #e2e2e6; margin-top:0.6rem; padding-top:0.6rem; background:#fbfbfc; }}
    .card.open .card-details {{ display:block; }}
    .det-title {{ font-size:0.72rem; text-transform:uppercase; letter-spacing:0.05em; color:#888; margin:0.55rem 0 0.2rem; }}
    .model-list {{ list-style:none; margin:0; padding:0; font-size:0.82rem; }}
    .model-list li {{ display:flex; justify-content:space-between; align-items:baseline; gap:0.6rem; padding:0.12rem 0; }}
    .model-list code {{ font-size:0.78rem; word-break:break-all; }}
    .mctx {{ color:#777; white-space:nowrap; font-size:0.75rem; }}
    .card-details blockquote {{ margin:0.25rem 0 0; padding:0.3rem 0.6rem; border-left:3px solid #d7d7dd; color:#555; font-size:0.78rem; }}
>>>>>>> 382d5fc (minor modifications)
    .card-name {{ font-weight:600; }}
    .badge {{ font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:12px; }}
    .badge-verified {{ background:#dcfce7; color:#166534; }}
    .badge-active {{ background:#dbeafe; color:#1e40af; }}
    .badge-expired {{ background:#fee2e2; color:#991b1b; }}
<<<<<<< HEAD
    .badge-unverified {{ background:#f3f4f6; color:#6b7280; }}
    .card-body {{ padding:1rem; }}
    .card-body p {{ margin:0.25rem 0; font-size:0.9rem; }}
=======
    .badge-probed {{ background:#ede9fe; color:#5b21b6; }}
    .badge-unverified {{ background:#f3f4f6; color:#6b7280; }}
    .card-body {{ padding:1rem; }}
    .card-body p {{ margin:0.25rem 0; font-size:0.9rem; }}
    .chips {{ margin:0.4rem 0 !important; }}
    .chip {{ display:inline-block; font-size:0.72rem; padding:0.12rem 0.45rem; border-radius:10px; margin:0.1rem 0.15rem 0.1rem 0; white-space:nowrap; }}
    .chip-ok {{ background:#dcfce7; color:#166534; }}
    .chip-warn {{ background:#fef3c7; color:#92400e; }}
    .chip-danger {{ background:#fee2e2; color:#991b1b; }}
    .chip-unknown {{ background:#f3f4f6; color:#6b7280; }}
    .promo {{ color:#92400e; font-weight:500; }}
    .muted {{ color:#6b7280; font-size:0.8rem !important; }}
    .warn {{ color:#b45309; }}
    .filters {{ display:flex; gap:0.5rem; flex-wrap:wrap; margin:0.75rem 0 1rem; }}
    .fbtn {{ border:1px solid #ddd; background:#fff; border-radius:16px; padding:0.35rem 0.8rem; font-size:0.85rem; cursor:pointer; }}
    .fbtn.active {{ background:#1f2937; color:#fff; border-color:#1f2937; }}
>>>>>>> 382d5fc (minor modifications)
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
<<<<<<< HEAD
=======
      <div class="stat"><div class="stat-num">{keyless}</div><div class="stat-label">Keyless</div></div>
>>>>>>> 382d5fc (minor modifications)
      <div class="stat"><div class="stat-num">{unverified}</div><div class="stat-label">Unverified</div></div>
      <div class="stat"><div class="stat-num">{expired}</div><div class="stat-label">Expired</div></div>
      <div class="stat"><div class="stat-num">{len(models)}</div><div class="stat-label">Total</div></div>
    </div>
    
    <div class="search">
      <input type="text" id="search" placeholder="Search providers...">
    </div>
<<<<<<< HEAD
=======
    <div class="filters">
      <button class="fbtn" data-filter="keyless">🔓 No key needed</button>
      <button class="fbtn" data-filter="notrain">🧠 No training on prompts</button>
      <button class="fbtn" data-filter="longctx">📏 128K+ context</button>
      <button class="fbtn" data-filter="probed">⚡ Live-confirmed</button>
      <button class="fbtn" data-filter="promo">⏳ Promo active now</button>
      <span class="muted" id="shown-count" style="align-self:center"></span>
    </div>
>>>>>>> 382d5fc (minor modifications)
    
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
<<<<<<< HEAD
    document.getElementById("search").addEventListener("input", function() {{
      var q = this.value.toLowerCase();
      document.querySelectorAll(".card").forEach(function(c) {{
        var name = c.querySelector(".card-name").textContent.toLowerCase();
        c.style.display = name.includes(q) ? "" : "none";
      }});
    }});
=======
    var active = {{}};
    function apply() {{
      var q = document.getElementById("search").value.toLowerCase();
      var shown = 0;
      document.querySelectorAll(".card").forEach(function(c) {{
        var name = c.dataset.name || "";
        var ok = name.includes(q);
        for (var f in active) {{
          if (active[f] && c.getAttribute("data-" + f) !== "1") {{ ok = false; break; }}
        }}
        c.style.display = ok ? "" : "none";
        if (ok) shown++;
      }});
      document.getElementById("shown-count").textContent = shown + " of " + document.querySelectorAll(".card").length + " providers";
    }}
    document.getElementById("search").addEventListener("input", apply);
    document.querySelectorAll(".fbtn").forEach(function(b) {{
      b.addEventListener("click", function() {{
        var f = b.dataset.filter;
        active[f] = !active[f];
        b.classList.toggle("active", !!active[f]);
        apply();
      }});
    }});
    document.querySelectorAll(".card-header").forEach(function(h) {{
      function toggle() {{
        var c = h.closest(".card");
        var open = c.classList.toggle("open");
        h.setAttribute("aria-expanded", open ? "true" : "false");
      }}
      h.addEventListener("click", toggle);
      h.addEventListener("keydown", function(e) {{
        if (e.key === "Enter" || e.key === " ") {{ e.preventDefault(); toggle(); }}
      }});
    }});
    apply();
>>>>>>> 382d5fc (minor modifications)
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
