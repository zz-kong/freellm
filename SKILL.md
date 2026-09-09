---
name: free-llm-api-discovery
description: Discover, validate, and document free LLM APIs with GitHub Pages publishing and settings.json integration
allowed-tools:
  - Bash(bash scripts/gather-llm-apis.sh)
  - Bash(bash scripts/test-apis.sh)
  - Bash(bash scripts/publish-docs.sh)
  - Bash(bash scripts/update-settings.sh)
---

# Free LLM API Discovery

A semi-automated pipeline to discover, validate, document, and integrate free LLM APIs.

## Overview

This skill provides tools to:

1. **Discover** free LLM APIs from various sources (web search, x.pcstyle.dev for relevant posts)
2. **Gather** model information (context length, rate limits, pricing, privacy implications)
3. **Test** API usability automatically in pi
4. **Publish** results to GitHub Pages or Cloudflare Pages
5. **Update** project settings.json with verified models

## Setup

No additional dependencies required. Uses standard bash tools and pi's built-in capabilities.

## Usage

### 1. Discover and Gather Free LLM APIs

```bash
bash scripts/gather-llm-apis.sh [--force]
```

Options:
- `--force` - Re-download and re-process all data

This will:
- Search for free LLM API information using web search
- Extract model details from documentation
- Store raw data in `data/raw/`
- Generate structured `data/models.json`
- Create documentation in `docs/models.md`

### 2. Test API Usability

```bash
bash scripts/test-apis.sh [--model <name>] [--limit <n>]
```

Options:
- `--model <name>` - Test a specific model by name
- `--limit <n>` - Test only first N models

This will:
- Test each API endpoint for availability
- Measure response time
- Test context window limits
- Test tool calling capability (if supported)
- Generate test results in `data/test-results.json`
- Log test output in `logs/test-<timestamp>.log`

### 3. Publish Documentation

```bash
bash scripts/publish-docs.sh [--destination <github|cloudflare>]
```

Options:
- `--destination github` - Publish to GitHub Pages
- `--destination cloudflare` - Publish to Cloudflare Pages (default)

This will:
- Build documentation site
- Generate index of all models
- Create searchable model database
- Deploy to selected destination

### 4. Update Settings

```bash
bash scripts/update-settings.sh [--settings <path>]
```

Options:
- `--settings <path>` - Path to settings.json (default: `../settings.json`)

This will:
- Parse verified models from `data/models.json`
- Update settings.json with working models
- Maintain existing configuration
- Backup original settings

## Complete Workflow

Run the full pipeline:

```bash
# Step 1: Gather all available free LLM APIs
bash scripts/gather-llm-apis.sh --force

# Step 2: Test each API's usability
bash scripts/test-apis.sh

# Step 3: Publish documentation
bash scripts/publish-docs.sh

# Step 4: Update project settings
bash scripts/update-settings.sh
```

## Output Structure

```
freellm/
├── data/
│   ├── raw/              # Raw API responses
│   ├── models.json       # Structured model database
│   └── test-results.json # API test results
├── docs/
│   ├── models.md         # Markdown documentation
│   └── index.html        # Static HTML site
├── logs/
│   └── test-*.log        # Test execution logs
├── settings.json         # Updated with verified models
└── README.md             # This documentation
```

## Model Information Captured

For each model, the system gathers:

- **Provider**: Company or organization
- **Model Name**: Exact model identifier
- **Context Length**: Input context window (tokens)
- **Max Output**: Maximum output length (tokens)
- **Rate Limits**: Requests per minute/day
- **Cost**: Free tier details
- **Authentication**: Required (API key, OAuth, none)
- **Capabilities**: Tool calling, vision, audio, video
- **Privacy**: Data usage policy, retention, etc.
- **Testing**: Verified working status, latency, reliability score

## Privacy Considerations

When testing free APIs:

1. **Do not submit sensitive data** - Most free tiers log prompts
2. **Check terms of service** - Some providers claim rights to use your data
3. **Rate limit yourself** - Avoid triggering anti-abuse systems
4. **Use test prompts** - Standardized prompts for fair comparison

## Troubleshooting

### API Tests Failing

- Check rate limits - you may have been throttled
- Verify API keys are correctly set
- Some APIs require registration even if "free"

### Documentation Not Updating

- Ensure `docs/` directory is writable
- Check GitHub Pages/Cloudflare configuration
- Verify `settings.json` path is correct

### Connection Errors

- Check network connectivity
- Some APIs may be temporarily unavailable
- Consider using a VPN if region-locked

## Advanced Usage

### Custom API Endpoints

Add custom endpoints to `data/custom-apis.json`:

```json
[
  {
    "name": "Custom API",
    "base_url": "https://custom.example.com/v1",
    "api_key_env": "CUSTOM_API_KEY",
    "models": ["custom-model-1", "custom-model-2"]
  }
]
```

### Filter by Capability

Filter models by specific capabilities:

```bash
# Models with tool calling
jq '.[] | select(.capabilities.tool_calling == true)' data/models.json

# Models with context > 100K
jq '.[] | select(.context_length > 100000)' data/models.json

# Free models with no auth
jq '.[] | select(.auth == "none" and .cost == "free")' data/models.json
```

## CI/CD Integration

This skill is designed for automation. Add to your workflow:

```yaml
name: Free LLM API Discovery

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM
  workflow_dispatch:      # Manual trigger

jobs:
  discover-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Discover APIs
        run: bash scripts/gather-llm-apis.sh
      - name: Test APIs
        run: bash scripts/test-apis.sh
      - name: Publish Docs
        run: bash scripts/publish-docs.sh
      - name: Update Settings
        run: bash scripts/update-settings.sh
      - name: Commit Changes
        run: |
          git config user.name 'github-actions[bot]'
          git config user.email 'github-actions[bot]@users.noreply.github.com'
          git add .
          git commit -m 'Update free LLM API data' || echo 'No changes'
          git push
```

## Contributing

Found a new free LLM API? Add it to `data/custom-apis.json` and run the pipeline to verify and document it.
