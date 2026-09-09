# Free LLM APIs

<<<<<<< HEAD
- generated: `2026-09-08T16:01:23.388803+00:00`
- providers: `17`
=======
- generated: `2026-09-09T04:04:18.109354+00:00`
- providers: `16`
>>>>>>> 382d5fc (minor modifications)

> ⚠️ Only providers with **verified_from_x = true** have been confirmed via X post evidence.
> Providers with **status = expired** should not be listed as active free tiers.

| # | Provider | Status | Context | Promo End | Auth |
|---|----------|--------|---------|-----------|------|
<<<<<<< HEAD
| 1 | Ollama Cloud | unverified | 131072 tokens | - | api_key |
| 2 | Google Gemini | active | 131000 tokens | - | api_key |
| 3 | OpenCode Zen | unverified | 1000000 tokens | - | api_key |
| 4 | OpenRouter | unverified | 131000 tokens | - | api_key |
| 5 | Groq | unverified | 131000 tokens | - | api_key |
| 6 | Mistral AI | unverified | 131072 tokens | - | api_key |
| 7 | Cloudflare Workers AI | unverified | 131072 tokens | - | api_key |
| 8 | Z AI | unverified | 131072 tokens | - | api_key |
| 9 | Qwen | unverified | 131072 tokens | - | api_key |
| 10 | Cerebras | unverified | 131072 tokens | - | api_key |
| 11 | DeepSeek | unverified | 131072 tokens | - | api_key |
| 12 | Sarvam AI | unverified | 131072 tokens | - | api_key |
| 13 | NVIDIA NIM | unverified | 131072 tokens | - | api_key |
| 14 | SambaNova | unverified | 131072 tokens | - | api_key |
| 15 | Hugging Face | unverified | 131072 tokens | - | api_key |
| 16 | Ollama | unverified | 131072 tokens | - | api_key |
| 17 | SiliconFlow | unverified | 32768 tokens | - | api_key |
=======
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
>>>>>>> 382d5fc (minor modifications)


## 1. Ollama Cloud

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `http://tokenrouter.com`
- **Auth**: api_key
- **Rate Limits**: {}

=======
- **Base URL**: `https://ollama.com/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:08+00:00): `public_model_list` — real model ids confirmed

>>>>>>> 382d5fc (minor modifications)
### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `ollama-cloud-free` — Context: `131072`, Output: `8192`
=======
- `kimi-k2.6` — Context: `unknown`, Output: `unknown`
- `kimi-k2.7-code` — Context: `unknown`, Output: `unknown`
- `nemotron-3-ultra` — Context: `unknown`, Output: `unknown`
- `gemma4:31b` — Context: `unknown`, Output: `unknown`
- `nemotron-3-super` — Context: `unknown`, Output: `unknown`
- `deepseek-v4-flash:0731` — Context: `unknown`, Output: `unknown`
- `glm-5.3-flash` — Context: `unknown`, Output: `unknown`
- `gpt-oss:120b` — Context: `unknown`, Output: `unknown`
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (16 posts)*


## 2. Google Gemini

- **Status**: `active`
<<<<<<< HEAD
- **Base URL**: `https://openrouter.ai/collections/free-models`
- **Auth**: api_key
- **Rate Limits**: {}

=======
- **Base URL**: `https://generativelanguage.googleapis.com/v1beta/openai`


- **Auth**: api_key
- **Rate Limits**: {}

- **Verification age**: manually verified 2026-09-08

>>>>>>> 382d5fc (minor modifications)
> **X claim verdict**: The X replies warning that the free tier trains on your prompts are substantially CORRECT under the Unpaid Services terms; the originating X post's 'permanent free tier, no billing required' framing omits this trade-off.

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**
- Human reviewers: **Yes**
- Regional exception: In the EEA, Switzerland and the UK the Paid-Services data terms apply even to the unpaid quota

### Models
<<<<<<< HEAD
- `google-gemini-free` — Context: `131000`, Output: `65500`
=======
- `google-gemini-free` — Context: `131000`, Output: `65500` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (19 posts)*


## 3. OpenCode Zen

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://ollama.com/`
- **Auth**: api_key
- **Rate Limits**: {}

