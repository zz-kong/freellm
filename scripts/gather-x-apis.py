#!/usr/bin/env python3
"""gather-x-apis.py - replace the hardcoded known-apis.json with real X-scraped data.

<<<<<<< HEAD
Reads data/x-leads.json and data/verified.json, then emits:
=======
Reads data/x-leads.json, data/verified.json and (when present) data/probes.json
from the keyless live discovery, then emits:
>>>>>>> 382d5fc (minor modifications)
  - data/raw/known-apis.json  (machine-readable provider list)
  - data/models.json          (normalized model database)
  - docs/models.md            (human-readable documentation)

<<<<<<< HEAD
Only includes providers with a verification status of "verified" or "active".
Unverified providers are included but flagged.

This replaces the previous script which just hardcoded a JSON blob.
"""
import json, os, re, sys, html, datetime
=======
X leads are the discovery surface; live probes supply real model ids and
free-catalog facts; verified.json is the only source allowed to define a
base_url that may receive API keys. Entries carry 'verified_at' so staleness
older than STALE_DAYS days is flagged instead of silently trusted.
"""
import json, os, re, sys, html, datetime
import trust
>>>>>>> 382d5fc (minor modifications)

BASE = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
LEADS = os.path.join(BASE, 'data', 'x-leads.json')
VERIFIED = os.path.join(BASE, 'data', 'verified.json')
<<<<<<< HEAD
=======
PROBES = os.path.join(BASE, 'data', 'probes.json')
STALE_DAYS = 30
>>>>>>> 382d5fc (minor modifications)
MODELS_FILE = os.path.join(BASE, 'data', 'models.json')
KNOWN_FILE = os.path.join(BASE, 'data', 'raw', 'known-apis.json')
DOCS_FILE = os.path.join(BASE, 'docs', 'models.md')

<<<<<<< HEAD
# Map provider names (from x-leads) to canonical data
# We only include providers that were found on X AND optionally verified.
# For known providers without X coverage, we can hardcode a minimal record.
KNOWN_ADDITIONS = {
    "Ollama": {
        "base_url": "https://cloud.ollama.com/v1",
        "models": [{"name": "ollama/free-7b", "context": 131072, "output": 4096}],
        "auth": "api_key", "free_tier": True,
        "rate_limits": {"requests_per_minute": 10, "requests_per_day": 500},
        "cost": "free",
        "capabilities": {"tool_calling": False, "vision": False},
        "privacy": {"logs_prompts": False, "use_for_training": False}
    },
    "SiliconFlow": {
        "base_url": "https://api.siliconflow.cn/v1",
        "models": [{"name": "free-mixtral-8x7b", "context": 32768, "output": 4096}],
        "auth": "api_key", "free_tier": True,
        "rate_limits": {"requests_per_minute": 20, "requests_per_day": 1000},
        "cost": "free",
        "capabilities": {"tool_calling": True, "vision": False},
        "privacy": {"logs_prompts": True, "use_for_training": False}
    },
    "Cerebras": {
        "base_url": "https://api.cerebras.ai/v1",
        "models": [{"name": "warp-1", "context": 131072, "output": 131072}],
        "auth": "api_key", "free_tier": True,
        "rate_limits": {"requests_per_minute": 60},
        "cost": "free",
        "capabilities": {"tool_calling": True, "vision": False},
        "privacy": {"logs_prompts": True, "use_for_training": False}
    }
}


def load():
    leads = json.load(open(LEADS))['leads']
    verified = json.load(open(VERIFIED)).get('providers', {})
    return leads, verified


def build_provider(leads, verified):
    """Build a provider record from X leads + verification data."""
=======
# No hardcoded provider records in this script. The original hardcode here
# was fabricated by an early LLM pass (dead host cloud.ollama.com, invented
# model ids like "ollama/free-7b"/"warp-1", invented rate limits and privacy
# claims) and was removed on 2026-09-09. Providers come from three sources,
# in trust order:
#   data/verified.json (hand-verified + cited) > live keyless probes
#   (data/probes.json) > X leads. To add a provider by hand, edit
#   data/verified.json with a source quote and a fresh verified_at - see the
#   "Adding a provider by hand" section in README.md, not a dict in here.


def norm(name):
    """Provider-name key for matching across X leads / probes / verified.json."""
    return re.sub(r'[^a-z0-9]', '', str(name).lower())


def load():
    # --skip-x runs (CI) have no X data: leads are optional, ground truth comes
    # from verified.json + the keyless live probes.
    leads = json.load(open(LEADS))['leads'] if os.path.exists(LEADS) else []
    verified = json.load(open(VERIFIED)).get('providers', {})
    probes = {}
    if os.path.exists(PROBES):
        try:
            for pname, p in json.load(open(PROBES)).get('sources', {}).items():
                probes[norm(pname)] = dict(p, _display=pname)
        except (ValueError, OSError) as e:
            print(f"WARNING: ignoring unreadable probes.json ({e})", file=sys.stderr)
    return leads, verified, probes


def models_from_probe(pentry, lead):
    """Turn a successful probe into model records with REAL ids.

    Returns None when the probe gives no model list (auth-required listing
    still has value elsewhere: it confirms the endpoint and base_url)."""
    if pentry.get('status') == 'ok' and pentry.get('free_models'):
        models = []
        for fm in pentry['free_models'][:8]:
            models.append({
                "name": fm['id'],
                "name_verified": True,
                "context": fm.get('context'),
                "output": None,
                "modality": "text",
                "capabilities": {"tool_calling": fm.get('tool_calling'),
                                 "vision": fm.get('vision')},
            })
        return models
    if pentry.get('status') == 'public_model_list' and pentry.get('model_ids'):
        cands = (lead or {}).get('context_candidates') or []
        ctx = cands[0] if cands else None
        return [{"name": mid, "name_verified": True, "context": ctx,
                 "output": None, "modality": "text"}
                for mid in pentry['model_ids'][:8]]
    return None


def promo_from(lead, v):
    """Structured promo window: dates from X extraction, narrative from verified.json."""
    promo = {}
    if lead and lead.get('promo_end_dates'):
        promo["end_dates"] = lead['promo_end_dates']
        promo["expired"] = bool(lead.get('promo_expired'))
    vp = (v or {}).get('promo') or {}
    if vp.get('end'):
        promo.setdefault("end_dates", [vp['end']])
    for k in ('claim', 'state', 'corroboration'):
        if vp.get(k):
            promo[k] = vp[k]
    return promo or None


def build_provider(leads, verified, probes):
    """Build a provider record from X leads + verification data + live probes."""
>>>>>>> 382d5fc (minor modifications)
    providers = []

    for lead in leads:
        std = lead['provider']
        v = verified.get(std, {})
        status = lead.get('verification', 'unverified')

        # Skip expired providers
        if status == 'expired':
            continue

        # Get privacy info
        priv = v.get('privacy', {})
        privacy = {
            "logs_prompts": True,
            "use_for_training": status != 'verified',  # unverified assumes worst
        }
        if priv.get('verdict') == 'risk_confirmed':
            privacy["use_for_training"] = True
            privacy["human_reviewers"] = True
        elif priv.get('verdict') == 'unknown_third_party':
            privacy["third_party_reseller"] = True

        # Add regional exception note
        if priv.get('regional_exception'):
            privacy["regional_exception"] = priv['regional_exception']

<<<<<<< HEAD
        # Build from leads
        models = []
        for ctx in lead.get('context_candidates', []):
            models.append({
                "name": f"{std.lower().replace(' ', '-')}-free",
=======
        # Build from leads. Model ids are NOT confirmed real ids (X posts
        # rarely name them), so mark them and test-apis.py re-derives a real
        # one from the provider's /models endpoint. Context that was never
        # stated in evidence stays null instead of a made-up default.
        synth_name = f"{std.lower().replace(' ', '-')}-free"
        models = []
        for ctx in lead.get('context_candidates', []):
            models.append({
                "name": synth_name,
                "name_verified": False,
>>>>>>> 382d5fc (minor modifications)
                "context": ctx,
                "output": ctx // 2,
                "modality": "text"
            })
        if not models:
            models.append({
<<<<<<< HEAD
                "name": f"{std.lower().replace(' ', '-')}-free",
                "context": 131072,
                "output": 8192,
=======
                "name": synth_name,
                "name_verified": False,
                "context": None,
                "output": None,
>>>>>>> 382d5fc (minor modifications)
                "modality": "text"
            })

        # Get endpoints from evidence URLs
        endpoints = []
        for ev in lead.get('evidence', [])[:5]:
            text = ev.get('excerpt', '') + ' ' + ev.get('url', '')
<<<<<<< HEAD
            for m in re.finditer(r'https?://(?:[a-z0-9-]+\.)+(?:com|ai|io|dev|cloud)\b[^\s,)]*', text, re.I):
                u = m.group(0).rstrip('.,;')
=======
            for m in re.finditer(r'https?://(?:[a-z0-9-]+\.)+(?:com|ai|io|dev|cloud)\b[^\s,)"\'>]*', text, re.I):
                u = m.group(0).rstrip('.,;"\'')
>>>>>>> 382d5fc (minor modifications)
                if 'x.com/' not in u and 't.co/' not in u:
                    endpoints.append(u)
        endpoints = list(dict.fromkeys(endpoints))[:3]

<<<<<<< HEAD
        provider = {
            "provider": std,
            "name": std,
            "base_url": endpoints[0] if endpoints else f"https://api.{std.lower().replace(' ', '')}.com/v1",
            "models": models,
            "auth": "api_key",
            "free_tier": True,
            "rate_limits": {},
            "cost": "free",
            "capabilities": {"tool_calling": True, "vision": True},
            "privacy": privacy,
            # X discovery provenance
            "_source": "x_scan",
=======
        # Base URL policy: NEVER guess a domain (a guessed https://api.<name>.com
        # is an uncontrolled destination for users' API keys). Order of trust:
        #   1. api_base_url manually verified in data/verified.json
        #   2. a scraped URL whose HOST plausibly belongs to this provider
        #      (trust.endpoint_affinity) - roundup posts quote many providers'
        #      URLs side by side, so the first URL in a post is often someone
        #      else's site; non-matching URLs stay as mentioned_urls only
        #   3. none - scripts/trust.py decides which of these may receive keys.
        vbase = v.get('api_base_url', '')
        mentioned = []
        if vbase:
            base_url, base_src = vbase, 'verified'
            mentioned = [u for u in endpoints if u != vbase]
        else:
            matched = [u for u in endpoints if trust.endpoint_affinity(std, u)]
            if matched:
                base_url, base_src = matched[0], 'x_scraped'
                mentioned = [u for u in endpoints if u not in matched]
            else:
                base_url, base_src = '', 'none'
                mentioned = list(endpoints)

        provider = {
            "provider": std,
            "name": std,
            "base_url": base_url,
            "models": models,
            "auth": "api_key",
            "free_tier": True,

            "rate_limits": {},
            "cost": "free",
            # capabilities stay unknown unless confirmed - do not claim true
            "capabilities": {"tool_calling": None, "vision": None},
            "privacy": privacy,
            # X discovery provenance
            "_source": "x_scan",
            "_base_url_source": base_src,
            "_mentioned_urls": mentioned,
>>>>>>> 382d5fc (minor modifications)
            "_x_posts": lead.get('post_count', 0),
            "_confidence": lead.get('confidence', 0),
            "_verified_status": status,
        }

        if lead.get('promo_end_dates'):
            provider["_promo_end"] = lead['promo_end_dates']
        if lead.get('rpm'):
            provider["rate_limits"]["requests_per_minute"] = lead['rpm'][0]
        if lead.get('rpd'):
            provider["rate_limits"]["requests_per_day"] = lead['rpd'][0]

<<<<<<< HEAD
=======
        # Auth is verified.json's to declare - a public /models list never
        # infers keyless access (see note below). '"auth": "none"' set here is
        # the ONLY channel by which a card can ever become keyless.
        if v.get('auth'):
            provider["auth"] = v['auth']
        # Hand-written extras travel through to the card's expandable details
        if v.get('notes'):
            provider["_notes"] = v['notes']
        if v.get('source'):
            provider["_verified_source"] = v['source']

>>>>>>> 382d5fc (minor modifications)
        # Add verification note
        if v.get('x_claim_verdict'):
            provider["_claim_verdict"] = v['x_claim_verdict']
        if priv.get('quote'):
            provider["_privacy_quote"] = priv['quote']

<<<<<<< HEAD
        providers.append(provider)

    # Add known providers without X coverage
    for std, data in KNOWN_ADDITIONS.items():
        if not any(p.get('provider') == std for p in providers):
            provider = {'provider': std, 'name': std}
            provider.update(data)
            provider['_source'] = 'hand_verified'
            provider['_verified_status'] = 'unverified'
            providers.append(provider)
=======
        # Structured promo window + manual-verification date
        promo = promo_from(lead, v)
        if promo:
            provider["_promo"] = promo
        if v.get('verified_at'):
            provider["_verified_at"] = v['verified_at']

        # Privacy: carry the cited verdict/detail so the site can show WHY
        # a badge says "trains on data".
        if priv.get('verdict'):
            privacy["verdict"] = priv['verdict']
        if priv.get('detail'):
            privacy["detail"] = priv['detail']

        # Live keyless probe (data/probes.json) - ground truth over claims.
        pentry = probes.get(norm(std))
        if pentry:
            provider["_probed"] = {"status": pentry.get('status'),
                                   "checked_at": pentry.get('checked_at')}
            pm = models_from_probe(pentry, lead)
            if pm:
                provider["models"] = pm
                provider["_probed"]["real_model_ids"] = True
            # NOTE: a public /models list does NOT mean keyless use. Live tests
            # (2026-09-09) confirmed ollama.com, opencode.ai/zen and llm7.io all
            # reject CHAT without a key while their listings are open. Auth is
            # only ever 'none' when verified.json says so.
            pb = pentry.get('base_url', '')
            # Only a first-party https host on TRUSTED_HOSTS upgrades the base.
            if trust.host_of(pb) in trust.TRUSTED_HOSTS and provider["_base_url_source"] in ('x_scraped', 'none'):
                provider["base_url"] = pb
                provider["_base_url_source"] = 'trusted_host'

        providers.append(provider)

    # Manual adds: providers that exist ONLY in data/verified.json - no X
    # lead, no first-party probe. This is the "I want to add a provider
    # myself" entry point. verified.json is the highest-trust source, so
    # its api_base_url is the only kind of base URL users' keys may be sent
    # to (scripts/trust.py). Recognized fields:
    #   api_base_url  https endpoint - required to show a base URL at all
    #   auth          "api_key" (default) or "none"; verified.json is the
    #                 ONLY place keyless access may be declared
    #   models        [{"name","context","output","modality"}] - hand-listed
    #   rate_limits   e.g. {"requests_per_minute": 40}
    #   capabilities  e.g. {"tool_calling": true, "vision": false}
    #   privacy       {"verdict","detail","quote",...} - cite the terms page
    #   promo         {"end","claim","state"} for time-limited free tiers
    #   verified_at   ISO date of your check (drives the stale-30d warning)
    #   display       nicer name than the dict key, if they differ
    #   source        URL of the primary source you verified against
    for std, v in verified.items():
        if any(norm(std) == norm(p['provider']) for p in providers):
            continue
        # A hand entry explicitly marked expired (e.g. a promo whose end date
        # passed) must not be listed as an active free tier - same rule the
        # lead loop applies to expired X leads.
        if v.get('status') == 'expired':
            continue
        models = [{"name": mm.get('name', '?'), "name_verified": True,
                   "context": mm.get('context'), "output": mm.get('output'),
                   "modality": mm.get('modality', 'text')}
                  for mm in (v.get('models') or [])]
        provider = {
            "provider": std,
            "name": v.get('display', std),
            "base_url": v.get('api_base_url', ''),
            "models": models,
            "auth": v.get('auth', 'api_key'),
            "free_tier": v.get('free_tier', True),
            "rate_limits": v.get('rate_limits', {}),
            "cost": "free",
            "capabilities": {"tool_calling": None, "vision": None,
                             **(v.get('capabilities') or {})},
            "privacy": dict(v.get('privacy') or {}),
            "_source": "hand_verified",
            "_base_url_source": "verified" if v.get('api_base_url') else "none",
            "_verified_status": "verified",
            "_x_posts": 0,
            "_confidence": 100,
        }
        if (v.get('privacy') or {}).get('quote'):
            provider["_privacy_quote"] = v['privacy']['quote']
        if v.get('source'):
            provider["_verified_source"] = v['source']
        if v.get('notes'):
            provider["_notes"] = v['notes']
        promo = promo_from(None, v)
        if promo:
            provider["_promo"] = promo
        if v.get('verified_at'):
            provider["_verified_at"] = v['verified_at']
        # A live probe enriches a hand entry exactly like a lead: real ids,
        # endpoint confirmation. It never overrides a manually verified base.
        pentry = probes.get(norm(std))
        if pentry:
            provider["_probed"] = {"status": pentry.get('status'),
                                   "checked_at": pentry.get('checked_at')}
            pm = models_from_probe(pentry, None)
            if pm:
                provider["models"] = pm
                provider["_probed"]["real_model_ids"] = True
        providers.append(provider)

    # Providers seen LIVE (free models on OpenRouter, public /models lists)
    # even when no X post ever mentioned them - ground truth needs no hype.
    seen = {norm(p.get('provider', '')) for p in providers}
    for pname, pentry in probes.items():
        if pname in seen:
            continue
        pm = models_from_probe(pentry, None)
        if not pm:
            continue
        providers.append({
            "provider": pentry.get('_display', pname.title()),
            "name": pentry.get('_display', pname.title()),
            "base_url": pentry.get('base_url', ''),
            "models": pm,
            # A public model listing proves discovery, not keyless chat
            # (see note above) - chat auth is verified.json's to declare.
            "auth": "api_key",
            "free_tier": True,
            "rate_limits": {}, "cost": "free",
            "capabilities": {"tool_calling": None, "vision": None},
            "privacy": {},
            "_source": "live_probe", "_base_url_source": "trusted_host",
            "_verified_status": "probed",
            "_probed": {"status": pentry.get('status'),
                        "checked_at": pentry.get('checked_at'),
                        "real_model_ids": True},
        })
>>>>>>> 382d5fc (minor modifications)

    return providers


<<<<<<< HEAD
=======
def promo_text(p):
    """One-line promo status: end date with live countdown, or None."""
    promo = p.get('_promo')
    if not promo:
        return None
    dates = promo.get('end_dates') or []
    txt = ', '.join(dates) if dates else (promo.get('state') or 'time-limited')
    if dates:
        try:
            end = min(datetime.date.fromisoformat(d) for d in dates)
            days = (end - datetime.date.today()).days
            if days < 0:
                txt += f' — ENDED {-days}d ago ⚠️'
            elif days == 0:
                txt += ' — LAST DAY ⚠️'
            else:
                txt += f' — {days}d left'
        except ValueError:
            pass
    return txt


def staleness(p):
    """'verified 12d ago' note, flagged when older than STALE_DAYS."""
    va = p.get('_verified_at')
    if not va:
        return None
    try:
        d = (datetime.date.today() - datetime.date.fromisoformat(va)).days
    except ValueError:
        return None
    if d <= 1:
        return f"manually verified {va}"
    note = f"manually verified {va} ({d} days ago)"
    if d > STALE_DAYS:
        note += f" — ⚠️ STALE, re-check primary sources"
    return note


>>>>>>> 382d5fc (minor modifications)
def write_known(providers):
    """Write raw known-apis.json."""
    with open(KNOWN_FILE, 'w') as f:
        json.dump(providers, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(providers)} providers -> {KNOWN_FILE}")


def write_models(providers):
    """Write normalized data/models.json."""
    models = []
    for p in providers:
<<<<<<< HEAD
=======
        # The cited privacy quote lives at record level for lead merges; the
        # site drawer reads privacy.quote, so fold it in here.
        priv = dict(p.get('privacy') or {})
        if p.get('_privacy_quote'):
            priv.setdefault('quote', p['_privacy_quote'])
>>>>>>> 382d5fc (minor modifications)
        models.append({
            "provider": p.get('provider','?'),
            "name": p.get('name',p.get('provider','?')),
            "base_url": p.get('base_url','?'),
            "models": p.get('models',[]),
            "auth": p.get('auth','api_key'),
            "free_tier": p.get('free_tier',True),
            "rate_limits": p.get('rate_limits',{}),
            "capabilities": p.get('capabilities',{'tool_calling':True,'vision':True}),
            "cost": p.get('cost','free'),
<<<<<<< HEAD
            "privacy": p.get('privacy',{}),
            "status": p.get('_verified_status','unverified'),
            "verified_from_x": p.get('_source') == 'x_scan',
            "context_from_x": p.get('_x_posts',0),
            "promo_warning": p.get('_claim_verdict'),
=======
            "privacy": priv,
            "status": p.get('_verified_status','unverified'),
            "verified_from_x": p.get('_source') == 'x_scan',
            "base_url_source": p.get('_base_url_source', 'hand_verified'),
            "context_from_x": p.get('_x_posts',0),
            "promo_warning": p.get('_claim_verdict'),
            "promo": p.get('_promo'),
            "verified_at": p.get('_verified_at'),
            "probed": p.get('_probed'),
            "mentioned_urls": p.get('_mentioned_urls', []),
            "notes": p.get('_notes'),
            "source": p.get('_verified_source'),
>>>>>>> 382d5fc (minor modifications)
        })
    with open(MODELS_FILE, 'w') as f:
        json.dump(models, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(models)} models -> {MODELS_FILE}")


def write_docs(providers):
    """Write human-readable docs/models.md."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    lines = [
        '# Free LLM APIs', '',
        f'- generated: `{now}`',
        f'- providers: `{len(providers)}`',
        '',
        '> ⚠️ Only providers with **verified_from_x = true** have been confirmed via X post evidence.',
        '> Providers with **status = expired** should not be listed as active free tiers.',
        '',
        '| # | Provider | Status | Context | Promo End | Auth |',
        '|---|----------|--------|---------|-----------|------|',
    ]

    for i, p in enumerate(providers, 1):
