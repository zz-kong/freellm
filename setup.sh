#!/bin/bash
# setup.sh - Setup the free-llm-api-discovery skill
# Run once to initialize the skill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Free LLM API Discovery - Setup ==="
echo ""

# Create directory structure
echo "Creating directory structure..."
mkdir -p "$BASE_DIR/data/raw"
mkdir -p "$BASE_DIR/docs"
mkdir -p "$BASE_DIR/logs"
mkdir -p "$BASE_DIR/scripts"
echo "  ✅ Created directories"

# Copy scripts to main scripts folder
echo ""
echo "Copying scripts..."
cp "$SCRIPT_DIR/scripts/gather-llm-apis.sh" "$SCRIPT_DIR/../"
cp "$SCRIPT_DIR/scripts/test-apis.sh" "$SCRIPT_DIR/../"
cp "$SCRIPT_DIR/scripts/publish-docs.sh" "$SCRIPT_DIR/../"
cp "$SCRIPT_DIR/scripts/update-settings.sh" "$SCRIPT_DIR/../"
chmod +x "$SCRIPT_DIR/../"*.sh
echo "  ✅ Scripts copied"

# Create sample settings.json
echo ""
echo "Creating sample settings.json..."
cat > "$BASE_DIR/../settings.json" << 'EOF'
{
  "version": "1.0.0",
  "models": {
    "groq-gpt-oss-120b": {
      "provider": "Groq",
      "base_url": "https://api.groq.com/openai/v1",
      "context_length": 131072,
      "max_output": 65536,
      "auth": "api_key",
      "rate_limits": {
        "requests_per_minute": 30,
        "requests_per_day": 1000
      },
      "verified": true,
      "added_at": "2026-09-08T00:00:00+00:00"
    },
    "llm7-gpt-oss-20b": {
      "provider": "LLM7",
      "base_url": "https://api.llm7.io/v1",
      "context_length": 131072,
      "max_output": null,
      "auth": "none",
      "rate_limits": {
        "requests_per_minute": 10,
        "requests_per_hour": 60
      },
      "verified": true,
      "added_at": "2026-09-08T00:00:00+00:00"
    }
  },
  "settings": {
    "default_model": "groq-gpt-oss-120b",
    "api_keys": {
      "GROQ_API_KEY": "YOUR_GROQ_API_KEY_HERE",
      "OPENROUTER_API_KEY": "YOUR_OPENROUTER_API_KEY_HERE"
    },
    "rate_limits": {
      "requests_per_minute": 60,
      "requests_per_day": 10000
    },
    "cache": {
      "enabled": true,
      "ttl": 3600
    },
    "logging": {
      "level": "info",
      "save_responses": false
    }
  }
}
EOF
echo "  ✅ Sample settings.json created"

# Create README for the skill
cat > "$BASE_DIR/README.md" << 'EOF'
# Free LLM API Discovery

Semi-automated pipeline to discover, validate, document, and integrate free LLM APIs.

## Quick Start

```bash
# Run the complete pipeline
bash gather-llm-apis.sh --force
bash test-apis.sh
bash publish-docs.sh
bash update-settings.sh
```

## Documentation

- **Models**: `docs/models.md` - Detailed documentation of each API
- **HTML Site**: `docs/site/index.html` - Interactive documentation site
- **Models JSON**: `data/models.json` - Structured model database

## Project Structure

```
freellm/
├── data/              # Data storage
│   ├── raw/          # Raw API responses
│   ├── models.json   # Structured model data
│   └── test-results.json # API test results
├── docs/             # Documentation
│   ├── models.md     # Markdown docs
│   └── site/         # Static HTML site
├── logs/            # Test logs
└── settings.json    # Updated with verified models
```

## API Providers

### Verified Providers
- **Groq** - Fast inference, 30 RPM free tier
- **OpenRouter** - Aggregator of free models
- **LLM7** - Anonymous access, no API key required
- **Kilo** - No key required, 200 req/hr
- **Cloudflare Workers AI** - 10K neurons/day free

### Other Available
- Mistral AI
- Google Gemini
- Z AI
- Aion Labs
- OVHcloud AI Endpoints

## Privacy Notes

1. Most free APIs log prompts for security
2. Some use your data to train models
3. Always check terms of service
4. Don't submit sensitive data to free APIs

## License

MIT
EOF
echo "  ✅ README.md created"

# Make scripts executable
chmod +x "$SCRIPT_DIR/scripts/"*.sh

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Add your API keys to settings.json:"
echo "   - Edit: $BASE_DIR/../settings.json"
echo "   - Update api_keys section with your keys"
echo ""
echo "2. Run the discovery pipeline:"
echo "   bash gather-llm-apis.sh --force"
echo ""
echo "3. Test the APIs:"
echo "   bash test-apis.sh"
echo ""
echo "4. Update project settings:"
echo "   bash update-settings.sh"
echo ""
echo "Documentation:"
echo "  - Markdown: $BASE_DIR/../docs/models.md"
echo "  - HTML: $BASE_DIR/../docs/site/index.html"
