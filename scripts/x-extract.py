#!/usr/bin/env python3
"""x-extract.py - turn the raw X corpus into structured free-LLM-API leads.

Reads  data/x-posts.json   (written by x-scan.sh)
Writes data/x-leads.json   (structured, machine-readable)
       docs/x-findings.md  (human-readable, with per-claim evidence + post dates)

Design notes
  - Every extracted field carries the post id/url it came from. No evidence, no claim.
  - Promotion windows are parsed from post text AND dated against created_at,
    because x.pcstyle.dev does NOT honor `until:` server-side.
  - Promotional/engagement-bait accounts are down-weighted, not deleted.
"""
import json, os, re, sys, html, datetime, collections, glob
from email.utils import parsedate_to_datetime


def ts_of(created_at):
    try:
        return int(parsedate_to_datetime(created_at).timestamp())
    except Exception:
        return 0

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(BASE, 'data', 'x-posts.json')
OUTJ = os.path.join(BASE, 'data', 'x-leads.json')
OUTM = os.path.join(BASE, 'docs', 'x-findings.md')
VERF = os.path.join(BASE, 'data', 'verified.json')

PROVIDERS = {
    'groq': 'Groq', 'openrouter': 'OpenRouter', 'mistral': 'Mistral AI',
    'gemini': 'Google Gemini', 'aistudio': 'Google Gemini', 'google ai': 'Google Gemini',
    'cloudflare': 'Cloudflare Workers AI', 'workers ai': 'Cloudflare Workers AI',
    'ollama': 'Ollama Cloud', 'cerebras': 'Cerebras', 'huggingface': 'Hugging Face',
    'hugging face': 'Hugging Face', 'kilo': 'Kilo Code', 'opencode': 'OpenCode Zen',
    'llm7': 'LLM7', 'pollinations': 'Pollinations', 'z.ai': 'Z AI', 'zhipu': 'Z AI',
    'glm': 'Z AI', 'nvidia': 'NVIDIA NIM', 'nemotron': 'NVIDIA NIM',
    'ovh': 'OVHcloud AI Endpoints', 'siliconflow': 'SiliconFlow',
    'modelscope': 'ModelScope', 'aion': 'Aion Labs', 'deepseek': 'DeepSeek',
    'cohere': 'Cohere', 'qwen': 'Qwen', 'moonshot': 'Moonshot Kimi', 'kimi': 'Moonshot Kimi',
    'sarvam': 'Sarvam AI', 'sambanova': 'SambaNova', 'github models': 'GitHub Models',
}

CTX   = re.compile(r'(\d{1,4}(?:\.\d+)?)\s*([km])\b[^\n]{0,24}?(context|window|ctx)'
                   r'|(?:context|window|ctx)[^\n]{0,24}?(\d{1,4}(?:\.\d+)?)\s*([km])\b', re.I)
RPM   = re.compile(r'(\d{1,5})\s*(?:requests?\s*/?\s*(?:min(?:ute)?|minute)|rpm)', re.I)
RPD   = re.compile(r'(\d{1,6})\s*(?:requests?\s*/?\s*(?:day|per day)|rpd)', re.I)
TOKS  = re.compile(r'([\d.,]+)\s*(?:billion|million|[bm])\s+free\s+tokens', re.I)
URL   = re.compile(r'https?://(?:[a-z0-9-]+\.)+(?:com|ai|io|dev|cloud|net|co|gg|sh|run)\b[^\s)>\]]*', re.I)

PRIVACY_RISK = re.compile(r'\b(?:train(?:ing)?\s+on\s+(?:your|user)\s+(?:data|prompts)|'
                          r'used\s+to\s+train|data\s+is\s+logged|prompts?\s+are\s+logged|'
                          r'logs?\s+(?:your\s+)?(?:prompts|inputs)|share\s+your\s+data)\b', re.I)