<<<<<<< HEAD
        ctx = ', '.join(f"{m.get('context','?')} tokens" for m in p.get('models',[])[:1]) or '-'
        promo = p.get('_promo_end')
        if promo:
            promo = ', '.join(promo) + (' ⚠️ EXPIRED' if p.get('_verified_status') == 'expired' else '')
=======
        ctx = ', '.join(f"{m['context']} tokens" if m.get('context') else 'unknown'
                        for m in p.get('models', [])[:1]) or '-'
        promo = promo_text(p)
>>>>>>> 382d5fc (minor modifications)
        lines.append(f'| {i} | {p["provider"]} | {p.get("_verified_status","unverified")} | {ctx} | {promo or "-"} | {p["auth"]} |')

    lines.extend(['', ''])

    for i, p in enumerate(providers, 1):
        lines += [
            f'## {i}. {p["provider"]}', '',
            f'- **Status**: `{p.get("_verified_status","unverified")}`',
<<<<<<< HEAD
            f'- **Base URL**: `{p["base_url"]}`',
=======
            f'- **Base URL**: `{p["base_url"] or "unknown - not confirmed from any evidence"}`',
            ('  > ⚠️ This base URL was scraped from a post - verify it on the provider\'s own site before sending any API key.'
             if p.get('_base_url_source') == 'x_scraped' else ''),
            (f'  > Other URLs quoted in the posts did not match this provider\'s name and are NOT credited as its endpoint: '
             + ', '.join(f'`{u}`' for u in p.get('_mentioned_urls', [])[:3])
             if not p.get('base_url') and p.get('_mentioned_urls') else ''),
>>>>>>> 382d5fc (minor modifications)
            f'- **Auth**: {p["auth"]}',
            f'- **Rate Limits**: {json.dumps(p["rate_limits"]) or "N/A"}',
            '',
        ]

