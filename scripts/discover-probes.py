#!/usr/bin/env python3
"""discover-probes.py - keyless live discovery against public model catalogs.

The X scan yields *leads* (claims in posts). This script yields *ground truth*
from the horse's mouth, with zero credentials and zero quota:

  1. OpenRouter's public catalog endpoint supports `?max_price=0` and returns
     the models that are free right now, with real ids and context lengths.
  2. First-party `/models` endpoints on the trust.TRUSTED_HOSTS list answer
     unauthenticated GETs for some providers (Groq, LLM7, ...). A 200 gives
     real model ids; a 401 still proves the endpoint is alive.

Writes data/probes.json for gather-x-apis.py to merge (real model ids replace
synthesized ones, base_urls get provenance 'trusted_probe'). SECURITY: this
script never reads or sends API keys - every request is unauthenticated by
design, and only first-party hosts listed below are contacted.

Usage: python3 scripts/discover-probes.py [--timeout SECONDS]
"""
import json
import os
import sys
import urllib.request
import urllib.error
import datetime

BASE = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
OUT = os.path.join(BASE, 'data', 'probes.json')
UA = 'Mozilla/5.0 (compatible; freellm-discovery/1.0; open-data project)'

# (canonical provider name, models endpoint). Keep to first-party hosts on
# scripts/trust.py TRUSTED_HOSTS - these URLs are stored as trusted base urls.
# Google Gemini /models requires a key, so it is deliberately absent.
FIRST_PARTY_PROBES = [
    ("Groq",            "https://api.groq.com/openai/v1/models"),
    ("Mistral AI",      "https://api.mistral.ai/v1/models"),
    ("Cerebras",        "https://api.cerebras.ai/v1/models"),
    ("LLM7",            "https://api.llm7.io/v1/models"),
    ("Together AI",     "https://api.together.xyz/v1/models"),
    ("SiliconFlow",     "https://api.siliconflow.cn/v1/models"),
    # names must match provider names used by X leads so the merge attaches
    ("Ollama Cloud",    "https://ollama.com/v1/models"),
    ("OpenCode Zen",    "https://opencode.ai/zen/v1/models"),
    ("NVIDIA NIM",      "https://integrate.api.nvidia.com/v1/models"),
]

OPENROUTER_FREE = "https://openrouter.ai/api/v1/models?max_price=0"
OPENROUTER_BASE = "https://openrouter.ai/api/v1"

MAX_IDS = 12  # ids stored per provider - enough for docs, keeps files small


def get_json(url, timeout):
    req = urllib.request.Request(url, headers={'User-Agent': UA,
                                               'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8', 'replace'))


def openai_ids(payload):
    """Model ids from an OpenAI-style /models response (both field spellings)."""
    items = payload.get('data') or payload.get('models') or []
    ids = []
    for it in items:
        if isinstance(it, str):
            ids.append(it)
        elif isinstance(it, dict):
            mid = it.get('id') or it.get('_id') or it.get('name')
            if mid:
                ids.append(str(mid))
    return ids


def probe_first_party(name, url, timeout):
    """Unauthenticated GET. 200 = public model list; 401/403 = endpoint alive,
    listing private; anything else = error. No credentials are ever attached."""
    entry = {"base_url": url.rsplit('/models', 1)[0], "checked_at": utcnow()}
    try:
        ids = openai_ids(get_json(url, timeout))
        entry["status"] = "public_model_list"
        entry["model_ids"] = ids[:MAX_IDS]
        entry["model_count"] = len(ids)
    except urllib.error.HTTPError as e:
        entry["status"] = f"endpoint_alive_listing_http_{e.code}" if e.code in (401, 403) else f"http_{e.code}"
    except Exception as e:
        entry["status"] = f"error: {type(e).__name__}"
    return entry


def probe_openrouter(timeout):
    """Free models currently listed on OpenRouter, with real ids + context."""
    entry = {"base_url": OPENROUTER_BASE, "checked_at": utcnow()}
    try:
        data = get_json(OPENROUTER_FREE, timeout).get('data') or []
        free = []
        for m in data:
            pr = m.get('pricing') or {}
            try:
                is_free = float(pr.get('prompt', 1)) == 0 and float(pr.get('completion', 1)) == 0
            except (TypeError, ValueError):
                is_free = False
            if is_free and m.get('id'):
                arch = m.get('architecture') or {}
                modality = str(arch.get('modality') or '')
                free.append({"id": str(m['id']),
                             "name": str(m.get('name') or m['id']),
                             "context": m.get('context_length'),
                             # capabilities confirmed live from the catalog
                             "tool_calling": 'tools' in (m.get('supported_parameters') or []),
                             "vision": 'image' in modality.split('->')[0]})
        entry["status"] = "ok"
        entry["free_models"] = free
    except urllib.error.HTTPError as e:
        entry["status"] = f"http_{e.code}"
    except Exception as e:
        entry["status"] = f"error: {type(e).__name__}"
    return entry


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')


def main():
    timeout = 20
    args = sys.argv[1:]
    if '--timeout' in args:
        timeout = int(args[args.index('--timeout') + 1])

    print("=== Keyless discovery probes (no credentials sent) ===")
    out = {"generated_at": utcnow(),
           "note": "Unauthenticated live probes of public model catalogs. "
                   "model_ids are REAL ids confirmed live; free_models are "
                   "listed at price 0 as of checked_at.",
           "sources": {}}

    orr = probe_openrouter(timeout)
    n = len(orr.get('free_models', []))
    print(f"  OpenRouter free catalog: {orr['status']}"
          + (f" ({n} free models)" if n else ""))
    out["sources"]["OpenRouter"] = orr

    for name, url in FIRST_PARTY_PROBES:
        r = probe_first_party(name, url, timeout)
        detail = (f" ({r.get('model_count', '?')} models)"
                  if r['status'] == 'public_model_list' else "")
        print(f"  {name:<12} {url.rsplit('/v1', 1)[0]:<42} {r['status']}{detail}")
        out["sources"][name] = r

    ok = sum(1 for s in out["sources"].values()
             if s.get('status') in ('ok', 'public_model_list'))
    if ok == 0:
        # Network down / all endpoints failing: still write (stale marker) but
        # exit 3 so gather-llm-apis.sh can warn without aborting the pipeline.
        print("WARNING: no probe succeeded - data/probes.json marks everything stale")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"Wrote {len(out['sources'])} probe results -> {OUT}")
    sys.exit(0 if ok else 3)


main()
