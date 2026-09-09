# X findings (via x.pcstyle.dev)

- generated: `2026-09-08T16:01:23.247069+00:00`
- posts scanned: `82`
- providers with leads: `16`

> Every value below is a *lead from a public post*, not verified fact. Each claim links to the post it came from. Promotion windows are inferred from post text and dated - x.pcstyle.dev does not honour `until:`, so server-side date filtering is unavailable.

| provider | status | conf | posts | context | promo ends | domains | privacy |
|---|---|---|---|---|---|---|---|
| Ollama Cloud | unverified | 6 | 16 | - | - | ai.google.dev, developers.cloudflare.com | ok: nothing leaves |
| Google Gemini | ✅ active | 6 | 19 | 131K | - | ai.google.dev, console.groq.com | risk_confirmed |
| Moonshot Kimi | ❌ expired | 5.3 | 4 | 1000K | 2026-08-12 (EXPIRED) | api.tokenrouter.com, tokenrouter.com | unknown_third_party |
| OpenCode Zen | unverified | 5 | 6 | 1000K | - | developers.cloudflare.com, ollama.com | - |
| OpenRouter | unverified | 5 | 11 | 131K, 256K | - | ai.google.dev, console.groq.com | - |
| Groq | unverified | 4.7 | 5 | 131K | - | ai.google.dev, console.groq.com | - |
| Mistral AI | unverified | 4.0 | 3 | - | - | console.groq.com, developers.cloudflare.com | - |
| Cloudflare Workers AI | unverified | 4 | 7 | - | - | developers.cloudflare.com, docs.mistral.ai | - |
| Z AI | unverified | 3.7 | 2 | - | - | - | - |
| Qwen | unverified | 3.0 | 3 | - | - | ai.google.dev, console.groq.com | - |
| Cerebras | unverified | 2.7 | 2 | - | - | ai.google.dev, console.groq.com | - |
| DeepSeek | unverified | 2.0 | 3 | - | - | - | - |
| Sarvam AI | unverified | 0.3 | 1 | - | - | - | - |
| NVIDIA NIM | unverified | 0.3 | 1 | - | - | - | - |
| SambaNova | unverified | 0.3 | 1 | - | - | - | - |
| Hugging Face | unverified | 0.3 | 1 | - | - | - | - |

## Verified against provider sources

Only providers with a manually checked source are listed. 2 on file.

### Google Gemini — active
- verdict on the X claim: The X replies warning that the free tier trains on your prompts are substantially CORRECT under the Unpaid Services terms; the originating X post's 'permanent free tier, no billing required' framing omits this trade-off.
- auth: API key from AI Studio; no billing account required for free quota
- limits: RPM + TPM (input) + RPD, applied per project (not per key); RPD resets midnight Pacific; exact per-model numbers are only shown in AI Studio after login, not published in the docs
- caveat: docs state 'Specified rate limits are not guaranteed and actual capacity may vary'
- privacy (risk_confirmed): Free quota counts as 'Unpaid Services': Google uses submitted content and responses to 'provide, improve, and develop' its products and ML technologies, and human reviewers may read/annotate inputs and outputs. Paid quota is the opposite: prompts/responses are not used to improve products.
- privacy (regional): In the EEA, Switzerland and the UK the Paid-Services data terms apply even to the unpaid quota
  > "When you use Unpaid Services, including, for example, Google AI Studio and the unpaid quota on Gemini API, Google uses the content you submit to the Services and any generated responses to provide, improve, and develop Google products and services and machine learning technologies"
  >
  > — <https://ai.google.dev/gemini-api/terms>

### Moonshot Kimi — expired
- verdict on the X claim: Context length and promo end date were REAL but are now EXPIRED; privacy implication is the important part the post never mentioned (third-party routing).
- privacy (unknown_third_party): The offer routes prompts through a third-party gateway, not Moonshot. Its logging/retention/training terms were not established by the X posts and must be read on the reseller's own site before use. Treat as untrusted for anything sensitive.
- promo claim: Free Kimi K3 access with a 1M context window
- promo end: 2026-08-12
- state: expired ~4 weeks before the 2026-09-08 scan; must not be listed as an active free tier
- independent corroboration: https://www.nodeloc.com/t/topic/102092 (2026-08-04, independent of X): 'Free Kimi K3 extended until August 12'
- via: tokenrouter.com (third-party reseller, not Moonshot first-party)

