# Free LLM APIs

- generated: `2026-09-09T04:04:18.109354+00:00`
- providers: `16`

> ⚠️ Only providers with **verified_from_x = true** have been confirmed via X post evidence.
> Providers with **status = expired** should not be listed as active free tiers.

| # | Provider | Status | Context | Promo End | Auth |
|---|----------|--------|---------|-----------|------|
| 1 | Ollama Cloud | unverified | unknown | - | api_key |
| 2 | Google Gemini | active | 131000 tokens | - | api_key |
| 3 | OpenCode Zen | unverified | 1000000 tokens | - | api_key |
| 4 | OpenRouter | unverified | 262144 tokens | - | api_key |
| 5 | Groq | unverified | 131000 tokens | - | api_key |
| 6 | Mistral AI | unverified | unknown | - | api_key |
| 7 | Cloudflare Workers AI | unverified | unknown | - | api_key |
| 8 | Z AI | unverified | unknown | - | api_key |
| 9 | Qwen | unverified | unknown | - | api_key |
| 10 | Cerebras | unverified | unknown | - | api_key |
| 11 | DeepSeek | unverified | unknown | - | api_key |
| 12 | Sarvam AI | unverified | unknown | - | api_key |
| 13 | NVIDIA NIM | unverified | unknown | - | api_key |
| 14 | SambaNova | unverified | unknown | - | api_key |
| 15 | Hugging Face | unverified | unknown | - | api_key |
| 16 | LLM7 | probed | unknown | - | api_key |


## 1. Ollama Cloud

- **Status**: `unverified`
- **Base URL**: `https://ollama.com/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:08+00:00): `public_model_list` — real model ids confirmed

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `kimi-k2.6` — Context: `unknown`, Output: `unknown`
- `kimi-k2.7-code` — Context: `unknown`, Output: `unknown`
- `nemotron-3-ultra` — Context: `unknown`, Output: `unknown`
- `gemma4:31b` — Context: `unknown`, Output: `unknown`
- `nemotron-3-super` — Context: `unknown`, Output: `unknown`
- `deepseek-v4-flash:0731` — Context: `unknown`, Output: `unknown`
- `glm-5.3-flash` — Context: `unknown`, Output: `unknown`
- `gpt-oss:120b` — Context: `unknown`, Output: `unknown`

*Source: Discovered via X (16 posts)*


## 2. Google Gemini

- **Status**: `active`
- **Base URL**: `https://generativelanguage.googleapis.com/v1beta/openai`


- **Auth**: api_key
- **Rate Limits**: {}

- **Verification age**: manually verified 2026-09-08

> **X claim verdict**: The X replies warning that the free tier trains on your prompts are substantially CORRECT under the Unpaid Services terms; the originating X post's 'permanent free tier, no billing required' framing omits this trade-off.

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**
- Human reviewers: **Yes**
- Regional exception: In the EEA, Switzerland and the UK the Paid-Services data terms apply even to the unpaid quota

### Models
- `google-gemini-free` — Context: `131000`, Output: `65500` _(inferred id - confirm via /models)_

*Source: Discovered via X (19 posts)*


## 3. OpenCode Zen

- **Status**: `unverified`
- **Base URL**: `https://opencode.ai/zen/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:09+00:00): `public_model_list` — real model ids confirmed

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `claude-fable-5` — Context: `1000000`, Output: `unknown`
- `claude-fable-5-1` — Context: `1000000`, Output: `unknown`
- `claude-opus-5` — Context: `1000000`, Output: `unknown`
- `claude-opus-4-8` — Context: `1000000`, Output: `unknown`
- `claude-opus-4-7` — Context: `1000000`, Output: `unknown`
- `claude-opus-4-6` — Context: `1000000`, Output: `unknown`
- `claude-opus-4-5` — Context: `1000000`, Output: `unknown`
- `claude-sonnet-5` — Context: `1000000`, Output: `unknown`

*Source: Discovered via X (6 posts)*


## 4. OpenRouter

- **Status**: `unverified`
- **Base URL**: `https://openrouter.ai/api/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:06+00:00): `ok` — real model ids confirmed

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `nex-agi/nex-n2.5-mini:free` — Context: `262144`, Output: `unknown`
- `nex-agi/nex-n2.5-pro:free` — Context: `262144`, Output: `unknown`
- `inclusionai/ling-3.0-flash-sante:free` — Context: `262144`, Output: `unknown`
- `inclusionai/ling-3.0-flash-fin:free` — Context: `262144`, Output: `unknown`
- `dots-studio/dots-3-note-preview:free` — Context: `512000`, Output: `unknown`
- `liquid/lfm-2.5-2.6b:free` — Context: `65536`, Output: `unknown`
- `nvidia/nemotron-3.5-lightning:free` — Context: `1000000`, Output: `unknown`
- `thinkingmachines/inkling-small:free` — Context: `1048576`, Output: `unknown`

