#!/usr/bin/env python3
"""update-settings.py - Merge verified models into settings.json.

Reads data/models.json and data/verified.json, writes settings.json with:
- A "models" section keyed by provider
- API keys section (from env vars or .env file)
- Global settings

Only includes verified providers (not expired ones).
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
MODELS_FILE = os.path.join(BASE, 'data', 'models.json')
VERIFIED_FILE = os.path.join(BASE, 'data', 'verified.json')
SETTINGS_FILE = os.path.join(BASE, 'settings.json')


def load_settings():
    """Load existing settings or create empty."""
    if os.path.exists(SETTINGS_FILE):
        backup = SETTINGS_FILE + '.backup.' + __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
        os.rename(SETTINGS_FILE, backup)
        print(f'Backup: {backup}')
    return {
        "version": "2.0.0",
        "models": {},
        "api_keys": {},
        "settings": {
            "default_model": None,
            "rate_limits": {
                "requests_per_minute": 60,
                "requests_per_day": 10000
            },
            "cache": {
                "enabled": True,
                "ttl": 3600
            },
            "logging": {
                "level": "info",
                "save_responses": False
            }
        }
    }


def build_models(models_data, verified_data):
    """Build settings models section from verified data + X leads."""
    providers = {}
    
    # First, add verified models from data/models.json
    for m in models_data:
        provider_name = m.get('provider', '')
        status = m.get('status', 'unverified')
        
        # Skip expired providers
        if status == 'expired':
            print(f'  SKIP (expired): {provider_name}')
            continue
        
        # Build model config
        model_entry = {
            "provider": provider_name,
            "base_url": m.get('base_url', ''),
            "auth": m.get('auth', 'api_key'),
            "verified_from_x": m.get('verified_from_x', False),
            "x_post_count": m.get('context_from_x', 0),
            "context_length": 131072,  # default
            "rate_limits": m.get('rate_limits', {}),
            "claims_verdict": m.get('promo_warning'),
        }
        
        # Add context from first model
        for model in m.get('models', []):
            ctx = model.get('context')
            if ctx:
                model_entry['context_length'] = ctx
                model_entry['model_name'] = model.get('name', 'free')
                break
        
        providers[provider_name.lower().replace(' ', '-')] = {
            "display_name": provider_name,
            **model_entry
        }
    
    # Second, add verification info from verified.json
    verified = verified_data.get('providers', {})
    for std_name, vdata in verified.items():
        key = std_name.lower().replace(' ', '-')
        if key in providers:
            providers[key]['verification'] = vdata.get('status', 'unverified')
        elif std_name:
            providers[key] = {
                "display_name": std_name,
                "provider": std_name,
                "base_url": "",
                "auth": "api_key",
                "verified_from_x": False,
                "x_post_count": 0,
                "context_length": 0,
                "rate_limits": {},
                "verification": vdata.get('status', 'unverified')
            }
    
    return providers


def build_api_keys():
    """Build API keys section from environment variables."""
    keys = {}
    env_prefixes = {
        'GROQ': 'GROQ_API_KEY',
        'GEMINI': 'GEMINI_API_KEY',
        'OPENROUTER': 'OPENROUTER_API_KEY',
        'MISTRAL': 'MISTRAL_API_KEY',
        'CLOUDFLARE': 'CLOUDFLARE_API_KEY',
        'CEREBRAS': 'CEREBRAS_API_KEY',
        'SILICONFLOW': 'SILICONFLOW_API_KEY',
    }
    for display, env_var in env_prefixes.items():
        val = os.environ.get(env_var, '')
        if val and len(val) > 3 and not val.startswith('YOUR_') and not val.startswith('sk-placeholder'):
            keys[display] = val
        else:
            keys[display] = ''  # placeholder - user must fill in
    return keys


def main():
    if not os.path.exists(MODELS_FILE):
        print(f'ERROR: {MODELS_FILE} not found. Run x-scan.sh and gather-x-apis.py first.')
        sys.exit(1)
    
    models_data = json.load(open(MODELS_FILE))
    verified_data = json.load(open(VERIFIED_FILE)) if os.path.exists(VERIFIED_FILE) else {'providers': {}}
    
    print(f'Loaded {len(models_data)} models from data/models.json')
    print(f'Loaded {len(verified_data.get("providers", {}))} verified records')
    
    # Load existing settings
    settings = load_settings()
    
    # Build models section
    providers = build_models(models_data, verified_data)
    settings['models'] = providers
    print(f'Added {len(providers)} providers to settings')
    
    # Build API keys
    settings['api_keys'] = build_api_keys()
    
    # Set default to first verified provider
    for key, p in providers.items():
        if p.get('verification') in ('verified', 'active'):
            settings['settings']['default_model'] = key
            break
    
    # Write
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    print(f'Written: {SETTINGS_FILE}')
    
    # Summary
    verified = [p for p in providers.values() if p.get('verification') in ('verified', 'active')]
    unverified = [p for p in providers.values() if p.get('verification') not in ('verified', 'active')]
    print(f'\nSummary:')
    print(f'  Verified: {len(verified)} - {", ".join(p["display_name"] for p in verified)}')
    print(f'  Unverified: {len(unverified)}')
    print(f'\nNext steps:')
    print(f'  1. Set your API keys in {SETTINGS_FILE} under "api_keys"')
    print(f'  2. Or set env vars: export GROQ_API_KEY=sk-... GEMINI_API_KEY=...')
    print(f'  3. Run: bash scripts/test-apis.sh')


main()