## Leads not yet verified

These came only from public posts. Check the provider docs/terms before adding them to settings.json.

- **Ollama Cloud** (16 posts, conf 6) — verify at: ai.google.dev, developers.cloudflare.com, ollama.com
- **OpenCode Zen** (6 posts, conf 5) — verify at: developers.cloudflare.com, ollama.com
- **OpenRouter** (11 posts, conf 5) — verify at: ai.google.dev, console.groq.com, openrouter.ai
- **Groq** (5 posts, conf 4.7) — verify at: ai.google.dev, console.groq.com, docs.mistral.ai
- **Mistral AI** (3 posts, conf 4.0) — verify at: console.groq.com, developers.cloudflare.com, docs.mistral.ai
- **Cloudflare Workers AI** (7 posts, conf 4) — verify at: developers.cloudflare.com, docs.mistral.ai, ollama.com
- **Z AI** (2 posts, conf 3.7) — verify at: provider docs
- **Qwen** (3 posts, conf 3.0) — verify at: ai.google.dev, console.groq.com, docs.mistral.ai
- **Cerebras** (2 posts, conf 2.7) — verify at: ai.google.dev, console.groq.com, developers.cloudflare.com
- **DeepSeek** (3 posts, conf 2.0) — verify at: provider docs
- **Sarvam AI** (1 posts, conf 0.3) — verify at: provider docs
- **NVIDIA NIM** (1 posts, conf 0.3) — verify at: provider docs
- **SambaNova** (1 posts, conf 0.3) — verify at: provider docs
- **Hugging Face** (1 posts, conf 0.3) — verify at: provider docs

## Ollama Cloud

- confidence **6/10** | posts 16 | last seen 2026-09-08
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: ends, through
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: ai.google.dev, developers.cloudflare.com, ollama.com, tokenrouter.com
- access signals: no card
- privacy risk: none
- privacy positive: nothing leaves

  - 2026-09-06 @kaimarstonai (33636 views): credit limits ⏳ No hidden trials 🔒  Run them 100% locally on your machine—total privacy, zero latency, and $0 cost with open-source models.  💻 Local AI & LLMs  Ollama — Easy CLI to run local LLMs  llama.cpp — https://t.co/Q2AR7tQs1R
    <https://x.com/kaimarstonai/status/2096550347389190557>
  - Tue Aug 04 @nahid_pro09 (7089 views) *(full thread)*: nded for high-volume production workloads treat this as a testing/learning window.  source: http://tokenrouter.com (https://tokenrouter.com/)  OSS Alternative: Ollama (https://github.com/ollama/ollama) run Kimi-compatible or open-weight models locally with zero rate limits
    <https://x.com/nahid_pro09/status/2084613478741057891>
  - Mon Jul 27 @QCXINT_ (5219 views) *(full thread)*: rojects, prototypes, and many small applications.  If you eventually need to run everything locally instead of using cloud APIs...  🖥️ Open Source Alternative: Ollama  Ollama lets you run open-source LLMs directly on your own machine.  It supports popular models like Kimi-K2.6, GLM-5.2, MiniMax, Dee
    <https://x.com/QCXINT_/status/2081876460089082017>
  - Thu Aug 27 @kaddisdeployed (1558 views) *(full thread)*: lare Workers AI  run AI models through Cloudflare useful for AI apps and agents free usage depends on your plan  https://developers.cloudflare.com/workers-ai/  Ollama  run open models directly on your computer no API bill for local inference works with tools like Claude Code and OpenCode  https://ol
    <https://x.com/kaddisdeployed/status/2092990800573415636>

## Google Gemini

