#!/usr/bin/env python3
"""trust.py - single source of truth for which API hosts may receive credentials.

data/models.json base URLs are extracted from X posts (see gather-x-apis.py)
and can therefore be ANY URL - a marketing page, a third-party reseller, or a
domain an attacker controls. This module decides which URLs are safe:

  1. `api_base_url` entries in data/verified.json (manually verified, cited)
     are authoritative and OVERRIDE the scraped base_url.
  2. Otherwise the host must be on TRUSTED_HOSTS (first-party API hosts).
  3. HTTPS only. An untrusted host is never sent an Authorization header;
     keyless (auth=none) providers may still be probed over https without keys.

Add providers to TRUSTED_HOSTS or - better - to verified.json with a citation.
"""
import json
import os
import re
from urllib.parse import urlparse

# First-party OpenAI-compatible API hosts seen in this project's data.
# Keep this list to official API hosts only (no resellers, no console pages).
TRUSTED_HOSTS = {
    "api.groq.com",
    "openrouter.ai",
    "api.mistral.ai",
    "generativelanguage.googleapis.com",
    "api.cerebras.ai",
    "api.siliconflow.cn",
    "api.llm7.io",
    "api.z.ai",
    "open.bigmodel.cn",
    "api.together.xyz",
    "integrate.api.nvidia.com",
    # added 2026-09-09: confirmed live first-party OpenAI-compatible /models
    "ollama.com",
    "opencode.ai",
}

# Words in a provider name that say nothing about whose host a URL is.
_GENERIC_TOKENS = {"ai", "api", "cloud", "labs", "free", "app", "io", "zen"}


def endpoint_affinity(provider_name, url):
    """True if `url`'s host plausibly belongs to `provider_name`.

    X roundup posts quote many providers' URLs side by side, so "first URL in
    the post" is often a DIFFERENT provider's site (an Ollama lead quoting
    tokenrouter.com, a Qwen lead quoting ai.google.dev). Only credit a scraped
    URL as an endpoint when the host shares a distinctive token with the
    provider name; generic tokens (ai, api, cloud, ...) never match on their
    own, and substring matches need >=4 chars to avoid 'ovh' in 'ovhcloud'-style
    false negatives. Equality matches are exact, so 'z' matches api.z.ai.
    """
    host = host_of(url) or ""
    host_tokens = {t for t in host.split(".") if t}
    name_tokens = [t for t in re.split(r"[^a-z0-9]+", str(provider_name).lower()) if t]
    for pt in name_tokens:
        if pt in _GENERIC_TOKENS:
            continue
        for ht in host_tokens:
            if pt == ht or (len(pt) >= 4 and pt in ht) or (len(ht) >= 4 and ht in pt):
                return True
    return False


def host_of(url):
    """Lowercased host of `url` if it is a usable https URL, else None."""
    try:
        u = urlparse(url or "")
    except ValueError:
        return None
    if u.scheme != "https":
        return None
    host = (u.hostname or "").lower()
    return host or None


def provider_slug(name):
    return (name or "").lower().replace(" ", "-")


def verified_bases(base_dir):
    """{provider_slug: api_base_url} from data/verified.json (missing file -> {})."""
    path = os.path.join(base_dir, "data", "verified.json")
    out = {}
    try:
        data = json.load(open(path))
    except (OSError, ValueError):
        return out
    for std, v in (data.get("providers") or {}).items():
        url = (v or {}).get("api_base_url")
        if url:
            out[provider_slug(std)] = url
    return out


def trusted_base(provider_name, scraped_url, bases=None):
    """Pick the URL to use and whether it may receive credentials.

    Returns (url, trusted, source) where source is one of
    'verified', 'trusted_host', 'unverified'.
    """
    bases = bases or {}
    vurl = bases.get(provider_slug(provider_name))
    if vurl:
        return vurl, True, "verified"
    if host_of(scraped_url) in TRUSTED_HOSTS:
        return scraped_url, True, "trusted_host"
    return scraped_url, False, "unverified"
