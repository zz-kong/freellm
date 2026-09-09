#!/usr/bin/env python3
"""test-apis.py - Comprehensive API usability testing.

Tests each provider in settings.json for:
  - Auth: does the API key work? What error on invalid key?
  - Basic prompt: chat completion with "Hello"
  - Context limits: prompt size scaling (short → medium → long → max)
  - Rate limiting: rapid requests to find 429 threshold
  - Model info: available models, quantization info
  - Response quality: latency, token counts, error messages

Usage:
<<<<<<< HEAD
  python3 scripts/test-apis.py                      # test all
=======
  python3 scripts/test-apis.py                      # test providers that have keys
  python3 scripts/test-apis.py --all                # also probe key-requiring providers without keys
  python3 scripts/test-apis.py --keyless            # ONLY providers that need no key (CI-safe)
>>>>>>> 382d5fc (minor modifications)
  python3 scripts/test-apis.py --limit 5            # first 5 only
  python3 scripts/test-apis.py --provider Groq      # one provider
  python3 scripts/test-apis.py --provider Groq --context 50000  # custom context
  python3 scripts/test-apis.py --context-limits short medium long  # which context tests to run
<<<<<<< HEAD
"""
import json, os, sys, time, urllib.request, urllib.error, urllib.parse
=======

Security: API keys are only sent to base_urls verified in data/verified.json
or listed in trust.TRUSTED_HOSTS - never to URLs scraped from X posts.
"""
import json, os, re, sys, time, urllib.request, urllib.error, urllib.parse
>>>>>>> 382d5fc (minor modifications)
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from pathlib import Path

<<<<<<< HEAD
=======
sys.path.insert(0, str(Path(__file__).resolve().parent))
import trust

>>>>>>> 382d5fc (minor modifications)
BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_FILE = BASE_DIR / "settings.json"
MODELS_FILE = BASE_DIR / "data/models.json"
RESULTS_FILE = BASE_DIR / "data/test-results.json"
LOGS_DIR = BASE_DIR / "logs"

<<<<<<< HEAD
=======
# {provider_slug: api_base_url} from data/verified.json - authoritative endpoints.
VERIFIED_BASES = trust.verified_bases(str(BASE_DIR))

def choice_text(choice):
    """Response text of a chat-completion choice (message.content; falls back
    to legacy text completions shape)."""
    msg = choice.get("message") or {}
    return msg.get("content") or choice.get("text") or ""

>>>>>>> 382d5fc (minor modifications)
# Test parameters (override with --context-limits short medium long etc)
CONTEXT_SIZES = ["short", "medium", "long", "max"]  # short=100, medium=1000, long=10000, max=50000
RATE_LIMIT_BATCH = 10  # requests to send in rapid burst
RATE_LIMIT_WAIT = 2    # seconds between bursts

# System prompt for context testing (content-free filler)
FILLER = "The quick brown fox jumps over the lazy dog. " * 5

def log(msg):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}")

<<<<<<< HEAD
=======
def env_candidates(key):
    """Env var names that could hold the key stored under `key` in settings.json.

    api_keys entries may be written as 'groq', 'GROQ', 'google-gemini' or the
    legacy 'GROQ_API_KEY' form; accept any spelling of the same name.
    """
    base = re.sub(r'[^A-Za-z0-9]+', '_', key).strip('_').upper()
    names = [base + "_API_KEY"]
    if base.endswith("_API"):
        names.append(base + "_KEY")
    if key.upper().endswith("_API_KEY"):
        names.append(key.upper())
    return names

>>>>>>> 382d5fc (minor modifications)
def load_settings():
    if not SETTINGS_FILE.exists():
        log("ERROR: settings.json not found")
        sys.exit(1)
    s = json.load(open(SETTINGS_FILE))
    # Read API keys from env vars (overrides settings.json)
    for key in s.get("api_keys", {}):
<<<<<<< HEAD
        env = f"{key}_API_KEY"
        val = os.environ.get(env, "")
        if val:
            s["api_keys"][key] = val
=======
        for env in env_candidates(key):
            val = os.environ.get(env, "")
            if val:
                s["api_keys"][key] = val
                break
>>>>>>> 382d5fc (minor modifications)
    return s

def make_request(url, data, headers=None, timeout=30):
    """Make HTTP request, return (status_code, response_text, headers_dict, error)."""
    if headers is None:
        headers = {}
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    req.add_header('Content-Type', 'application/json')
    # Add User-Agent to avoid Cloudflare bot detection (e.g. Groq, OpenRouter)
    if 'User-Agent' not in req.headers:
        req.add_header('User-Agent', 'freellm-test/1.0')
    
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed_ms = (time.time() - start) * 1000
<<<<<<< HEAD
            return resp.status, resp.read().decode('utf-8'), dict(resp.headers), elapsed_ms
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.time() - start) * 1000
        body = e.read().decode('utf-8') if e.fp else ""
        return e.code, body, dict(e.headers), elapsed_ms
=======
            hdrs = {k.lower(): v for k, v in dict(resp.headers).items()}
            return resp.status, resp.read().decode('utf-8'), hdrs, elapsed_ms
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.time() - start) * 1000
        body = e.read().decode('utf-8') if e.fp else ""
        hdrs = {k.lower(): v for k, v in dict(e.headers).items()}
        return e.code, body, hdrs, elapsed_ms
>>>>>>> 382d5fc (minor modifications)
    except Exception as e:
        return None, str(e), {}, 0

# Note: Cloudflare Workers AI uses `X-Auth-Token` header instead of Bearer.
# For other providers, all use standard Bearer auth via Authorization header.
#
def test_auth(provider_name, base_url, api_key, auth_type, model_name=None):
    """Test authentication behavior."""
    results = {
        "provider": provider_name,
        "auth_type": auth_type,
        "key_configured": bool(api_key),
        "valid_key_status": None,
        "invalid_key_status": None,
        "no_key_status": None,
        "key_error_messages": {},
    }
    
    # Valid key test
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    code, body, hdrs, ms = make_request(f"{base_url}/chat/completions", {
        "model": model_name or "qwen/qwen3.8-27b", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5
    }, headers)
    results["valid_key_status"] = code
    if code and 400 <= code < 500:
        try:
            err = json.loads(body).get("error", {}).get("message", "")
            results["key_error_messages"]["valid"] = err[:200]
        except:
            results["key_error_messages"]["valid"] = body[:200]
    results["valid_key_latency_ms"] = round(ms, 1)
    
    # Invalid key test (if we have a key)
    if api_key:
        headers_bad = {"Authorization": "Bearer INVALID_KEY_TEST_12345"}
        code, body, hdrs, ms = make_request(f"{base_url}/chat/completions", {
            "model": model_name or "qwen/qwen3.8-27b", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5
        }, headers_bad)
        results["invalid_key_status"] = code
        if code:
            try:
                err = json.loads(body).get("error", {}).get("message", "")
                results["key_error_messages"]["invalid"] = err[:200]
            except:
                results["key_error_messages"]["invalid"] = body[:200]
        results["invalid_key_latency_ms"] = round(ms, 1)
    
    # No key test
    code, body, hdrs, ms = make_request(f"{base_url}/chat/completions", {
        "model": model_name or "qwen/qwen3.8-27b", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5
    }, {})
    results["no_key_status"] = code
    if code:
        try:
            err = json.loads(body).get("error", {}).get("message", "")
            results["key_error_messages"]["no_key"] = err[:200]
        except:
            results["key_error_messages"]["no_key"] = body[:200]
    results["no_key_latency_ms"] = round(ms, 1)
    
    return results

def test_basic_prompt(provider_name, base_url, api_key, model_name="gpt-oss-120b"):
    """Test basic chat completion."""
    results = {"provider": provider_name}
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    
    code, body, hdrs, ms = make_request(f"{base_url}/chat/completions", {
        "model": model_name,
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 20,
    }, headers)
    
    results["basic_prompt"] = {
        "status": code,
        "latency_ms": round(ms, 1),
        "has_choices": code == 200 and '"choices"' in body,
        "error": None,
        "response_length": 0,
        "model_name": None,
        "usage": None,
    }
    
    if code == 200:
        try:
            resp = json.loads(body)
            choices = resp.get("choices", [])
            if choices:
<<<<<<< HEAD
                results["basic_prompt"]["response_length"] = len(choices[0].get("text", ""))
=======
                results["basic_prompt"]["response_length"] = len(choice_text(choices[0]))
>>>>>>> 382d5fc (minor modifications)
                results["basic_prompt"]["model_name"] = resp.get("model")
                results["basic_prompt"]["usage"] = resp.get("usage")
            else:
                results["basic_prompt"]["error"] = "No choices in response"
        except Exception as e:
            results["basic_prompt"]["error"] = str(e)[:200]
    elif code:
        try:
            err = json.loads(body).get("error", {}).get("message", "")
            results["basic_prompt"]["error"] = err[:200]
        except:
            results["basic_prompt"]["error"] = body[:200]
    
    return results

def test_context_limits(provider_name, base_url, api_key, model_name="gpt-oss-120b", sizes=None):
    """Test with progressively larger prompts."""
    if sizes is None:
        sizes = CONTEXT_SIZES
    
    results = {"provider": provider_name, "tests": []}
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    
    # Build prompt sizes
    size_map = {"short": 100, "medium": 1000, "long": 10000, "max": 50000}
    
    for size_label in sizes:
        word_count = size_map.get(size_label, 100)
        prompt_text = FILLER * (word_count // 10)  # Each filler block is ~10 words
        
        code, body, hdrs, ms = make_request(f"{base_url}/chat/completions", {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt_text}],
            "max_tokens": 5,
        }, headers)
        
        test_result = {
            "size_label": size_label,
            "approx_words": word_count,
            "status": code,
            "latency_ms": round(ms, 1),
            "worked": code == 200,
            "error": None,
            "response_tokens": 0,
        }
        
        if code == 200:
            try:
                resp = json.loads(body)
                choices = resp.get("choices", [])
                if choices:
                    test_result["worked"] = True
<<<<<<< HEAD
                    test_result["response_tokens"] = len(choices[0].get("text", ""))
=======
                    test_result["response_tokens"] = len(choice_text(choices[0]))
>>>>>>> 382d5fc (minor modifications)
                else:
                    test_result["worked"] = False
                    test_result["error"] = "No choices"
            except:
                test_result["worked"] = False
                test_result["error"] = "Invalid JSON response"
        elif code == 400:
            try:
                err = json.loads(body).get("error", {}).get("message", "")
                test_result["worked"] = False
                test_result["error"] = err[:200]
            except:
                test_result["worked"] = False
                test_result["error"] = body[:200]
        else:
            test_result["worked"] = False
            test_result["error"] = f"HTTP {code}"
        
        results["tests"].append(test_result)
    
    # Determine max working context
    for test in reversed(results["tests"]):
        if test["worked"]:
            results["max_working_context"] = test["approx_words"]
            break
    else:
        results["max_working_context"] = 0
    
    return results

def test_rate_limits(provider_name, base_url, api_key, model_name="gpt-oss-120b", batch=RATE_LIMIT_BATCH, wait=RATE_LIMIT_WAIT):
    """Test rate limiting by sending rapid requests."""
    results = {"provider": provider_name, "batches": [], "first_429_at": None}
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    
    success = 0
<<<<<<< HEAD
    first_429 = None
    first_429_batch = None
    
=======
    total_sent = 0
    first_429 = None
    first_429_batch = None

>>>>>>> 382d5fc (minor modifications)
    for batch_idx in range(5):  # Max 5 batches
        batch_results = []
        for req_idx in range(batch):
            code, body, hdrs, ms = make_request(f"{base_url}/chat/completions", {
                "model": model_name,
                "messages": [{"role": "user", "content": f"req {batch_idx*batch + req_idx}"}],
                "max_tokens": 5,
            }, headers)
            
<<<<<<< HEAD
=======
            total_sent += 1
>>>>>>> 382d5fc (minor modifications)
            batch_results.append({
                "request": batch_idx * batch + req_idx,
                "status": code,
                "latency_ms": round(ms, 1),
                "success": code == 200,
            })
<<<<<<< HEAD
            
            if code == 429 and first_429 is None:
                first_429 = batch_idx * batch + req_idx
                first_429_batch = batch_idx + 1
                # Read Retry-After if available
                retry_after = hdrs.get("retry-after", [None])[0]
                batch_results[-1]["retry_after"] = retry_after
=======

            if code == 429 and first_429 is None:
                first_429 = batch_idx * batch + req_idx
                first_429_batch = batch_idx + 1
                # Read Retry-After if available (header values are strings in
                # our lowercased headers dict)
                if hdrs.get("retry-after"):
                    batch_results[-1]["retry_after"] = hdrs["retry-after"]
>>>>>>> 382d5fc (minor modifications)
        
        success_this = sum(1 for r in batch_results if r["success"])
        success += success_this
        results["batches"].append({
            "batch": batch_idx + 1,
            "requests": batch_results,
            "success": success_this,
            "total": batch,
        })
        
        if first_429 is not None:
            break
        
        if batch_idx < 4:
            time.sleep(wait)
    
    results["total_success"] = success
<<<<<<< HEAD
    results["first_429_at_request"] = first_429
    results["first_429_at_batch"] = first_429_batch
    results["success_rate"] = round(success / min(batch * 5, success + 1), 3)
=======
    results["total_sent"] = total_sent
    results["first_429_at_request"] = first_429
    results["first_429_at_batch"] = first_429_batch
    results["success_rate"] = round(success / total_sent, 3) if total_sent else 0
>>>>>>> 382d5fc (minor modifications)
    
    return results

def test_model_info(provider_name, base_url, api_key):
    """Check models endpoint for available models and quantization info."""
    results = {"provider": provider_name, "models": []}
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    headers['User-Agent'] = 'freellm-test/1.0'
    
    # /models is GET, not POST
    url = f"{base_url}/models"
    req = urllib.request.Request(url, headers=headers, method='GET')
    
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            elapsed_ms = (time.time() - start) * 1000
            body = resp.read().decode('utf-8')
            code = resp.status
            hdrs = dict(resp.headers)
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.time() - start) * 1000
        body = e.read().decode('utf-8') if e.fp else ""
        code = e.code
        hdrs = dict(e.headers)
    except Exception as e:
        code = None
        body = str(e)
        hdrs = {}
        elapsed_ms = (time.time() - start) * 1000
    
    results["status"] = code
    results["latency_ms"] = round(elapsed_ms, 1)
    
    if code == 200:
        try:
            data = json.loads(body)
            models_list = data.get("data", [])
            if not models_list and isinstance(data, list):
                models_list = data
            
            for m in models_list[:20]:  # Limit to 20 models
                model_info = {
                    "id": m.get("id", m.get("model", "")),
                    "object": m.get("object", ""),
                    "owned_by": m.get("owned_by", ""),
                    "created": m.get("created", ""),
                }
                # Look for quantization info in ID or metadata
                model_id = model_info["id"].lower()
                if any(q in model_id for q in ["q4", "q5", "q8", "f16", "f32", "int8", "int4", "bf16", "fp8", "fp16"]):
                    model_info["quantization"] = [q for q in ["q4", "q5", "q8", "f16", "f32", "int8", "int4", "bf16", "fp8", "fp16"] if q in model_id][0]
                results["models"].append(model_info)
            
            results["total_models"] = len(models_list)
        except Exception as e:
            results["parse_error"] = str(e)[:200]
    elif code:
        try:
            err = json.loads(body).get("error", {}).get("message", "")
            results["error"] = err[:200]
        except:
            results["error"] = body[:200]
    
    return results

<<<<<<< HEAD
def get_api_key(provider_key, provider_data, settings):
    """Get API key for provider from env var or settings.json.
    
    Env var names use uppercase provider key: GROQ_API_KEY, GEMINI_API_KEY, etc.
    Settings.json api_keys uses provider_key directly, but some mappings differ.
    """
    # Map provider_key -> api_keys key (some differ due to naming conventions)
    KEY_MAP = {
        'google-gemini': 'google-gemini',  # api_keys key
        'gemini': 'google-gemini',          # alternate
        'mistral-ai': 'mistral-ai',
        'mistral': 'mistral-ai',
        'cloudflare-workers-ai': 'cloudflare-workers-ai',
        'cloudflare': 'cloudflare-workers-ai',
    }
    
    # Try env var first (uppercase provider key + _API_KEY)
    env_var = f"{provider_key.upper()}_API_KEY"
    val = os.environ.get(env_var, "")
    if val:
        return val
    
    # Fall back to settings.json api_keys section
    api_keys = settings.get("api_keys", {})
    
    # Try provider_key directly
    val = api_keys.get(provider_key, "")
    if val:
        return val
    
    # Try mapped keys
    for mapped_key, api_key_name in KEY_MAP.items():
        if provider_key == mapped_key or mapped_key in provider_key:
            val = api_keys.get(api_key_name, "")
            if val:
                return val
    
    return ""

def run_test_for_provider(settings, provider_key, provider_data, context_sizes=None, rate_batch=None, rate_wait=None):
    """Run all tests for a single provider.
    
    Skips providers that don't have API keys configured (unless auth='none').
    """
    base_url = provider_data.get("base_url", "")
    if not base_url or "PLACEHOLDER" in base_url or "example" in base_url:
        return {
            "provider": provider_key,
            "skipped": True,
            "reason": f"Invalid base_url: {base_url}"
        }
    
    api_key = get_api_key(provider_key, provider_data, settings)
    auth_type = provider_data.get("auth", "api_key")
    model_name = provider_data.get("model_name", "gpt-oss-120b")
    
=======
def _norm_key(s):
    """Canonical form for provider/api-key names: alphanumerics only, lowercase,
    with a trailing 'api key' suffix removed. 'GROQ_API_KEY', 'GROQ', 'groq' all
    normalize to 'groq'."""
    return re.sub(r'[^a-z0-9]+', '', (s or '').lower()).removesuffix('apikey')

# Alternate spellings of the same provider, in normalized form.
KEY_ALIASES = {
    'gemini': 'googlegemini',
    'googlegemini': 'googlegemini',
    'mistral': 'mistralai',
    'mistralai': 'mistralai',
    'cloudflare': 'cloudflareworkersai',
    'cloudflareworkersai': 'cloudflareworkersai',
    'zai': 'zai',
    'z.ai': 'zai',
}

# Env var names users actually set, per normalized provider (the mechanical
# NAME_API_KEY derivation can't guess e.g. GEMINI_API_KEY for google-gemini).
ENV_NAMES = {
    'groq': ['GROQ_API_KEY'],
    'googlegemini': ['GEMINI_API_KEY', 'GOOGLE_GEMINI_API_KEY', 'GOOGLEAISTUDIO_API_KEY'],
    'openrouter': ['OPENROUTER_API_KEY'],
    'mistralai': ['MISTRAL_API_KEY', 'MISTRALAI_API_KEY'],
    'cloudflareworkersai': ['CLOUDFLARE_API_KEY', 'CLOUDFLARE_WORKERS_API_KEY'],
    'cerebras': ['CEREBRAS_API_KEY'],
    'siliconflow': ['SILICONFLOW_API_KEY'],
    'ollamacloud': ['OLLAMA_API_KEY', 'OLLAMACLOUD_API_KEY'],
    'llm7': ['LLM7_API_KEY'],
}

def _lookup_key(api_keys, needle_norm):
    """Case/format-insensitive lookup in the api_keys dict."""
    for k, v in api_keys.items():
        if v and _norm_key(k) == needle_norm:
            return v
    return ""

def get_api_key(provider_key, provider_data, settings):
    """Get API key for provider from env var or settings.json.

    Env var names use uppercase provider key: GROQ_API_KEY, GEMINI_API_KEY, etc.
    settings.json api_keys entries are matched case- and format-insensitively,
    so 'groq', 'GROQ' and legacy 'GROQ_API_KEY' all resolve for provider 'groq'.
    """
    norm = _norm_key(provider_key)
    wanted = {norm}
    if norm in KEY_ALIASES:
        wanted.add(KEY_ALIASES[norm])

    # Try env vars first: known names for this provider, then the mechanical
    # NAME_API_KEY derivation (plus aliases).
    names = list(ENV_NAMES.get(norm, []))
    names += [re.sub(r'[^A-Z0-9]+', '_', name.upper()) + "_API_KEY" for name in sorted(wanted)]
    for env_var in names:
        val = os.environ.get(env_var, "")
        if val:
            return val

    # Fall back to settings.json api_keys section
    api_keys = settings.get("api_keys", {})
    for name in sorted(wanted):
        val = _lookup_key(api_keys, name)
        if val:
            return val
    # ... and the raw (un-aliased) provider key form as a last resort
    return _lookup_key(api_keys, norm) or ""

def pick_model(model_info, configured):
    """Choose which model id to use for chat requests.

    The `configured` name comes from data/models.json and may be synthesized
    (e.g. '<provider>-free') rather than a real model id. Prefer it only if
    the provider's own /models list confirms it; otherwise pick a real id from
    that list (free-tier ids first). Falls back to `configured` when /models
    is unavailable.
    """
    ids = [m.get("id") for m in model_info.get("models", []) if m.get("id")]
    if not ids:
        return configured, "configured (models endpoint unavailable)"
    if configured in ids:
        return configured, "configured (confirmed by /models)"
    free = [i for i in ids if "free" in i.lower()]
    if free:
        return free[0], "auto-selected from /models (free tier)"
    return ids[0], "auto-selected from /models"

def run_test_for_provider(settings, provider_key, provider_data, context_sizes=None, rate_batch=None, rate_wait=None):
    """Run all tests for a single provider.

    Skips providers that don't have API keys configured (unless auth='none').
    Security: credentials are only ever sent to a base_url that is either
    verified in data/verified.json or on trust.TRUSTED_HOSTS. Scraped URLs
    (data/models.json base_url comes from X posts) are never trusted with keys.
    """
    display = provider_data.get("display_name", provider_key)
    raw_url = provider_data.get("base_url", "")
    base_url, trusted, base_src = trust.trusted_base(
        provider_data.get("provider", provider_key), raw_url, VERIFIED_BASES)

    if not base_url or "PLACEHOLDER" in base_url or "example" in base_url:
        return {
            "provider": provider_key,
            "display_name": display,
            "skipped": True,
            "reason": f"Invalid base_url: {base_url}"
        }
    if not trust.host_of(base_url):
        return {
            "provider": provider_key,
            "display_name": display,
            "skipped": True,
            "reason": f"Refusing non-https base_url: {base_url}"
        }

    api_key = get_api_key(provider_key, provider_data, settings)
    auth_type = provider_data.get("auth", "api_key")

    if auth_type != "none" and not trusted:
        return {
            "provider": provider_key,
            "display_name": display,
            "skipped": True,
            "reason": (f"Security: base_url host '{trust.host_of(base_url)}' is not a verified "
                       f"first-party endpoint (scraped from X posts). Add an 'api_base_url' entry "
                       f"for this provider to data/verified.json or trust.TRUSTED_HOSTS to test it."),
            "base_url": base_url,
        }

>>>>>>> 382d5fc (minor modifications)
    # Skip providers that require auth but have no key
    if auth_type != "none" and not api_key:
        return {
            "provider": provider_key,
<<<<<<< HEAD
            "display_name": provider_data.get("display_name", provider_key),
            "skipped": True,
            "reason": "API key not configured (no env var or settings.json entry)",
            "env_var": f"{provider_key.upper()}_API_KEY",
        }
    
    results = {
        "provider": provider_key,
        "display_name": provider_data.get("display_name", provider_key),
        "base_url": base_url,
        "auth": auth_type,
        "tests": {}
    }
    
    # 1. Auth test
    log(f"  Testing auth for {provider_key}...")
    results["tests"]["auth"] = test_auth(provider_key, base_url, api_key, provider_data.get("auth", "api_key"), model_name)
    
    # 2. Basic prompt
    log(f"  Testing basic prompt for {provider_key}...")
    results["tests"]["basic_prompt"] = test_basic_prompt(provider_key, base_url, api_key, model_name)
    
    # 3. Context limits
    log(f"  Testing context limits for {provider_key}...")
    results["tests"]["context_limits"] = test_context_limits(provider_key, base_url, api_key, model_name, context_sizes)
    
=======
            "display_name": display,
            "skipped": True,
            "reason": "API key not configured (no env var or settings.json entry)",
            "env_var": (ENV_NAMES.get(_norm_key(provider_key))
                        or [re.sub(r'[^A-Z0-9]+', '_', _norm_key(provider_key).upper()) + "_API_KEY"])[0],
        }

    # Untrusted + keyless: probe without any credentials, and never attach one.
    if not trusted:
        api_key = ""

    results = {
        "provider": provider_key,
        "display_name": display,
        "base_url": base_url,
        "base_url_source": base_src,
        "auth": auth_type,
        "tests": {}
    }

    # 0. Model info first (GET /models, no chat request) - its list of real
    #    model ids drives which model every chat test below will target.
    log(f"  Checking model info for {provider_key}...")
    results["tests"]["model_info"] = test_model_info(provider_key, base_url, api_key)
    model_name, model_src = pick_model(results["tests"]["model_info"],
                                       provider_data.get("model_name") or "gpt-oss-120b")
    results["model_used"] = model_name
    results["model_source"] = model_src
    log(f"  Model for tests: {model_name} [{model_src}]")

    # 1. Auth test
    log(f"  Testing auth for {provider_key}...")
    results["tests"]["auth"] = test_auth(provider_key, base_url, api_key, provider_data.get("auth", "api_key"), model_name)

    # 2. Basic prompt
    log(f"  Testing basic prompt for {provider_key}...")
    results["tests"]["basic_prompt"] = test_basic_prompt(provider_key, base_url, api_key, model_name)

    # 3. Context limits
    log(f"  Testing context limits for {provider_key}...")
    results["tests"]["context_limits"] = test_context_limits(provider_key, base_url, api_key, model_name, context_sizes)

>>>>>>> 382d5fc (minor modifications)
    # 4. Rate limits (only if auth works)
    if results["tests"]["auth"].get("valid_key_status") == 200:
        log(f"  Testing rate limits for {provider_key}...")
        results["tests"]["rate_limits"] = test_rate_limits(provider_key, base_url, api_key, model_name, rate_batch or RATE_LIMIT_BATCH, rate_wait or RATE_LIMIT_WAIT)
    else:
        results["tests"]["rate_limits"] = {"skipped": True, "reason": "Auth not working (status {})".format(results["tests"]["auth"].get("valid_key_status"))}
    
<<<<<<< HEAD
    # 5. Model info
    log(f"  Checking model info for {provider_key}...")
    results["tests"]["model_info"] = test_model_info(provider_key, base_url, api_key)
    
=======
>>>>>>> 382d5fc (minor modifications)
    # Compute usability score
    usability = 0
    max_usability = 5  # auth, basic, context, rate, model
    
    if results["tests"]["auth"].get("valid_key_status") == 200:
        usability += 1
    if results["tests"]["basic_prompt"].get("basic_prompt", {}).get("has_choices"):
        usability += 1
    if results["tests"]["context_limits"].get("tests"):
        max_ctx = results["tests"]["context_limits"].get("max_working_context", 0)
        if max_ctx >= 100:
            usability += 1
        else:
            usability += 0.5
    if results["tests"]["rate_limits"].get("total_success", 0) > 5:
        usability += 1
    if results["tests"]["model_info"].get("models"):
        usability += 1
    
    results["usability_score"] = round(usability / max_usability * 10, 1)
    results["usability_label"] = "✅ Excellent" if usability >= 4.5 else "🟢 Good" if usability >= 3.5 else "🟡 Fair" if usability >= 2.5 else "🟠 Poor" if usability >= 1.5 else "❌ Broken"
    
    return results

def main():
    context_sizes = CONTEXT_SIZES
    rate_batch = RATE_LIMIT_BATCH
    rate_wait = RATE_LIMIT_WAIT
    limit = None
    provider_filter = None
<<<<<<< HEAD
    
=======
    test_all = False
    keyless_only = False

>>>>>>> 382d5fc (minor modifications)
    # Parse args
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1]); i += 2
        elif args[i] == "--provider" and i + 1 < len(args):
            provider_filter = args[i + 1]; i += 2
        elif args[i] == "--context-limits" and i + 1 < len(args):
            context_sizes = args[i + 1].split(); i += 2
        elif args[i] == "--context-limit" and i + 1 < len(args):
            context_sizes = [args[i + 1]]; i += 2
        elif args[i] == "--rate-batch" and i + 1 < len(args):
            rate_batch = int(args[i + 1]); i += 2
        elif args[i] == "--rate-wait" and i + 1 < len(args):
            rate_wait = int(args[i + 1]); i += 2
<<<<<<< HEAD
=======
        elif args[i] == "--all":
            test_all = True; i += 1
        elif args[i] == "--keyless":
            keyless_only = True; i += 1
>>>>>>> 382d5fc (minor modifications)
        elif args[i] == "--help":
            print(__doc__); sys.exit(0)
        else:
            print(f"Unknown arg: {args[i]}"); sys.exit(1)
    
    # Load data
    settings = load_settings()
    
    # Get providers to test
    providers_to_test = []
    
    if provider_filter:
        if provider_filter in settings.get("models", {}):
            providers_to_test = [provider_filter]
        else:
            print(f"Provider '{provider_filter}' not found in settings.json")
            print(f"Available: {list(settings.get('models', {}).keys())}")
            sys.exit(1)
    else:
        providers_to_test = list(settings.get("models", {}).keys())
        if limit:
            providers_to_test = providers_to_test[:limit]
    
    # Auto-detect which providers have API keys configured
    providers_with_keys = []
    providers_without_keys = []
    
    for pk in providers_to_test:
        pd = settings["models"][pk]
        api_key = get_api_key(pk, pd, settings)
        auth_type = pd.get("auth", "api_key")
        if (api_key and auth_type != "none") or auth_type == "none":
            providers_with_keys.append(pk)
        else:
            providers_without_keys.append(pk)
    
<<<<<<< HEAD
    # Default behavior: only test providers that have keys
    # Use --all to test everything (will fail for missing keys)
    should_test = providers_with_keys if not providers_without_keys else providers_with_keys
    
    if providers_without_keys and not provider_filter:
=======
    # Default behavior: only test providers that have keys (or need none).
    # --all also probes key-requiring providers with no key (no-key behavior).
    # --keyless tests ONLY auth=none providers: no credentials exist in the
    # process, which makes it the safe mode for CI/GitHub Actions.
    if keyless_only:
        should_test = [pk for pk in providers_to_test
                       if settings["models"][pk].get("auth", "api_key") == "none"]
    else:
        should_test = providers_to_test if test_all else providers_with_keys

    if providers_without_keys and not provider_filter and not test_all and not keyless_only:
>>>>>>> 382d5fc (minor modifications)
        print(f"Skipping {len(providers_without_keys)} providers without API keys:")
        for pk in providers_without_keys:
            env = f"{pk.upper()}_API_KEY"
            print(f"  - {pk} (set {env} or add to settings.json)")
        print()
    
<<<<<<< HEAD
=======
    if not should_test and keyless_only:
        print("No keyless providers configured (auth=none) - nothing to test.")
        sys.exit(0)

>>>>>>> 382d5fc (minor modifications)
    if not should_test:
        print("ERROR: No providers have API keys configured.")
        print("Set keys via environment variables:")
        print("  export GROQ_API_KEY=\"gsk-...\"")
        print("  export GEMINI_API_KEY=\"...\"")
        print()
        print("Or configure in settings.json under api_keys:")
        print('  "groq": "gsk-...", "gemini": "...", "openrouter": "sk-or-..."')
        sys.exit(1)
    
<<<<<<< HEAD
    log(f"Testing {len(should_test)} providers with keys: {', '.join(should_test)}")
=======
    log(f"Testing {len(should_test)} {'keyless' if keyless_only else 'keyed'} providers: {', '.join(should_test)}")
>>>>>>> 382d5fc (minor modifications)
    log(f"Context sizes: {context_sizes}")
    log(f"Rate limit: {rate_batch} req/batch, {rate_wait}s between")
    log("")
    
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    all_results = []
    
    for i, provider_key in enumerate(should_test, 1):
        provider_data = settings["models"][provider_key]
        log(f"\n[{i}/{len(should_test)}] {provider_data.get('display_name', provider_key)}")
        
        result = run_test_for_provider(settings, provider_key, provider_data, context_sizes, rate_batch, rate_wait)
        all_results.append(result)
        
        # Print quick summary
        if not result.get("skipped"):
            score = result.get("usability_score", 0)
            label = result.get("usability_label", "?")
            basic = result["tests"].get("basic_prompt", {}).get("basic_prompt", {})
            ctx = result["tests"].get("context_limits", {}).get("max_working_context", "?")
            
            # Get the main failure reason for quick debugging
            basic_err = basic.get("error", "")
            auth_err = result["tests"].get("auth", {}).get("key_error_messages", {}).get("valid", "")
            
            summary_parts = [
                f"  Score: {score}/10 {label}",
                f"  Basic: {'✅' if basic.get('has_choices') else '❌'} | Latency: {basic.get('latency_ms', '?')}ms | Model: {basic.get('model_name', '?')}",
            ]
            if basic_err or auth_err:
                # Clean up common error messages
                err_msg = basic_err or auth_err
                if "1010" in str(err_msg):
                    err_msg = "Cloudflare WAF block (403/1010) - check API key in Groq dashboard"
                elif "401" in str(err_msg) or "invalid" in str(err_msg).lower():
                    err_msg = "Auth failed - key may be invalid"
                elif "429" in str(err_msg):
                    err_msg = "Rate limited"
                else:
                    err_msg = str(err_msg)[:80]
                summary_parts.append(f"  Error: {err_msg}")
            # Check for Cloudflare WAF block specifically
            if "1010" in str(basic_err) or "1010" in str(auth_err):
                summary_parts.append("  Groq blocks requests from urllib. Use curl or the groq Python package.")
            elif "403" in str(basic_err) or "403" in str(auth_err):
                summary_parts.append("  Server 403. Check your API key and provider docs for auth format.")
            
            print("\n".join(summary_parts))
        else:
            print(f"  SKIPPED: {result.get('reason', '?')}")
    
    # Save results
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    output = {
        "test_run": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "providers_tested": len(all_results),
            "context_sizes": context_sizes,
            "rate_limit_params": {"batch": rate_batch, "wait_seconds": rate_wait},
        },
        "results": all_results,
    }
    
    # Save JSON
    json.dump(output, open(RESULTS_FILE, 'w'), indent=2, ensure_ascii=False)
    log(f"\nResults saved: {RESULTS_FILE}")
    
    # Generate markdown report
    md_lines = [
        "# API Test Results",
        f"\n**Generated**: {output['test_run']['timestamp']}\n",
        f"**Providers tested**: {len(all_results)}",
        f"**Context sizes**: {', '.join(context_sizes)}",
        f"**Rate limit**: {rate_batch} req/batch, {rate_wait}s between\n",
        "## Summary\n",
        "| Provider | Score | Label | Auth OK | Basic | Context Max | Rate Success |",
        "|----------|-------|-------|---------|-------|-------------|--------------|",
    ]
    
    for r in all_results:
        if r.get("skipped"):
            md_lines.append(f"| {r.get('display_name', r.get('provider'))} | - | SKIPPED | - | - | - | - |")
            continue
        
        t = r.get("tests", {})
        auth = t.get("auth", {}).get("valid_key_status")
        basic = t.get("basic_prompt", {}).get("basic_prompt", {})
        ctx = t.get("context_limits", {}).get("max_working_context", 0)
        rate = t.get("rate_limits", {}).get("total_success", 0)
        
        md_lines.append(
            f"| {r.get('display_name', r.get('provider'))} "
            f"| {r.get('usability_score', 0)}/10 "
            f"| {r.get('usability_label', '?')} "
            f"| {auth} "
            f"| {'✅' if basic.get('has_choices') else '❌'} "
            f"| {ctx} words "
            f"| {rate} |"
        )
    
    # Add detailed results
    md_lines.append("\n## Detailed Results\n")
    for r in all_results:
        if r.get("skipped"):
            continue
        md_lines.append(f"### {r.get('display_name', r['provider'])}\n")
        
        # Auth
        auth = r["tests"].get("auth", {})
        md_lines.append(f"**Auth**: key_configured={auth.get('key_configured')} | valid={auth.get('valid_key_status')} | invalid={auth.get('invalid_key_status')} | no_key={auth.get('no_key_status')}")
        if auth.get('key_error_messages'):
            for k, v in auth['key_error_messages'].items():
                md_lines.append(f"  - {k}: {v[:100]}")
        md_lines.append("")
        
        # Basic
        bp = r["tests"].get("basic_prompt", {}).get("basic_prompt", {})
        md_lines.append(f"**Basic prompt**: status={bp.get('status')} | latency={bp.get('latency_ms')}ms | choices={'✅' if bp.get('has_choices') else '❌'} | model={bp.get('model_name')} | error={bp.get('error')}")
        usage = bp.get('usage')
        if usage:
            md_lines.append(f"  Usage: {json.dumps(usage)}")
        md_lines.append("")
        
        # Context
        ctx = r["tests"].get("context_limits", {})
        md_lines.append(f"**Context limits**: max_working={ctx.get('max_working_context')} words")
        for t in ctx.get("tests", []):
            md_lines.append(f"  - {t['size_label']}: {'✅' if t['worked'] else '❌'} ({t['approx_words']} words) | latency={t['latency_ms']}ms | error={t.get('error')}")
        md_lines.append("")
        
        # Rate limits
        rl = r["tests"].get("rate_limits", {})
        md_lines.append(f"**Rate limits**: first_429@request={rl.get('first_429_at_request')} | batch={rl.get('first_429_at_batch')} | total_success={rl.get('total_success')} | success_rate={rl.get('success_rate')}")
        md_lines.append("")
        
        # Model info
        mi = r["tests"].get("model_info", {})
        md_lines.append(f"**Models**: status={mi.get('status')} | count={mi.get('total_models', '?')} | latency={mi.get('latency_ms')}ms")
        if mi.get("models"):
            for m in mi["models"][:10]:
                q = m.get("quantization", "")
                md_lines.append(f"  - {m['id']} (quant: {q or 'N/A'})")
        md_lines.append("")
        
        # Usability
        md_lines.append(f"**Usability**: {r.get('usability_score', 0)}/10 {r.get('usability_label', '')}")
        md_lines.append("")
    
    report_file = LOGS_DIR / f"test-summary-{timestamp}.md"
    open(report_file, 'w').write('\n'.join(md_lines))
    log(f"Markdown report: {report_file}")
    
    # Quick summary
<<<<<<< HEAD
    scores = [r.get('usability_score', 0) for r in all_results if not r.get('skipped')]
    if scores:
        log(f"\nAverage usability: {sum(scores)/len(scores):.1f}/10")
        best = max(all_results, key=lambda r: r.get('usability_score', 0))
        worst = min(all_results, key=lambda r: r.get('usability_score', 0))
=======
    tested = [r for r in all_results if not r.get('skipped')]
    scores = [r.get('usability_score', 0) for r in tested]
    if scores:
        log(f"\nAverage usability: {sum(scores)/len(scores):.1f}/10")
        best = max(tested, key=lambda r: r.get('usability_score', 0))
        worst = min(tested, key=lambda r: r.get('usability_score', 0))
>>>>>>> 382d5fc (minor modifications)
        log(f"Best: {best.get('display_name', best['provider'])} ({best['usability_score']})")
        log(f"Worst: {worst.get('display_name', worst['provider'])} ({worst['usability_score']})")


main()

# Quick note: context tests use word approximation, not actual tokens.
# 1 token ≈ 0.75 words for English text. A "50000 word" prompt is ~66K tokens,
# which will likely exceed most free tier limits and trigger 429s or 400s.