<<<<<<< HEAD
=======
        # Promo window with live countdown
        promo = promo_text(p)
        if promo:
            lines.append(f'- **Promo ends**: {promo}')
            lines.append('')

        # Staleness of the manual verification
        stale = staleness(p)
        if stale:
            lines.append(f'- **Verification age**: {stale}')
            lines.append('')

        # Live keyless probe result
        probed = p.get('_probed')
        if probed:
            real = ' — real model ids confirmed' if probed.get('real_model_ids') else ''
            lines.append(f'- **Live probe** ({probed.get("checked_at","?")}): '
                         f'`{probed.get("status","?")}`{real}')
            lines.append('')

>>>>>>> 382d5fc (minor modifications)
        # Claims from X
        claim = p.get('_claim_verdict')
        if claim:
            lines.append(f'> **X claim verdict**: {claim}')
            lines.append('')

        # Privacy
        priv = p.get('privacy', {})
        priv_notes = []
        if priv.get('logs_prompts'):
            priv_notes.append('Logs prompts: **Yes**')
        if priv.get('use_for_training'):
            priv_notes.append('Used for training: **Yes**')
        if priv.get('human_reviewers'):
            priv_notes.append('Human reviewers: **Yes**')
        if priv.get('third_party_reseller'):
            priv_notes.append('Third-party reseller: **Yes** (data terms unknown)')
        if priv.get('regional_exception'):
            priv_notes.append(f'Regional exception: {priv["regional_exception"]}')
        if not priv_notes:
            priv_notes.append('Not confirmed (unverified)')

        lines.append('### Privacy')
        for n in priv_notes:
            lines.append(f'- {n}')
        lines.append('')

        # Models
        lines.append('### Models')
        for m in p.get('models', []):
