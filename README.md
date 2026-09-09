# Free LLM API Discovery Project

This project discovers, validates, and documents free LLM APIs. It's designed to be semi-automated and runs in Termux on Android.

## Features

- ✅ Discover free LLM APIs from multiple providers
- ✅ Gather model information (context length, rate limits, privacy)
- ✅ Test API usability automatically
- ✅ Publish documentation to GitHub Pages or Cloudflare Pages
- ✅ Update project settings.json with verified models
- ✅ Generate searchable HTML documentation
- ✅ Track reliability scores for each API

## Project Structure

```
freellm/
├── data/              # Data storage
│   ├── raw/          # Raw API responses
│   ├── models.json   # Structured model database (auto-generated)
│   └── test-results.json # API test results (auto-generated)
├── docs/             # Documentation
│   ├── models.md     # Markdown documentation (auto-generated)
│   └── site/         # Static HTML site (generated)
├── logs/             # Test logs
├── scripts/          # Pipeline scripts
│   ├── gather-llm-apis.sh   # Discover and gather APIs
│   ├── test-apis.sh         # Test API usability
│   ├── publish-docs.sh      # Publish to GitHub Pages/Cloudflare Pages
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
bash scripts/gather-llm-apis.sh --force

# Step 2: Test APIs (optional, for verification)
bash scripts/test-apis.sh

# Step 3: Publish documentation
bash scripts/publish-docs.sh

# Step 4: Update project settings
bash scripts/update-settings.sh
```

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

## API Testing

Run API tests to verify functionality:

```bash
# Test all APIs
bash scripts/test-apis.sh

# Test specific model
bash scripts/test-apis.sh --model "gpt-oss-120b"

# Test limited number
bash scripts/test-apis.sh --limit 5
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

## Privacy Notes

⚠️ **Important**: When using free APIs:

1. **Prompts may be logged** - Most free APIs log your requests for security
2. **Data may be used for training** - Some providers use your data to improve models
3. **Rate limits apply** - Free tiers have strict limits
4. **Terms change** - Free tiers can change without notice
5. **No SLA** - Free APIs have no uptime guarantee

Always review provider terms of service before production use.

## Custom APIs

To add custom API providers:

1. Create `data/custom-apis.json`
2. Add your provider configuration:

```json
[
  {
    "provider": "MyCustomAPI",
    "name": "My Custom API",
    "base_url": "https://api.example.com/v1",
    "models": [
      {"name": "custom-model-1", "context": 100000, "output": 10000, "modality": "text"}
    ],
    "auth": "api_key",
    "free_tier": true,
    "rate_limits": {"requests_per_minute": 100},
    "capabilities": {"tool_calling": true, "vision": false}
  }
]
```

3. Run `bash scripts/gather-llm-apis.sh`

## CI/CD Integration

Add this to your `.github/workflows/`:

```yaml
name: Free LLM API Discovery

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

jobs:
  discover-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup
        run: |
          curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
          sudo apt-get install -y nodejs jq
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