PRIVACY_OK   = re.compile(r'\b(?:no\s+(?:data\s+)?retention|zero\s+data\s+retention|'
                          r'(?:not|never)\s+(?:be\s+)?(?:used\s+to\s+)?train|'
                          r'data\s+(?:is\s+)?not\s+used|end[-\s]to[-\s]end|'
                          r'nothing\s+leaves|stays?\s+(?:on|local)\s+your|opt[-\s]out)\b', re.I)
DURATION = re.compile(r'\b(?:until|till|through|ends?\s+(?:on)?|end\s+of|'
                      r'limited[-\s]time|for\s+(?:the\s+)?(?:first|next)\s+\d+\s*\w*\s*(?:days?|hours?|weeks?)|'
                      r'launch\s+week|this\s+week(?:end)?|today\s+only|beta)\b', re.I)
NEEDS    = re.compile(r'\b(?:no\s+credit\s+card|no\s+card|no\s+signup|no\s+api\s+key|'
                      r'sign\s*up|sign\s*up\s+free|create\s+(?:a\s+|your\s+)?(?:free\s+)?account|'
                      r'api\s+key)\b', re.I)
# Promo windows: capture an actual end date, not just the word "through".
PROMO_END = re.compile(r'\b(?:through|till|until|ends?\s+(?:on)?|end\s+of|by)\s+'
                       r'(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+)?'
                       r'(\d{1,2})(?:st|nd|rd|th)?\b', re.I)
MONTHS = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
          'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
MONTH_AT = re.compile(r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{1,2})', re.I)
# bare domains in prose (t.co/x.com are links, not providers)
DOMAIN = re.compile(r'(?<![a-z0-9.-])((?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+'
                    r'(?:com|ai|io|dev|cloud|net|co|gg|sh|run|app|tools|zone))\b', re.I)
BAD_DOMAINS = {'x.com', 't.co', 'twitter.com', 'pic.twitter.com', 'github.com', 'ibb.co'}
BAIT     = re.compile(r'\b(?:comment\s+\w+\s+(?:below|and)|follow\s+(?:and|to)\s+(?:like|rt|comment)|'
                      r'\b(?:rt|retweet)\s+to\b|giveaway|dm\s+me|link\s+in\s+bio|'
                      r'\$[\d,]+\s+(?:worth\s+of\s+)?(?:free\s+)?credits)\b', re.I)

def clean(t):
    return html.unescape(t or '').replace('\u2028', ' ').replace('\u2028', ' ')

def to_int(n, unit):
    mult = 1_000 if (unit or 'k').lower() == 'k' else 1_000_000
    return int(float(n) * mult)


def normalize_promo_end(text, post_ts):
    """Infer an ISO promo end date from prose, using the post date to pick the year.
    A bare day-number ('through the 12th') resolves to that day in the post's month,
    rolling to next month/year if it is already in the past."""
    if not post_ts:
        return []
    base = datetime.datetime.fromtimestamp(post_ts, datetime.timezone.utc)
    found = []
    for m in MONTH_AT.finditer(text):
        mo = MONTHS.get(m.group(1)[:3].lower())
        day = int(m.group(2))
        if not mo or day > 31:
            continue
        yr = base.year if mo >= base.month else base.year + 1
        try:
            found.append(datetime.date(yr, mo, day))
        except ValueError:
            pass
    for m in PROMO_END.finditer(text):
        day = int(m.group(1))
        if day > 31:
            continue
        mo, yr = base.month, base.year
        if day < base.day:
            mo = base.month + 1
            if mo > 12:
                mo, yr = 1, base.year + 1
        try:
            found.append(datetime.date(yr, mo, day))
        except ValueError:
            pass
    return sorted({d.isoformat() for d in found if d >= base.date()})


def domains_in(text, spans=None):
    """Domains in `text`. If `spans` is given, keep only matches overlapping them.
    Always match on the FULL text: slicing first can start a window in the middle of
    a hostname and invent a domain ('...cloudflare.com' -> 'lare.com')."""
    out = set()
    for m in DOMAIN.finditer(text):
        d = m.group(0).lower().strip('.')
        if d in BAD_DOMAINS:
            continue
        if spans is not None and not any(s <= m.start() < e for s, e in spans):
            continue
        out.add(d)
    # drop fragments that are just the tail of a longer domain seen in the same text
    return {d for d in out if not any(o != d and o.endswith('.' + d) for o in out)}