=======
- **Base URL**: `https://opencode.ai/zen/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:09+00:00): `public_model_list` — real model ids confirmed

>>>>>>> 382d5fc (minor modifications)
### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `opencode-zen-free` — Context: `1000000`, Output: `500000`
=======
- `claude-fable-5` — Context: `1000000`, Output: `unknown`
- `claude-fable-5-1` — Context: `1000000`, Output: `unknown`
- `claude-opus-5` — Context: `1000000`, Output: `unknown`
- `claude-opus-4-8` — Context: `1000000`, Output: `unknown`
- `claude-opus-4-7` — Context: `1000000`, Output: `unknown`
- `claude-opus-4-6` — Context: `1000000`, Output: `unknown`
- `claude-opus-4-5` — Context: `1000000`, Output: `unknown`
- `claude-sonnet-5` — Context: `1000000`, Output: `unknown`
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (6 posts)*


## 4. OpenRouter

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://openrouter.ai/collections/fr`
- **Auth**: api_key
- **Rate Limits**: {}

=======
- **Base URL**: `https://openrouter.ai/api/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:06+00:00): `ok` — real model ids confirmed

>>>>>>> 382d5fc (minor modifications)
### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `openrouter-free` — Context: `131000`, Output: `65500`
- `openrouter-free` — Context: `256000`, Output: `128000`
=======
- `nex-agi/nex-n2.5-mini:free` — Context: `262144`, Output: `unknown`
- `nex-agi/nex-n2.5-pro:free` — Context: `262144`, Output: `unknown`
- `inclusionai/ling-3.0-flash-sante:free` — Context: `262144`, Output: `unknown`
- `inclusionai/ling-3.0-flash-fin:free` — Context: `262144`, Output: `unknown`
- `dots-studio/dots-3-note-preview:free` — Context: `512000`, Output: `unknown`
- `liquid/lfm-2.5-2.6b:free` — Context: `65536`, Output: `unknown`
- `nvidia/nemotron-3.5-lightning:free` — Context: `1000000`, Output: `unknown`
- `thinkingmachines/inkling-small:free` — Context: `1048576`, Output: `unknown`
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (11 posts)*


## 5. Groq

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://ai.google.dev/gemini-api/docs/pricing`
- **Auth**: api_key
- **Rate Limits**: {}

=======
- **Base URL**: `https://api.groq.com/openai/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:06+00:00): `endpoint_alive_listing_http_401`

>>>>>>> 382d5fc (minor modifications)
### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `groq-free` — Context: `131000`, Output: `65500`
=======
- `groq-free` — Context: `131000`, Output: `65500` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (5 posts)*


## 6. Mistral AI

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://console.groq.com/`
- **Auth**: api_key
- **Rate Limits**: {}

=======
- **Base URL**: `https://api.mistral.ai/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:06+00:00): `endpoint_alive_listing_http_401`

>>>>>>> 382d5fc (minor modifications)
### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `mistral-ai-free` — Context: `131072`, Output: `8192`
=======
- `mistral-ai-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (3 posts)*


## 7. Cloudflare Workers AI

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key`
=======
- **Base URL**: `unknown - not confirmed from any evidence`

  > Other URLs quoted in the posts did not match this provider's name and are NOT credited as its endpoint: `https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key`
>>>>>>> 382d5fc (minor modifications)
- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `cloudflare-workers-ai-free` — Context: `131072`, Output: `8192`
=======
- `cloudflare-workers-ai-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (7 posts)*


## 8. Z AI

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://api.zai.com/v1`
=======
- **Base URL**: `unknown - not confirmed from any evidence`


>>>>>>> 382d5fc (minor modifications)
- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `z-ai-free` — Context: `131072`, Output: `8192`
=======
- `z-ai-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (2 posts)*


## 9. Qwen

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://ai.google.dev/gemini-api/docs/pricing`
=======
- **Base URL**: `unknown - not confirmed from any evidence`

  > Other URLs quoted in the posts did not match this provider's name and are NOT credited as its endpoint: `https://ai.google.dev/gemini-api/docs/pricing`, `https://console.groq.com/`
>>>>>>> 382d5fc (minor modifications)
- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `qwen-free` — Context: `131072`, Output: `8192`
=======
- `qwen-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (3 posts)*


## 10. Cerebras

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://console.groq.com/`
- **Auth**: api_key
- **Rate Limits**: {}

=======
- **Base URL**: `https://api.cerebras.ai/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:07+00:00): `endpoint_alive_listing_http_403`

>>>>>>> 382d5fc (minor modifications)
### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `cerebras-free` — Context: `131072`, Output: `8192`
=======
- `cerebras-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (2 posts)*


## 11. DeepSeek

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://api.deepseek.com/v1`
=======
- **Base URL**: `unknown - not confirmed from any evidence`


>>>>>>> 382d5fc (minor modifications)
- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `deepseek-free` — Context: `131072`, Output: `8192`
=======
- `deepseek-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (3 posts)*


## 12. Sarvam AI

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://api.sarvamai.com/v1`
=======
- **Base URL**: `unknown - not confirmed from any evidence`


