# Free LLM API Discovery Project

This project discovers, validates, and documents free LLM APIs. It's designed to be semi-automated and runs in Termux on Android.

## Features

- ✅ Discover free LLM APIs from multiple sources: X-post scanning, **keyless live probes**, and hand-verified records
- ✅ Gather model information (context length, rate limits, privacy)
- ✅ **Confirm endpoints with zero credentials**: the OpenRouter free-model catalog and first-party `/models` endpoints are probed without any API key
- ✅ Track **promo end dates** with countdown labels ("23d left", "ENDED 5d ago", "LAST DAY")
- ✅ Show **privacy badges** confirmed from providers' own terms (trains on prompts / logs prompts / third-party gateway / no-training) - unverified claims are labeled "privacy unconfirmed"
- ✅ Test API usability automatically (`--keyless` mode tests only providers that need no key, safe for CI)
- ✅ Publish a searchable, **filterable** site to GitHub Pages (No key needed / No training / 128K+ context / Live-confirmed / Promo active)
- ✅ Flag hand-verified facts that go **stale** (docs warn once `verified_at` is older than 30 days)
- ✅ Update project settings.json with verified models
- ✅ Track reliability scores for each API

## Project Structure

```
freellm/
├── data/              # Data storage
│   ├── raw/          # Raw API responses
│   ├── verified.json # Hand-verified provider records (+ verified_at dates)
│   ├── x-leads.json  # Raw leads scraped from X (optional source)
│   ├── probes.json   # Keyless live-probe results (auto-generated)
│   ├── models.json   # Structured model database (auto-generated)
│   └── test-results.json # API test results (auto-generated)
├── docs/             # Documentation
│   ├── models.md     # Markdown documentation (auto-generated)
│   └── site/         # Static HTML site (generated, deployed to GitHub Pages)
├── logs/             # Test logs
├── .github/workflows/
│   └── discover-and-publish.yml # Daily cron: keyless discovery + keyless tests + Pages deploy (no secrets)
├── scripts/          # Pipeline scripts
│   ├── gather-llm-apis.sh   # Discover and gather APIs (--skip-x to skip X scan)
│   ├── gather-x-apis.py     # Merge X leads + probes + verified records
│   ├── discover-probes.py   # Keyless live probes (OpenRouter + first-party /models)
│   ├── trust.py             # First-party host allowlist / trust decisions
│   ├── test-apis.sh         # Test API usability (--keyless for CI-safe mode)
│   ├── publish-docs.sh      # Generate docs/models.md + docs/site/
│   └── update-settings.sh   # Update settings.json
├── models/           # Custom model configurations
├── tests/            # Test scripts
├── settings.json     # Project settings (auto-updated)
├── SKILL.md          # Skill documentation
├── README.md         # This file
└── CHANGELOG.md      # Version history
```

## Quick Start

```bash
cd /data/data/com.termux/files/home/freellm

# Step 1: Discover free LLM APIs
#   Add --skip-x to skip the X-post scan (no browse-x login needed;
#   discovery then runs on keyless live probes + verified.json only)
bash scripts/gather-llm-apis.sh --force

# Step 2: Test APIs (optional, for verification)
#   --keyless tests only providers that need no API key - this is what CI runs
bash scripts/test-apis.sh --keyless

# Step 3: Publish documentation
bash scripts/publish-docs.sh

# Step 4: Update project settings
bash scripts/update-settings.sh
```

## Discovery Sources

Three independent sources feed `data/models.json`, in order of trust:

1. **`data/verified.json`** - hand-verified first-party records with a
   `verified_at` date. The docs flag any entry older than 30 days as stale.
2. **Keyless live probes** (`scripts/discover-probes.py` -> `data/probes.json`) -
   runs with **zero credentials**: the OpenRouter free-model catalog
   (`/api/v1/models?max_price=0`, real model ids, context lengths, tool/vision
   flags) and first-party `GET /models` endpoints (Groq, Mistral, Cerebras,
   LLM7, Together, SiliconFlow). A public model list proves the endpoint is
   alive and lists models; a 401/403 is honestly recorded as
   `endpoint_alive_listing_http_N`. Providers discovered this way are marked
   `Discovered via keyless live probe` and a `⚡ live probe` status line.
3. **X-post scanning** (`scripts/x-scan.sh` via the browse-x extension) - the
   original source: free-tier promos, rate-limit claims, promo end dates and
   privacy claims found in posts. Everything from this source is treated as a
   **claim, not a fact**: base URLs are labelled "scraped URL" and never
   receive API keys, privacy chips only appear when confirmed from the
   provider's own terms, and promo countdowns expire out of the "active"
   filter automatically.

Live usability tests (`test-apis.py`) score each provider 0-10 and write
`data/test-results.json`; the site shows the last test date and score on each
card. A public `/models` listing does **not** prove keyless chat works - LLM7's
listing is public but its chat endpoint returns 401 without a key, and it is
scored accordingly.

## Supported Free API Providers

### Verified Providers