*Source: Discovered via X (11 posts)*


## 5. Groq

- **Status**: `unverified`
- **Base URL**: `https://api.groq.com/openai/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:06+00:00): `endpoint_alive_listing_http_401`

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `groq-free` — Context: `131000`, Output: `65500` _(inferred id - confirm via /models)_

*Source: Discovered via X (5 posts)*


## 6. Mistral AI

- **Status**: `unverified`
- **Base URL**: `https://api.mistral.ai/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:06+00:00): `endpoint_alive_listing_http_401`

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `mistral-ai-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_

*Source: Discovered via X (3 posts)*


## 7. Cloudflare Workers AI

- **Status**: `unverified`
- **Base URL**: `unknown - not confirmed from any evidence`

  > Other URLs quoted in the posts did not match this provider's name and are NOT credited as its endpoint: `https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key`
- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `cloudflare-workers-ai-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_

*Source: Discovered via X (7 posts)*


## 8. Z AI

- **Status**: `unverified`
- **Base URL**: `unknown - not confirmed from any evidence`


- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `z-ai-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_

*Source: Discovered via X (2 posts)*


## 9. Qwen

- **Status**: `unverified`
- **Base URL**: `unknown - not confirmed from any evidence`

  > Other URLs quoted in the posts did not match this provider's name and are NOT credited as its endpoint: `https://ai.google.dev/gemini-api/docs/pricing`, `https://console.groq.com/`
- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `qwen-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_

*Source: Discovered via X (3 posts)*


## 10. Cerebras

- **Status**: `unverified`
- **Base URL**: `https://api.cerebras.ai/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:07+00:00): `endpoint_alive_listing_http_403`

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `cerebras-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_

*Source: Discovered via X (2 posts)*


## 11. DeepSeek

- **Status**: `unverified`
- **Base URL**: `unknown - not confirmed from any evidence`


- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `deepseek-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_

*Source: Discovered via X (3 posts)*


## 12. Sarvam AI

- **Status**: `unverified`
- **Base URL**: `unknown - not confirmed from any evidence`


- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `sarvam-ai-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_

*Source: Discovered via X (1 posts)*


## 13. NVIDIA NIM

- **Status**: `unverified`
- **Base URL**: `https://integrate.api.nvidia.com/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Verification age**: manually verified 2026-09-09

- **Live probe** (2026-09-09T03:39:09+00:00): `public_model_list` — real model ids confirmed

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `01-ai/yi-large` — Context: `unknown`, Output: `unknown`
- `adept/fuyu-8b` — Context: `unknown`, Output: `unknown`
- `ai21labs/jamba-1.5-large-instruct` — Context: `unknown`, Output: `unknown`
- `aisingapore/sea-lion-7b-instruct` — Context: `unknown`, Output: `unknown`
- `bigcode/starcoder2-15b` — Context: `unknown`, Output: `unknown`
- `databricks/dbrx-instruct` — Context: `unknown`, Output: `unknown`
- `deepseek-ai/deepseek-coder-6.7b-instruct` — Context: `unknown`, Output: `unknown`
- `deepseek-ai/deepseek-v4-flash-0731` — Context: `unknown`, Output: `unknown`

*Source: Discovered via X (1 posts)*


## 14. SambaNova

- **Status**: `unverified`
- **Base URL**: `unknown - not confirmed from any evidence`


- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `sambanova-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_

*Source: Discovered via X (1 posts)*


## 15. Hugging Face

- **Status**: `unverified`
- **Base URL**: `unknown - not confirmed from any evidence`


- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
- `hugging-face-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_

*Source: Discovered via X (1 posts)*


## 16. LLM7

- **Status**: `probed`
- **Base URL**: `https://api.llm7.io/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:07+00:00): `public_model_list` — real model ids confirmed

### Privacy
- Not confirmed (unverified)

### Models
- `DeepSeek-V4-Flash-0731` — Context: `unknown`, Output: `unknown`
- `Inkling` — Context: `unknown`, Output: `unknown`
- `Inkling-Small` — Context: `unknown`, Output: `unknown`
- `L3-8B-Lunaris-v1-Turbo` — Context: `unknown`, Output: `unknown`
- `XiaomiMiMo/MiMo-V2.5` — Context: `unknown`, Output: `unknown`
- `XiaomiMiMo/MiMo-V2.5-Pro` — Context: `unknown`, Output: `unknown`
- `chroma-v.46-flash` — Context: `unknown`, Output: `unknown`
- `claude-fable-5` — Context: `unknown`, Output: `unknown`

*Source: Discovered via keyless live probe*

