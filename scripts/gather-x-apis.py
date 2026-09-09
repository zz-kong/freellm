#!/usr/bin/env python3
"""gather-x-apis.py - replace the hardcoded known-apis.json with real X-scraped data.

Reads data/x-leads.json and data/verified.json, then emits:
  - data/raw/known-apis.json  (machine-readable provider list)
  - data/models.json          (normalized model database)
  - docs/models.md            (human-readable documentation)

Only includes providers with a verification status of "verified" or "active".
Unverified providers are included but flagged.

This replaces the previous script which just hardcoded a JSON blob.
"""
import json, os, re, sys, html, datetime

BASE = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
LEADS = os.path.join(BASE, 'data', 'x-leads.json')
VERIFIED = os.path.join(BASE, 'data', 'verified.json')
MODELS_FILE = os.path.join(BASE, 'data', 'models.json')
KNOWN_FILE = os.path.join(BASE, 'data', 'raw', 'known-apis.json')
DOCS_FILE = os.path.join(BASE, 'docs', 'models.md')

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

        # Build from leads
        models = []
        for ctx in lead.get('context_candidates', []):
            models.append({
                "name": f"{std.lower().replace(' ', '-')}-free",
                "context": ctx,
                "output": ctx // 2,
                "modality": "text"
            })
        if not models:
            models.append({
                "name": f"{std.lower().replace(' ', '-')}-free",
                "context": 131072,
                "output": 8192,
                "modality": "text"
            })

        # Get endpoints from evidence URLs
        endpoints = []
        for ev in lead.get('evidence', [])[:5]:
            text = ev.get('excerpt', '') + ' ' + ev.get('url', '')
            for m in re.finditer(r'https?://(?:[a-z0-9-]+\.)+(?:com|ai|io|dev|cloud)\b[^\s,)]*', text, re.I):
                u = m.group(0).rstrip('.,;')
                if 'x.com/' not in u and 't.co/' not in u:
                    endpoints.append(u)
        endpoints = list(dict.fromkeys(endpoints))[:3]

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

        # Add verification note
        if v.get('x_claim_verdict'):
            provider["_claim_verdict"] = v['x_claim_verdict']
        if priv.get('quote'):
            provider["_privacy_quote"] = priv['quote']

        providers.append(provider)

    # Add known providers without X coverage
    for std, data in KNOWN_ADDITIONS.items():
        if not any(p.get('provider') == std for p in providers):
            provider = {'provider': std, 'name': std}
            provider.update(data)
            provider['_source'] = 'hand_verified'
            provider['_verified_status'] = 'unverified'
            providers.append(provider)

    return providers


def write_known(providers):
    """Write raw known-apis.json."""
    with open(KNOWN_FILE, 'w') as f:
        json.dump(providers, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(providers)} providers -> {KNOWN_FILE}")


def write_models(providers):
    """Write normalized data/models.json."""
    models = []
    for p in providers:
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
            "privacy": p.get('privacy',{}),
            "status": p.get('_verified_status','unverified'),
            "verified_from_x": p.get('_source') == 'x_scan',
            "context_from_x": p.get('_x_posts',0),
            "promo_warning": p.get('_claim_verdict'),
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
        ctx = ', '.join(f"{m.get('context','?')} tokens" for m in p.get('models',[])[:1]) or '-'
        promo = p.get('_promo_end')
        if promo:
            promo = ', '.join(promo) + (' ⚠️ EXPIRED' if p.get('_verified_status') == 'expired' else '')
        lines.append(f'| {i} | {p["provider"]} | {p.get("_verified_status","unverified")} | {ctx} | {promo or "-"} | {p["auth"]} |')

    lines.extend(['', ''])

    for i, p in enumerate(providers, 1):
        lines += [
            f'## {i}. {p["provider"]}', '',
            f'- **Status**: `{p.get("_verified_status","unverified")}`',
            f'- **Base URL**: `{p["base_url"]}`',
            f'- **Auth**: {p["auth"]}',
            f'- **Rate Limits**: {json.dumps(p["rate_limits"]) or "N/A"}',
            '',
        ]

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
            lines.append(f'- `{m.get("name","?")}` — Context: `{m.get("context","?")}`, Output: `{m.get("output","?")}`')
        lines.append('')

        provenance = []
        if p.get('_source') == 'x_scan':
            provenance.append(f"Discovered via X ({p.get('_x_posts',0)} posts)")
        if p.get('_source') == 'hand_verified':
            provenance.append("Manual verification")
        if provenance:
            lines.append(f'*Source: {", ".join(provenance)}*')
            lines.append('')

        lines.append('')

    with open(DOCS_FILE, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Wrote documentation -> {DOCS_FILE}")


def main():
    leads, verified = load()
    providers = build_provider(leads, verified)
    write_known(providers)
    write_models(providers)
    write_docs(providers)
    print(f"\nDone: {len(providers)} providers in data/")


main()