| Provider | Auth | Rate Limit | Context | Max Output |
|----------|------|------------|---------|------------|
| Groq | API Key | 30 RPM | 131K | 65K |
| OpenRouter | API Key | 20 RPM | 262K | 262K |
| Mistral AI | API Key | ~1 RPS | 256K | Varies |
| Google Gemini | API Key | 15 RPM | 1M | 65K |
| Cloudflare Workers AI | API Key | 10K neurons/day | Varies | Shared |
| LLM7 | None | 10 RPM | 131K | Varies |
| Kilo | None | 200 req/hr | 1M | 262K |
| OVHcloud | None | 2 RPM | 131K | 32K |
| Z AI | API Key | 1 concurrent | 200K | 131K |
| Aion Labs | API Key | 15 RPM | 131K | 32K |

## Documentation

### Markdown

View the detailed API documentation in `docs/models.md`

### HTML

For a better experience, view the interactive HTML site:
```bash
termux-open docs/site/index.html
```

Each provider card shows its trust signals (verified / probed / scraped URL
warning, promo countdown, last live-test score, privacy chips, verification
age). **Click a card header to expand it**: the details drawer lists the
available models (real ids from live probes, or inferred ids marked as such,
with context lengths), daily limits, the cited privacy detail and ToS quote,
promo claims, and any hand-written `notes` / `source` from verified.json.
Use the search box plus the five filter chips - **No key needed**,
**No training on prompts** (verified terms only), **128K+ context**,
**Live-confirmed**, **Promo active now** - all client-side, combinable.

## API Testing

Run API tests to verify functionality:

```bash
# Test all APIs
bash scripts/test-apis.sh

# Test specific model
bash scripts/test-apis.sh --model "gpt-oss-120b"

# Test limited number
bash scripts/test-apis.sh --limit 5

# Keyless mode only: providers with auth="none" - safe to run on CI
bash scripts/test-apis.sh --keyless
```

Test results are stored in:
- `data/test-results.json` - JSON format
- `logs/test-*.log` - Detailed logs
- `logs/test-summary-*.md` - Summary report

## Settings Configuration

After discovery, update your settings:

```bash
bash scripts/update-settings.sh
```

This will:
1. Read verified models from `data/models.json`
2. Update `settings.json` with working models
3. Create a backup of the previous settings
4. Set the first working model as default

### Manual Settings Update

Edit `settings.json` to add your API keys:

```json
{
  "settings": {
    "api_keys": {
      "GROQ_API_KEY": "your_groq_api_key",
      "OPENROUTER_API_KEY": "your_openrouter_api_key",
      "MISTRAL_API_KEY": "your_mistral_api_key"
    },
    "default_model": "groq-gpt-oss-120b"
  }
}
```

## Security Model

Your API keys are only ever sent to **https** endpoints that are either:

1. listed as `api_base_url` in `data/verified.json` (hand-verified first-party
   endpoints), or
2. in the first-party host allowlist in `scripts/trust.py` (`TRUSTED_HOSTS`).

Base URLs scraped from X posts are treated as **untrusted**: providers whose
only known endpoint is scraped are skipped by `test-apis.sh` with an explicit
message instead of receiving your key, and the docs label them
`scraped from a post`. To enable testing for such a provider, verify its real
endpoint yourself and add an `api_base_url` entry to its `data/verified.json`
record. All content originating from X posts (tweet text, usernames, URLs) is
HTML-escaped before it reaches the generated site.

A scraped URL is only credited as a provider's endpoint if its host actually
plausibly belongs to that provider (`trust.endpoint_affinity()`) - roundup
posts quote many providers' URLs side by side, so "first URL in the post" is
frequently a *different* provider's site (an Ollama lead once quoted
tokenrouter.com). Non-matching URLs are never shown as an endpoint; they stay
visible, muted, as "quoted in posts but not credited". A card with no credible
endpoint simply says **"❓ not confirmed"** - the site never lists a guessed or
unmatched URL as if it were the provider's API. For the same reason a provider
is only marked keyless (`auth: none`) when `data/verified.json` says so; a
*public* `/models` listing does not prove keyless chat - live tests showed
ollama.com, opencode.ai/zen and llm7.io all reject chat without a key while
their listings are open, and those providers are scored and labeled honestly
as a result.

## Privacy Notes

⚠️ **Important**: When using free APIs:

1. **Prompts may be logged** - Most free APIs log your requests for security
2. **Data may be used for training** - Some providers use your data to improve models
3. **Rate limits apply** - Free tiers have strict limits
4. **Terms change** - Free tiers can change without notice
5. **No SLA** - Free APIs have no uptime guarantee

Always review provider terms of service before production use.

## Adding a provider by hand

There is one manual entry point: **`data/verified.json`**. It is the
highest-trust source in the pipeline, which is exactly why hand edits belong
there and nowhere else - its `api_base_url` is the *only* kind of base URL
the test scripts may ever send an API key to (see Security Model). Providers
discovered automatically (X leads, live probes) are never edited by hand;
your verified record overrides or supplies what the scraper cannot know.