def providers_in(text):
    """Providers named anywhere in a text -> {std: [surface forms]}"""
    low = text.lower()
    hits = {}
    for std, keys in PROVIDER_KEYS.items():
        for k in keys:
            if k in low:
                hits.setdefault(std, []).append(k)
    return hits


def thread_posts(path):
    """Expand a status deep-dive file into evidence items (full, untruncated text).
    Replies rarely repeat the provider name, so every non-root post inherits the
    providers named by the root post - otherwise thread-level privacy pushback
    ('wait until the free tier trains on your prompts') is attributed to nobody."""
    try:
        d = json.load(open(path))
    except Exception:
        return []
    raw = d.get('posts') or []
    # Only the thread's PRIMARY provider (most-named in the root post) inherits replies.
    # A reply like "wait until the free tier trains on your prompts" is about the thread's
    # subject, not about every other model the root post mentioned in passing.
    root_counts = collections.Counter()
    if raw:
        low0 = clean((raw[0] or {}).get('text', '')).lower()
        for std, keys in PROVIDER_KEYS.items():
            root_counts[std] = sum(low0.count(k) for k in keys)
    primary = [s for s, c in root_counts.most_common(1) if c > 0]
    out = []
    for i, p in enumerate(raw):
        out.append({
            'id': p.get('id'), 'url': p.get('url') or d.get('url'),
            'date': (p.get('created_at') or '?')[:10],
            'author': ((p.get('author') or {}).get('screen_name')) or '?',
            'views': p.get('views') or 0, 'likes': p.get('likes') or 0,
            'created_timestamp': ts_of(p.get('created_at')),
            'replying_to': p.get('replying_to'),
            'full_text': clean(p.get('text', '')),
            '_inherit': [] if i == 0 else primary,
        })
    return out


# std -> the surface forms that identify it in prose
PROVIDER_KEYS = {}
for _k, _v in PROVIDERS.items():
    PROVIDER_KEYS.setdefault(_v, set()).add(_k)


def signal_count(s):
    n = 0
    for rx in (CTX, RPM, RPD, TOKS, DURATION, PRIVACY_RISK, PRIVACY_OK, NEEDS):
        n += len(rx.findall(s))
    return n


def author_of(p):
    a = p.get('author')
    if isinstance(a, str):
        return a, 0
    if isinstance(a, dict):
        return a.get('screen_name') or '?', a.get('followers') or 0
    return '?', 0


