# Free LLM API Discovery - Quick Start

## Get Started in 5 Minutes

```bash
cd /data/data/com.termux/files/home/freellm
bash scripts/gather-llm-apis.sh --force
cat docs/models.md | head -80
```

## What You Get

- **10+ Free LLM APIs** with full details
- **Context lengths**, rate limits, capabilities
- **Privacy implications** for each provider
- **Markdown documentation** in docs/models.md
- **Project settings** ready to use

## Quick Commands

| Command | Purpose |
|---------|---------|
| `bash scripts/gather-llm-apis.sh --force` | Discover all free APIs |
| `cat docs/models.md` | View documentation |
| `bash scripts/test-apis.sh --limit 3` | Test first 3 APIs |
| `bash scripts/update-settings.sh` | Update project settings |
| `bash scripts/publish-docs.sh` | Publish to web |

## Top 3 Free APIs

### 1. Groq (Fastest)
- **Speed**: Ultra-fast LPU inference
- **Rate**: 30 RPM, 1000 RPD
- **Context**: 131K tokens
- **Auth**: API key (free)

### 2. LLM7 (No Key)
- **Speed**: 10 RPM
- **Auth**: None required
- **Context**: 131K tokens
- **Best for**: Quick testing

### 3. Kilo (Anonymous)
- **Speed**: 200 req/hr
- **Auth**: None required
- **Context**: 1M tokens
- **Best for**: Long context

## Example Usage

```bash
# Groq (with API key)
curl https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -d '{"model":"gpt-oss-120b","messages":[{"role":"user","content":"Hello"}]}'

# LLM7 (no API key)
curl https://api.llm7.io/v1/chat/completions \
  -d '{"model":"gpt-oss:20b","messages":[{"role":"user","content":"Hello"}]}'
```

## File Locations

| File | Description |
|------|-------------|
| `docs/models.md` | API documentation |
| `data/models.json` | API database |
| `settings.json` | Project config |
| `README.md` | Full documentation |

## What's Next?

1. Add your API keys to `settings.json`
2. Test the APIs you need
3. Publish documentation
4. Start using free LLMs!

---

**Ready to go!** 🚀

For full docs: `cat COMPLETE_SUMMARY.md`