**Two cases, same file.**

*Case A - the provider was already discovered (an X lead or a probe exists).*
Add an entry under `"providers"` keyed by the provider's canonical name
(exact name match on the dict key merges it onto that lead). This is how you
fix or supply its endpoint:

```json
"NVIDIA NIM": {
  "verified_at": "2026-09-09",
  "api_base_url": "https://integrate.api.nvidia.com/v1",
  "source": "https://build.nvidia.com/models",
  "auth": "api_key",
  "notes": "Endpoint + auth verified live: GET /v1/models public, chat 401 without key."
}
```

*Case B - it was never discovered and no probe covers it.* The same entry
stands alone; it is emitted as its own card with a `verified` badge:

```json
"MyFavoriteProvider": {
  "display": "My Favorite Provider",
  "verified_at": "2026-09-09",
  "api_base_url": "https://api.myfavorite.example/v1",
  "source": "https://myfavorite.example/pricing",
  "auth": "api_key",
  "models": [{"name": "mf-large", "context": 128000, "output": 8192}],
  "rate_limits": {"requests_per_minute": 30},
  "capabilities": {"tool_calling": true, "vision": false},
  "privacy": {"verdict": "risk_confirmed",
              "detail": "what the ToS does with prompts",
              "quote": "verbatim ToS sentence you actually read"},
  "promo": {"end": "2026-12-31", "claim": "free tier ends Dec 31"}
}
```

Field notes - the honesty rules the fields enforce:

- `verified_at` is **mandatory in spirit**: everything in the entry should
  have been checked against a primary source on that date; entries older
  than 30 days render as `stale` on the site.
- `api_base_url` must be the provider's first-party **https** endpoint.
  Omit it rather than guess - an omitted endpoint renders as
  "❓ not confirmed", a guessed one sends users' keys to a wrong host.
- `auth` may be `"api_key"` (default) or `"none"`. **`"none"` must mean you
  proved keyless chat works** - a public `/models` listing is not proof
  (several providers here have open listings but 401 on chat). Only a
  card's verified record can declare `"none"`.
- `privacy` chips render only from a cited `verdict`
  (`risk_confirmed` / `unknown_third_party`) - copy the `quote` from the
  ToS, don't paraphrase from memory. Omit `privacy` and the card honestly
  says "privacy unconfirmed".
- `"status": "expired"` keeps the entry out of the provider cards (e.g. an
  expired promo) while it stays visible in the site's verification log.
- `models`, `rate_limits`, `capabilities`, `promo`, `display`, `source` and
  `notes` are all optional. Everything on record renders in the card's
  **click-to-expand details drawer** - so when you want to surface any extra
  info about a provider (model list, signup caveats, quota quirks), that
  drawer is where it lands.

**Optional but recommended - make CI re-verify it.** If the provider has a
keyless `GET /models` endpoint, add it to `FIRST_PARTY_PROBES` in
`scripts/discover-probes.py` (and its host to `TRUSTED_HOSTS` in
`scripts/trust.py` if it is genuinely first-party). The daily workflow then
confirms the endpoint is alive and fills in **real model ids** every run -
ground truth no scrape or hand entry can match.

Then rebuild and (optionally) test:

```bash
python3 scripts/discover-probes.py     # keyless, safe to rerun
python3 scripts/gather-x-apis.py
bash scripts/publish-docs.sh
bash scripts/test-apis.sh --provider "NVIDIA NIM"   # only if you set that key
```

## GitHub Actions & Pages

`.github/workflows/discover-and-publish.yml` is a working workflow, checked in:

- **Runs daily** (06:30 UTC) and on manual dispatch.
- **Manual runs have a "skip discovery" toggle** (`skip_discovery`): check it
  and the run skips probes, gather and live tests entirely, building the
  static page straight from the `data/` files already committed to the repo.
  Use it to republish a corrected `verified.json` or card layout without
  waiting on live endpoints. The daily schedule always runs full discovery.
- `gather-llm-apis.sh --skip-x` (no X login in CI; probes + verified.json only),
  then `test-apis.py --keyless` (only `auth=none` providers), then
  `publish-docs.sh`.
- Uploads `docs/site/` with the official Pages actions
  (`configure-pages` / `upload-pages-artifact` / `deploy-pages`) and keeps a
  14-day `data-snapshot` artifact (models/probes/test-results) for history.
- **Uses zero secrets.** No API key ever exists on the runner, so nothing can
  leak; X scraping is skipped rather than run with a logged-in session.

To go live: push the repo to GitHub, then in **Settings → Pages** set *Source*
to **GitHub Actions** and open the **Actions** tab and enable workflows. The
site URL appears on the workflow run summary after the first deploy.

## Dependencies

- **jq** - JSON processor (`pkg install jq`)
- **curl** - HTTP client (usually pre-installed)
- **bash** - Shell interpreter (pre-installed)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and feature requests, please open an issue on GitHub.