- confidence **6/10** | posts 19 | last seen 2026-09-08
- context candidates: 131000
- rate limit: rpm=- rpd=-
- promo signals: through, until
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: ai.google.dev, console.groq.com, openrouter.ai, www.cerebras.ai
- access signals: api key, no card, no credit card
- privacy risk: train on your prompts
- privacy positive: none

  - Mon Jul 27 @QCXINT_ (5219 views) *(full thread)*: 🚨 Google is quietly giving developers production-grade Gemini models—for free. 🤯  No credit card.  No trial.  Just generate an API key and start building.  Google's Gemini API Free Tier lets you access the same production-ready models used in real applications, making it one of the best ways to prot
    <https://x.com/QCXINT_/status/2081876460089082017>
  - Thu Aug 27 @kaddisdeployed (1558 views) *(full thread)*: OpenRouter  hundreds of models through one API dedicated free models section great for testing different models  https://openrouter.ai/collections/free-models  Gemini API  free tier for selected models free input + output on eligible models rate limits apply  https://ai.google.dev/gemini-api/docs/pr
    <https://x.com/kaddisdeployed/status/2092990800573415636>
  - 2025-08-11 @rahulpandey187 (202 views): Built a free AI image generator that turns voice messages into art! 🗣️➡️🖼️ Talk to a Telegram bot, and it uses @GroqCloud for transcription, @GoogleAI's Gemini for prompt enhancement, and @HuggingFace to generate the image. All with free API tiers.  #AI #Automation #n8n #GenAI https://t.co/I6lS00chI
    <https://x.com/rahulpandey187/status/1955011523518079388>
  - 2026-09-07 @phpld (145 views): @GoogleAIStudio When I start seeing clear indication that top people using Claude or ChatGPT are switching over I’ll try it too. Or maybe with a free allotment of credits
    <https://x.com/phpld/status/2096968264987378049>

## Moonshot Kimi

- confidence **5.3/10** | posts 4 | last seen 2026-09-03
- context candidates: 1000000
- rate limit: rpm=- rpd=-
- promo signals: ends, limited-time, through, until
- **inferred promo end**: 2026-08-12  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: api.tokenrouter.com, tokenrouter.com
- access signals: api key, no credit card
- privacy risk: none
- privacy positive: none

  - 2026-09-03 @zefirium (9945 views): MiniMax M3, Kimi K3, GPT-5.6 Luna, Nemotron 3 Ultra, and Meta Muse Spark 1.3 - all FREE.  > KiosAPI: MiniMax M3, Kimi K3, GLM 5.3 Flash, GPT-5.6 Luna, Agnes 2.5 Pro, NVIDIA Nemotron. Limited-time $0 row, OpenAI-compatible: https://t.co/9Xr2YCTYzS  > Azure for Students: $100 Azure https://t.co/or8Ndp
    <https://x.com/zefirium/status/2095552339591430539>
  - Tue Aug 04 @nahid_pro09 (7089 views) *(full thread)*: Kimi-K3 extended through august 12😳  If you have been sitting on the sidelines waiting to test a top-tier model without paying a dime, now is your window. freeKimi K3 gives you real access to a frontier-grade LLM through a simple API key no credit card, no subscription, no enterprise deal required  
    <https://x.com/nahid_pro09/status/2084613478741057891>
  - Mon Jul 27 @QCXINT_ (5219 views) *(full thread)*: of using cloud APIs...  🖥️ Open Source Alternative: Ollama  Ollama lets you run open-source LLMs directly on your own machine.  It supports popular models like Kimi-K2.6, GLM-5.2, MiniMax, DeepSeek, Qwen, Gemma, gpt-oss, and many more.  🔥 Ollama Features  🏠 Run AI models locally with no cloud depend
    <https://x.com/QCXINT_/status/2081876460089082017>
  - Tue Aug 04 @nahid_pro09 (308 views) *(reply)* *(full thread)*: website: https://tokenrouter.com  access moonshotai's kimi k3 with a massive 1m context window completely for free on tokenrouter  bookmark this and test a frontier-grade model without paying a dime before the promo expires  follow @nahid_pro09  for more free AI deals like this
    <https://x.com/nahid_pro09/status/2084613724602786292>

## OpenCode Zen