>>>>>>> 382d5fc (minor modifications)
- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `sarvam-ai-free` — Context: `131072`, Output: `8192`
=======
- `sarvam-ai-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (1 posts)*


## 13. NVIDIA NIM

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://api.nvidianim.com/v1`
- **Auth**: api_key
- **Rate Limits**: {}

=======
- **Base URL**: `https://integrate.api.nvidia.com/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Verification age**: manually verified 2026-09-09

- **Live probe** (2026-09-09T03:39:09+00:00): `public_model_list` — real model ids confirmed

>>>>>>> 382d5fc (minor modifications)
### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `nvidia-nim-free` — Context: `131072`, Output: `8192`
=======
- `01-ai/yi-large` — Context: `unknown`, Output: `unknown`
- `adept/fuyu-8b` — Context: `unknown`, Output: `unknown`
- `ai21labs/jamba-1.5-large-instruct` — Context: `unknown`, Output: `unknown`
- `aisingapore/sea-lion-7b-instruct` — Context: `unknown`, Output: `unknown`
- `bigcode/starcoder2-15b` — Context: `unknown`, Output: `unknown`
- `databricks/dbrx-instruct` — Context: `unknown`, Output: `unknown`
- `deepseek-ai/deepseek-coder-6.7b-instruct` — Context: `unknown`, Output: `unknown`
- `deepseek-ai/deepseek-v4-flash-0731` — Context: `unknown`, Output: `unknown`
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (1 posts)*


## 14. SambaNova

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://api.sambanova.com/v1`
=======
- **Base URL**: `unknown - not confirmed from any evidence`


>>>>>>> 382d5fc (minor modifications)
- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `sambanova-free` — Context: `131072`, Output: `8192`
=======
- `sambanova-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (1 posts)*


## 15. Hugging Face

- **Status**: `unverified`
<<<<<<< HEAD
- **Base URL**: `https://api.huggingface.com/v1`
=======
- **Base URL**: `unknown - not confirmed from any evidence`


>>>>>>> 382d5fc (minor modifications)
- **Auth**: api_key
- **Rate Limits**: {}

### Privacy
- Logs prompts: **Yes**
- Used for training: **Yes**

### Models
<<<<<<< HEAD
- `hugging-face-free` — Context: `131072`, Output: `8192`
=======
- `hugging-face-free` — Context: `unknown`, Output: `unknown` _(inferred id - confirm via /models)_
>>>>>>> 382d5fc (minor modifications)

*Source: Discovered via X (1 posts)*


<<<<<<< HEAD
## 16. Ollama

- **Status**: `unverified`
- **Base URL**: `https://cloud.ollama.com/v1`
- **Auth**: api_key
- **Rate Limits**: {"requests_per_minute": 10, "requests_per_day": 500}
=======
## 16. LLM7

- **Status**: `probed`
- **Base URL**: `https://api.llm7.io/v1`


- **Auth**: api_key
- **Rate Limits**: {}

- **Live probe** (2026-09-09T03:39:07+00:00): `public_model_list` — real model ids confirmed
>>>>>>> 382d5fc (minor modifications)

### Privacy
- Not confirmed (unverified)

### Models
<<<<<<< HEAD
- `ollama/free-7b` — Context: `131072`, Output: `4096`

*Source: Manual verification*


## 17. SiliconFlow

- **Status**: `unverified`
- **Base URL**: `https://api.siliconflow.cn/v1`
- **Auth**: api_key
- **Rate Limits**: {"requests_per_minute": 20, "requests_per_day": 1000}

### Privacy
- Logs prompts: **Yes**

### Models
- `free-mixtral-8x7b` — Context: `32768`, Output: `4096`

*Source: Manual verification*
=======
- `DeepSeek-V4-Flash-0731` — Context: `unknown`, Output: `unknown`
- `Inkling` — Context: `unknown`, Output: `unknown`
- `Inkling-Small` — Context: `unknown`, Output: `unknown`
- `L3-8B-Lunaris-v1-Turbo` — Context: `unknown`, Output: `unknown`
- `XiaomiMiMo/MiMo-V2.5` — Context: `unknown`, Output: `unknown`
- `XiaomiMiMo/MiMo-V2.5-Pro` — Context: `unknown`, Output: `unknown`
- `chroma-v.46-flash` — Context: `unknown`, Output: `unknown`
- `claude-fable-5` — Context: `unknown`, Output: `unknown`

*Source: Discovered via keyless live probe*
>>>>>>> 382d5fc (minor modifications)