def main():
    if not os.path.exists(SRC):
        sys.exit(f'missing {SRC} - run scripts/x-scan.sh first')
    posts = json.load(open(SRC))
    now = datetime.datetime.now(datetime.timezone.utc)

    # splice in full thread text from any status deep-dives (search snippets are truncated)
    raw_x = os.path.join(BASE, 'data', 'raw', 'x')
    fulltext = {}
    for f in sorted(glob.glob(os.path.join(raw_x, 'status-*.json'))):
        for tp in thread_posts(f):
            if tp['id']:
                fulltext[str(tp['id'])] = tp
    posts = [p for p in posts if str(p.get('id')) not in fulltext] + list(fulltext.values())

    leads = collections.defaultdict(lambda: {
        'provider': None, 'context_candidates': set(), 'rpm': set(), 'rpd': set(),
        'free_token_claims': set(), 'endpoints': set(), 'privacy_risk': set(),
        'privacy_positive': set(), 'promo_window': set(), 'promo_end': set(),
        'domains': set(), 'access': set(), 'models': set(),
        'evidence': [], '_authored': set(), '_spam': 0, '_reach': 0, '_latest': 0,
    })

    for p in posts:
        text = clean(p.get('text', '')) or p.get('full_text', '')
        low = text.lower()
        handle, followers = author_of(p)
        ts = p.get('created_timestamp') or 0
        when = p.get('date') if p.get('date') else (
            datetime.datetime.utcfromtimestamp(ts).date().isoformat() if ts else '?')
        spam = bool(BAIT.search(text))

        # Window around each provider mention. A list post that names 7 providers
        # must not smear one provider's context length / promo date onto the others.
        # Replies inside a thread inherit the thread's topic instead.
        inherited = p.get('_inherit') or []
        prov_hits = {s: ['<thread>'] for s in inherited} if inherited else providers_in(text)
        for std in prov_hits:
            spans, wins = [], []
            if inherited:                      # reply: whole text belongs to the thread subject
                spans, wins = [(0, len(text))], [text]
            else:
                for key in prov_hits[std]:
                    for m in re.finditer(re.escape(key), low):
                        s, e = max(0, m.start() - 160), min(len(text), m.end() + 320)
                        spans.append((s, e))
                        wins.append(text[s:e])
            wins = list(dict.fromkeys(wins))
            if not wins:
                continue
            blob = ' \n '.join(wins)                       # claims scoped to this provider
            best = max(wins, key=signal_count)              # most claim-dense window
            blob_low = blob.lower()

            L = leads[std]
            L['provider'] = std
            L['_reach'] += p.get('views') or 0
            L['_latest'] = max(L['_latest'], ts)
            if handle.lower() == std.split()[0].lower() or std.split()[0].lower().replace(' ', '') in handle.lower():
                L['_authored'].add(handle)
            if spam:
                L['_spam'] += 1
            L['evidence'].append({
                'id': p.get('id'), 'url': p.get('url'), 'date': when,
                'author': handle, 'followers': followers,
                'views': p.get('views') or 0, 'likes': p.get('likes') or 0,
                'spam_flag': spam,
                'reply': bool(p.get('replying_to')),
                'full': bool(p.get('full_text')),
                'windowed': len(wins) > 0 and len(blob) < len(text),
                'excerpt': best.strip().replace('\n', ' ')[:300],
            })
            for m in CTX.finditer(blob):
                n, u = (m.group(1), m.group(2)) or (m.group(4), m.group(5))
                if n: L['context_candidates'].add(to_int(n, u))
            for m in RPM.finditer(blob): L['rpm'].add(int(m.group(1)))
            for m in RPD.finditer(blob): L['rpd'].add(int(m.group(1)))
            for m in TOKS.finditer(blob): L['free_token_claims'].add(m.group(0).strip())
            for m in DURATION.finditer(blob): L['promo_window'].add(m.group(0).strip().lower())
            for d in normalize_promo_end(blob, ts): L['promo_end'].add(d)
            for d in domains_in(text, spans): L['domains'].add(d)
            for m in NEEDS.finditer(blob): L['access'].add(m.group(0).strip().lower())
            for m in PRIVACY_RISK.finditer(blob): L['privacy_risk'].add(' '.join(m.group(0).split()).lower())
            for m in PRIVACY_OK.finditer(blob): L['privacy_positive'].add(' '.join(m.group(0).split()).lower())
            for m in URL.finditer(blob):
                u = m.group(0).rstrip('.,;')
                if 't.co/' not in u and 'x.com/' not in u: L['endpoints'].add(u)

    ranked = []
    for std, L in leads.items():
        ev = sorted(L['evidence'], key=lambda e: (e['author'].lower() == std.split()[0].lower(), e['views']), reverse=True)
        n_ev = len(ev)
        own = len(L['_authored']) > 0
        # Score by claim density, not raw post count: a single thread that states a
        # context length, a promo end date and a privacy signal beats ten vague posts.
        claims = (1 if L['context_candidates'] else 0) \
            + (1 if L['promo_end'] else 0) \
            + (1 if (L['privacy_risk'] or L['privacy_positive']) else 0) \
            + (1 if (L['rpm'] or L['rpd']) else 0) \
            + (1 if L['free_token_claims'] else 0)
        spammy = L['_spam'] > n_ev / 2
        score = max(0, min(10, round(
            (2 if own else 0)                    # provider's own account said it
            + claims                             # up to 5 concrete, checkable fields
            + min(2, n_ev / 3)                   # corroboration across posts
            + (1 if any(e.get('full') for e in ev) else 0)   # full thread, not a snippet
            + (1 if L['domains'] else 0)         # a doc/endpoint to verify against
            - (3 if spammy else 0), 1)))                        # engagement-bait thread
        ranked.append({
            'provider': std, 'confidence': score,
            'official_seen': own, 'post_count': n_ev,
            'spam_heavy': spammy,
            'context_candidates': sorted(L['context_candidates']),
            'rpm': sorted(L['rpm']), 'rpd': sorted(L['rpd']),
            'free_token_claims': sorted(L['free_token_claims']),
            'endpoints': sorted(L['endpoints'])[:6],
            'promo_window_signals': sorted(L['promo_window']),
            'promo_end_dates': sorted(L['promo_end']),
            'domains': sorted(L['domains'])[:8],
            'access_signals': sorted(L['access']),
            'privacy_risk_signals': sorted(L['privacy_risk']),
            'privacy_positive_signals': sorted(L['privacy_positive']),
            'last_seen': datetime.datetime.utcfromtimestamp(L['_latest']).date().isoformat() if L['_latest'] else None,
            'evidence': ev[:8],
        })
    ranked.sort(key=lambda r: -r['confidence'])

    # --- verification layer -------------------------------------------------
    # X posts are claims. Anything checkable (context, promo window, privacy)
    # is only a lead until it is confirmed against the provider's own terms/docs.
    verified = {}
    if os.path.exists(VERF):
        try:
            verified = (json.load(open(VERF)).get('providers') or {})
        except Exception as e:
            print(f'warning: could not read {VERF}: {e}', file=sys.stderr)
    today = now.date()
    for r in ranked:
        v = verified.get(r['provider'])
        r['verified'] = v
        r['verification'] = 'verified' if v else 'unverified'
        if v and v.get('status'):
            r['verification'] = v['status']
        ends = [d for d in r['promo_end_dates'] if re.match(r'\d{4}-\d{2}-\d{2}$', d)]
        r['promo_expired'] = bool(ends) and all(datetime.date.fromisoformat(d) < today for d in ends)
        if r['promo_expired']:
            r['verification'] = 'expired'

    json.dump({'generated': now.isoformat(), 'source': 'x.pcstyle.dev',
               'posts_scanned': len(posts), 'leads': ranked},
              open(OUTJ, 'w'), indent=1, ensure_ascii=False)

    m = [f'# X findings (via x.pcstyle.dev)', '',
         f'- generated: `{now.isoformat()}`',
         f'- posts scanned: `{len(posts)}`',
         f'- providers with leads: `{len(ranked)}`', '',
         '> Every value below is a *lead from a public post*, not verified fact. '
         'Each claim links to the post it came from. Promotion windows are inferred '
         'from post text and dated - x.pcstyle.dev does not honour `until:`, so '
         'server-side date filtering is unavailable.', '',
         '| provider | status | conf | posts | context | promo ends | domains | privacy |',
         '|---|---|---|---|---|---|---|---|']
    ICON = {'verified': '✅', 'expired': '❌ expired', 'contradicted': '⚠️ contradicted',
            'active': '✅ active', 'unknown_third_party': '❓'}
    for r in ranked:
        ctx = ', '.join(f'{c//1000}K' for c in r['context_candidates'][:3]) or '-'
        pend = ', '.join(r['promo_end_dates'][:2]) or '-'
        if r.get('promo_expired'):
            pend += ' (EXPIRED)'
        dom = ', '.join(r['domains'][:2]) or '-'
        pv = (r.get('verified') or {}).get('privacy', {}).get('verdict')
        pr = pv or (('risk: ' + r['privacy_risk_signals'][0]) if r['privacy_risk_signals'] else
                    ('ok: ' + r['privacy_positive_signals'][0] if r['privacy_positive_signals'] else '-'))
        m.append(f"| {r['provider']} | {ICON.get(r['verification'], r['verification'])} | {r['confidence']} "
                 f"| {r['post_count']} | {ctx} | {pend} | {dom} | {pr} |")
    m += ['', '## Verified against provider sources', '',
          'Only providers with a manually checked source are listed. ' + str(len(verified)) + ' on file.', '']
    for r in [x for x in ranked if x.get('verified')]:
        v = r['verified']
        m += [f"### {r['provider']} — {r['verification']}"]
        if v.get('x_claim_verdict'):
            m.append(f"- verdict on the X claim: {v['x_claim_verdict']}")
        ft = v.get('free_tier') or {}
        for k, lbl in (('auth', 'auth'), ('limits_model', 'limits'), ('caveat', 'caveat')):
            if ft.get(k):
                m.append(f"- {lbl}: {ft[k]}")
        p = v.get('privacy') or {}
        if p:
            m.append(f"- privacy ({p.get('verdict')}): {p.get('detail')}")
            if p.get('regional_exception'):
                m.append(f"- privacy (regional): {p['regional_exception']}")
            if p.get('quote'):
                m.append(f"  > \"{p['quote']}\"\n  >\n  > — <{p.get('source')}>")
        pr = v.get('promo') or {}
        for k, lbl in (('claim', 'promo claim'), ('end', 'promo end'), ('state', 'state'),
                      ('corroboration', 'independent corroboration')):
            if pr.get(k):
                m.append(f"- {lbl}: {pr[k]}")
        if v.get('via'):
            m.append(f"- via: {v['via']}")
        m.append('')
    m += ['## Leads not yet verified', '',
          'These came only from public posts. Check the provider docs/terms before adding them to settings.json.', '']
    for r in [x for x in ranked if not x.get('verified')]:
        m.append(f"- **{r['provider']}** ({r['post_count']} posts, conf {r['confidence']}) — "
                 f"verify at: {', '.join(r['domains'][:3]) if r['domains'] else 'provider docs'}")
    m.append('')
    for r in ranked:
        m += [f"## {r['provider']}", '',
              f"- confidence **{r['confidence']}/10** | posts {r['post_count']} | last seen {r['last_seen']}"
              + (' | ⚠️ mostly promo/bait' if r['spam_heavy'] else ''),
              f"- context candidates: {', '.join(map(str, r['context_candidates'])) or 'none found'}",
              f"- rate limit: rpm={r['rpm'] or '-'} rpd={r['rpd'] or '-'}",
              f"- promo signals: {', '.join(r['promo_window_signals']) or 'none'}",
              f"- **inferred promo end**: {', '.join(r['promo_end_dates']) or 'none'}  "
              f"_(derived from post prose + post date - verify on the provider's site)_",
              f"- domains seen: {', '.join(r['domains']) or 'none'}",
              f"- access signals: {', '.join(r['access_signals']) or 'none'}",
              f"- privacy risk: {', '.join(r['privacy_risk_signals']) or 'none'}",
              f"- privacy positive: {', '.join(r['privacy_positive_signals']) or 'none'}", '']
        for e in r['evidence'][:4]:
            flag = ' `[bait]`' if e['spam_flag'] else ''
            full = ' *(full thread)*' if e.get('full') else ''
            rep = ' *(reply)*' if e.get('reply') else ''
            m += [f"  - {e['date']} @{e['author']} ({e['views']} views){rep}{flag}{full}: {e['excerpt']}",
                  f"    <{e['url']}>"]
        m.append('')
    os.makedirs(os.path.dirname(OUTM), exist_ok=True)
    open(OUTM, 'w').write('\n'.join(m))
    print(f'leads: {len(ranked)}  -> {OUTJ}')
    print(f'report: {OUTM}')

main()