- confidence **5/10** | posts 6 | last seen 2026-09-08
- context candidates: 1000000
- rate limit: rpm=- rpd=-
- promo signals: through
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: developers.cloudflare.com, ollama.com
- access signals: none
- privacy risk: none
- privacy positive: none

  - 2026-09-04 @sakatayasha (8308 views): holy sh*t, it can't be f**king real   You can use Meta's Muse Spark 1.3 for FREEEEE on Opencode  Muse Spark 1.3 is Meta's frontier, proprietary multimodal reasoning AI model and heavily optimized for advanced coding  what it does:  - Muse Spark 1.3 free and no setup needed - full https://t.co/kuwhgn
    <https://x.com/sakatayasha/status/2095754421041033460>
  - 2026-09-03 @CDGalpha (7564 views): you can get Muse Spark 1.3 for completely free😱  long coding tasks can burn your API credits fast.  OpenCode just made Muse Spark 1.3 Contributor Free available at no token cost.  what you get:  • 1M-token context • up to 131K output • reasoning and tool calling • structured https://t.co/XHFLQmwBNj
    <https://x.com/CDGalpha/status/2095506864653894053>
  - Thu Aug 27 @kaddisdeployed (1558 views) *(full thread)*: /developers.cloudflare.com/workers-ai/  Ollama  run open models directly on your computer no API bill for local inference works with tools like Claude Code and OpenCode  https://ollama.com/  you don’t need to subscribe to 10 different AI tools just to experiment  start with these.l  test the models 
    <https://x.com/kaddisdeployed/status/2092990800573415636>
  - 2026-02-15 @acoyfellow (168 views): out chomp: an OpenAI-compatible proxy that routes to free LLM providers  Grab your keys from @GroqInc  @cerebras @SambaNovaAI @FireworksAI_HQ @openrouter and @OpenCode Zen..  A single endpoint to gobble up their free tokens 🍪  (also ships as an MCP server:
    <https://x.com/acoyfellow/status/2023001331594559796>

## OpenRouter

- confidence **5/10** | posts 11 | last seen 2026-09-04
- context candidates: 131000, 256000
- rate limit: rpm=- rpd=-
- promo signals: through
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: ai.google.dev, console.groq.com, openrouter.ai
- access signals: no card
- privacy risk: none
- privacy positive: none

  - 2026-02-16 @Kailzer (2971 views): @openrouter @MiniMax_AI most devs dont need frontier reasoning. they need good enough at basically free. thats the gap MiniMax walked straight through and OpenClaw riding on top of it proves the point. the killer apps are being built on the cheapest capable model not the most expensive one
    <https://x.com/Kailzer/status/2023464643495371012>
  - Thu Aug 27 @kaddisdeployed (1558 views) *(full thread)*: stop paying for every AI API you want to test 👀  there are actually a lot of good options you can use for $0 right now  here are 7 worth bookmarking:  OpenRouter  hundreds of models through one API dedicated free models section great for testing different models  https://openrouter.ai/collections/fr
    <https://x.com/kaddisdeployed/status/2092990800573415636>
  - 2026-02-16 @Kaancang1 (1215 views): @kira_daruma @openrouter @MiniMax_AI Everyone wants to use it for free, but I'm not asking about that. When it becomes paid, will there be people who continue to use it via the API or membership?
    <https://x.com/Kaancang1/status/2023456534076739869>
  - 2026-02-14 @hey_apurv (715 views): @MiniMax_AI You can now try Minimax 2.5 on @usecloudclaw for @openclaw ai agents  ps: there are more free models available via @openrouter  also, check my latest article for a gift https://t.co/wOMgViT56n
    <https://x.com/hey_apurv/status/2022654299176854006>

## Groq

- confidence **4.7/10** | posts 5 | last seen 2026-09-08
- context candidates: 131000
- rate limit: rpm=- rpd=-
- promo signals: none
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: ai.google.dev, console.groq.com, docs.mistral.ai, www.cerebras.ai
- access signals: no card, no credit card
- privacy risk: none
- privacy positive: none

  - Thu Aug 27 @kaddisdeployed (1558 views) *(full thread)*: free-models  Gemini API  free tier for selected models free input + output on eligible models rate limits apply  https://ai.google.dev/gemini-api/docs/pricing  Groq  free developer tier insanely fast inference access to models like GPT-OSS and Qwen  https://console.groq.com/  Cerebras  $5 free API c
    <https://x.com/kaddisdeployed/status/2092990800573415636>
  - 2025-08-11 @rahulpandey187 (202 views): Built a free AI image generator that turns voice messages into art! 🗣️➡️🖼️ Talk to a Telegram bot, and it uses @GroqCloud for transcription, @GoogleAI's Gemini for prompt enhancement, and @HuggingFace to generate the image. All with free API tiers.  #AI #Automation #n8n #GenAI https://t.co/I6lS00chI
    <https://x.com/rahulpandey187/status/1955011523518079388>
  - 2026-02-15 @acoyfellow (168 views): check out chomp: an OpenAI-compatible proxy that routes to free LLM providers  Grab your keys from @GroqInc  @cerebras @SambaNovaAI @FireworksAI_HQ @openrouter and @OpenCode Zen..  A single endpoint to gobble up their free tokens 🍪  (also ships as an MCP server:
    <https://x.com/acoyfellow/status/2023001331594559796>
  - 2026-09-03 @aiclawbots (117 views): that actually survived august  eight providers still offer a standing free tier with no card required:  1. google gemini api, current flash models, no card 2. groq, 30 requests a minute, 131k context on gpt-oss-120b 3. openrouter, 14 free models, up to 1m https://t.co/lm7mvwRnVo
    <https://x.com/aiclawbots/status/2095572535488172089>

## Mistral AI

- confidence **4.0/10** | posts 3 | last seen 2026-09-08
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: through
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: console.groq.com, developers.cloudflare.com, docs.mistral.ai, www.cerebras.ai
- access signals: no card, no credit card
- privacy risk: none
- privacy positive: none

  - Thu Aug 27 @kaddisdeployed (1558 views) *(full thread)*: S and Qwen  https://console.groq.com/  Cerebras  $5 free API credits very fast inference great for experimenting with AI apps  https://www.cerebras.ai/pricing  Mistral  free API mode no credit card required to get started usage limits apply  https://docs.mistral.ai/getting-started/quickstarts/studio
    <https://x.com/kaddisdeployed/status/2092990800573415636>
  - 2026-09-08 @JulianGoldieSEO (753 views): ee LLM API and it lives on GitHub.  It gives you 7 billion free tokens a month.  You get 34 providers and 635 models in one place.  It runs Claude, Ollama, and Mistral for zero cost.  You will never hit a rate limit https://t.co/H3fMTsnv1G
    <https://x.com/JulianGoldieSEO/status/2097340935885492583>
  - 2026-07-28 @Ryan95322865 (392 views): ack. $0. No card.  Not a 7-day trial. Not "subscribe to continue." Same tools devs actually ship with, local and cloud, free right now.  Ollama  run Llama 3.1, Mistral, Qwen locally. Free forever, no card, no rate https://t.co/a7yVJ1g2ER
    <https://x.com/Ryan95322865/status/2082140022841495947>

## Cloudflare Workers AI

- confidence **4/10** | posts 7 | last seen 2026-08-27
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: through
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: developers.cloudflare.com, docs.mistral.ai, ollama.com
- access signals: no credit card
- privacy risk: none
- privacy positive: none

  - Thu Aug 27 @kaddisdeployed (1558 views) *(full thread)*: e API mode no credit card required to get started usage limits apply  https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key  Cloudflare Workers AI  run AI models through Cloudflare useful for AI apps and agents free usage depends on your plan  https://developers.cl
    <https://x.com/kaddisdeployed/status/2092990800573415636>
  - Thu Aug 27 @painn_x (63 views) *(reply)* *(full thread)*: @kaddisdeployed they’re all goated
    <https://x.com/painn_x/status/2092992042712306010>
  - Thu Aug 27 @avosuai (56 views) *(reply)* *(full thread)*: @kaddisdeployed Worth checking out. Thanks for sharing kadd
    <https://x.com/avosuai/status/2092991376921071645>
  - Thu Aug 27 @undefinedKi (41 views) *(reply)* *(full thread)*: @kaddisdeployed nice list bro, bookmarked
    <https://x.com/undefinedKi/status/2093002582222348576>

## Z AI

- confidence **3.7/10** | posts 2 | last seen 2026-09-03
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: limited-time
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: none
- access signals: none
- privacy risk: none
- privacy positive: none

  - 2026-09-03 @zefirium (9945 views): MiniMax M3, Kimi K3, GPT-5.6 Luna, Nemotron 3 Ultra, and Meta Muse Spark 1.3 - all FREE.  > KiosAPI: MiniMax M3, Kimi K3, GLM 5.3 Flash, GPT-5.6 Luna, Agnes 2.5 Pro, NVIDIA Nemotron. Limited-time $0 row, OpenAI-compatible: https://t.co/9Xr2YCTYzS  > Azure for Students: $100 Azure https://t.co/or8Ndp
    <https://x.com/zefirium/status/2095552339591430539>
  - Mon Jul 27 @QCXINT_ (5219 views) *(full thread)*: oud APIs...  🖥️ Open Source Alternative: Ollama  Ollama lets you run open-source LLMs directly on your own machine.  It supports popular models like Kimi-K2.6, GLM-5.2, MiniMax, DeepSeek, Qwen, Gemma, gpt-oss, and many more.  🔥 Ollama Features  🏠 Run AI models locally with no cloud dependency.  ⚡ Op
    <https://x.com/QCXINT_/status/2081876460089082017>

## Qwen

- confidence **3.0/10** | posts 3 | last seen 2026-08-27
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: none
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: ai.google.dev, console.groq.com, docs.mistral.ai, www.cerebras.ai
- access signals: no card, no credit card
- privacy risk: none
- privacy positive: none

  - Mon Jul 27 @QCXINT_ (5219 views) *(full thread)*: Alternative: Ollama  Ollama lets you run open-source LLMs directly on your own machine.  It supports popular models like Kimi-K2.6, GLM-5.2, MiniMax, DeepSeek, Qwen, Gemma, gpt-oss, and many more.  🔥 Ollama Features  🏠 Run AI models locally with no cloud dependency.  ⚡ OpenAI-compatible REST API.  🐳
    <https://x.com/QCXINT_/status/2081876460089082017>
  - Thu Aug 27 @kaddisdeployed (1558 views) *(full thread)*: le models rate limits apply  https://ai.google.dev/gemini-api/docs/pricing  Groq  free developer tier insanely fast inference access to models like GPT-OSS and Qwen  https://console.groq.com/  Cerebras  $5 free API credits very fast inference great for experimenting with AI apps  https://www.cerebra
    <https://x.com/kaddisdeployed/status/2092990800573415636>
  - 2026-07-28 @Ryan95322865 (392 views): No card.  Not a 7-day trial. Not "subscribe to continue." Same tools devs actually ship with, local and cloud, free right now.  Ollama  run Llama 3.1, Mistral, Qwen locally. Free forever, no card, no rate https://t.co/a7yVJ1g2ER
    <https://x.com/Ryan95322865/status/2082140022841495947>

## Cerebras

- confidence **2.7/10** | posts 2 | last seen 2026-08-27
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: through
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: ai.google.dev, console.groq.com, developers.cloudflare.com, docs.mistral.ai, www.cerebras.ai
- access signals: no credit card
- privacy risk: none
- privacy positive: none

  - Thu Aug 27 @kaddisdeployed (1558 views) *(full thread)*: to models like GPT-OSS and Qwen  https://console.groq.com/  Cerebras  $5 free API credits very fast inference great for experimenting with AI apps  https://www.cerebras.ai/pricing  Mistral  free API mode no credit card required to get started usage limits apply  https://docs.mistral.ai/getting-start
    <https://x.com/kaddisdeployed/status/2092990800573415636>
  - 2026-02-15 @acoyfellow (168 views): check out chomp: an OpenAI-compatible proxy that routes to free LLM providers  Grab your keys from @GroqInc  @cerebras @SambaNovaAI @FireworksAI_HQ @openrouter and @OpenCode Zen..  A single endpoint to gobble up their free tokens 🍪  (also ships as an MCP server:
    <https://x.com/acoyfellow/status/2023001331594559796>

## DeepSeek

- confidence **2.0/10** | posts 3 | last seen 2026-09-05
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: limited-time
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: none
- access signals: none
- privacy risk: none
- privacy positive: none

  - Mon Jul 27 @QCXINT_ (5219 views) *(full thread)*: en Source Alternative: Ollama  Ollama lets you run open-source LLMs directly on your own machine.  It supports popular models like Kimi-K2.6, GLM-5.2, MiniMax, DeepSeek, Qwen, Gemma, gpt-oss, and many more.  🔥 Ollama Features  🏠 Run AI models locally with no cloud dependency.  ⚡ OpenAI-compatible RE
    <https://x.com/QCXINT_/status/2081876460089082017>
  - 2026-09-05 @MR_0FFICIALL (315 views): 𝗗𝗲𝗲𝗽𝗦𝗲𝗲𝗸 𝗩𝟰 𝗚𝗼𝘁 𝗠𝗼𝗿𝗲 𝗘𝘅𝗽𝗲𝗻𝘀𝗶𝘃𝗲. 𝗕.𝗔𝗜 𝗝𝘂𝘀𝘁 𝗠𝗮𝗱𝗲 𝗩𝟰-𝗙𝗹𝗮𝘀𝗵 𝗙𝗿𝗲𝗲  DeepSeek-V4 has officially increased its pricing.  But at the same time, https://t.co/bhV5HbjB5e has opened DeepSeek-V4-Flash for limited-time free access.  And the https://t.co/1xEgez60XD
    <https://x.com/MR_0FFICIALL/status/2096208159270441425>
  - 2026-09-05 @Quinmooda (122 views): 𝗗𝗲𝗲𝗽𝗦𝗲𝗲𝗸 𝗩𝟰 𝗜𝘀 𝗠𝗼𝗿𝗲 𝗘𝘅𝗽𝗲𝗻𝘀𝗶𝘃𝗲. 𝗕𝘂𝘁 𝗕.𝗔𝗜 𝗝𝘂𝘀𝘁 𝗠𝗮𝗱𝗲 𝗩𝟰-𝗙𝗹𝗮𝘀𝗵 𝗘𝗮𝘀𝗶𝗲𝗿 𝘁𝗼 𝗧𝗿𝘆. ⚡  DeepSeek-V4 has officially moved to higher pricing.  At the same time, https://t.co/FXfjXxkOzL is offering DeepSeek-V4-Flash with limited-time
    <https://x.com/Quinmooda/status/2096244753100615972>

## Sarvam AI

- confidence **0.3/10** | posts 1 | last seen 2026-09-05
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: none
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: none
- access signals: none
- privacy risk: none
- privacy positive: none

  - 2026-09-05 @buzzy_bit (102541 views): Since a lot of you asked for it, here's my Sarvam AI interview experience https://t.co/Q6HQPiZWdb
    <https://x.com/buzzy_bit/status/2096138888251375848>

## NVIDIA NIM

- confidence **0.3/10** | posts 1 | last seen 2026-09-03
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: limited-time
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: none
- access signals: none
- privacy risk: none
- privacy positive: none

  - 2026-09-03 @zefirium (9945 views): x M3, Kimi K3, GPT-5.6 Luna, Nemotron 3 Ultra, and Meta Muse Spark 1.3 - all FREE.  > KiosAPI: MiniMax M3, Kimi K3, GLM 5.3 Flash, GPT-5.6 Luna, Agnes 2.5 Pro, NVIDIA Nemotron. Limited-time $0 row, OpenAI-compatible: https://t.co/9Xr2YCTYzS  > Azure for Students: $100 Azure https://t.co/or8NdpaKRz
    <https://x.com/zefirium/status/2095552339591430539>

## SambaNova

- confidence **0.3/10** | posts 1 | last seen 2026-02-15
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: none
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: none
- access signals: none
- privacy risk: none
- privacy positive: none

  - 2026-02-15 @acoyfellow (168 views): check out chomp: an OpenAI-compatible proxy that routes to free LLM providers  Grab your keys from @GroqInc  @cerebras @SambaNovaAI @FireworksAI_HQ @openrouter and @OpenCode Zen..  A single endpoint to gobble up their free tokens 🍪  (also ships as an MCP server:
    <https://x.com/acoyfellow/status/2023001331594559796>

## Hugging Face

- confidence **0.3/10** | posts 1 | last seen 2025-08-11
- context candidates: none found
- rate limit: rpm=- rpd=-
- promo signals: none
- **inferred promo end**: none  _(derived from post prose + post date - verify on the provider's site)_
- domains seen: none
- access signals: none
- privacy risk: none
- privacy positive: none

  - 2025-08-11 @rahulpandey187 (202 views): or that turns voice messages into art! 🗣️➡️🖼️ Talk to a Telegram bot, and it uses @GroqCloud for transcription, @GoogleAI's Gemini for prompt enhancement, and @HuggingFace to generate the image. All with free API tiers.  #AI #Automation #n8n #GenAI https://t.co/I6lS00chI1
    <https://x.com/rahulpandey187/status/1955011523518079388>