<<<<<<< HEAD
            lines.append(f'- `{m.get("name","?")}` — Context: `{m.get("context","?")}`, Output: `{m.get("output","?")}`')
=======
            ctx = m.get('context') if m.get('context') else 'unknown'
            out = m.get('output') if m.get('output') else 'unknown'
            note = '' if m.get('name_verified') else ' _(inferred id - confirm via /models)_'
            lines.append(f'- `{m.get("name","?")}` — Context: `{ctx}`, Output: `{out}`{note}')
>>>>>>> 382d5fc (minor modifications)
        lines.append('')

        provenance = []
        if p.get('_source') == 'x_scan':
            provenance.append(f"Discovered via X ({p.get('_x_posts',0)} posts)")
        if p.get('_source') == 'hand_verified':
            provenance.append("Manual verification")
<<<<<<< HEAD
=======
        if p.get('_source') == 'live_probe':
            provenance.append("Discovered via keyless live probe")
>>>>>>> 382d5fc (minor modifications)
        if provenance:
            lines.append(f'*Source: {", ".join(provenance)}*')
            lines.append('')

        lines.append('')

    with open(DOCS_FILE, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Wrote documentation -> {DOCS_FILE}")


def main():
<<<<<<< HEAD
    leads, verified = load()
    providers = build_provider(leads, verified)
=======
    leads, verified, probes = load()
    providers = build_provider(leads, verified, probes)
>>>>>>> 382d5fc (minor modifications)
    write_known(providers)
    write_models(providers)
    write_docs(providers)
    print(f"\nDone: {len(providers)} providers in data/")


main()
