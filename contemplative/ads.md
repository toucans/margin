# Ad evidence

**An ad running three months is profitable.** Nobody subsidises a loser that
long, and no other public source separates who is making money from who is
merely posting. This is the check a problem framing passes before it is
believed.

Record per ad: the first line of the hook, the landing page headline, the price
where shown, delivery start and stop, and — where the EU exposes it — targeting
and reach. Targeting is advertisers naming the buyer with their own money,
which settles by observation what `vocabulary.md` can only count.

---

## Google — wired

The Ads Transparency Center is public and needs no login. There is no official
API for commercial ads; the only official feed is a BigQuery set limited to
political ones. Access is through Apify, added as an MCP server at user scope:

    claude mcp add --transport http --scope user apify https://mcp.apify.com

OAuth on first use — run `/mcp` and authenticate. `search-actors` finds the
Transparency Center scrapers, `call-actor` runs them. Runs consume Apify
credits.

## Meta — wired

ID review has cleared. The Ad Library API answers, and **it covers more than
the EU note assumed.**

Access is a token in `~/.config/margin/meta.env` — outside the repo, never
committed — and `contemplative/sweeps/meta_ads.py`, one stdlib-only file that
is both a CLI and the `meta` MCP server:

    python3 sweeps/meta_ads.py search "grey area drinking" --countries DK,GB

**Corrections to what was assumed above, all measured 2026-08-29:**

- `ad_type=ALL` returns **commercial** ads in every country tested — DK, DE,
  NL, GB, US, AU — not political-only outside the EU. The US and AU sweeps are
  not the dead ends the note feared.
- Targeting (`target_ages`, `target_gender`, `target_locations`) returns
  **everywhere**, not just the EU. `eu_total_reach` is the EU-only field: 100
  of 100 DK rows carried it, US and AU rows did not.
- DK commercial history reached back to 2025-11-18 — about the year the DSA
  requires, so longevity is readable directly.

**`search_type` is the whole ballgame.** `KEYWORD_UNORDERED` matches loosely:
*sober curious* in the US returned drama-short ads containing neither idea.
`KEYWORD_EXACT_PHRASE` returned the actual lane — IM8 Health, Sarah Rusbatch,
TABB for Women. Sweeping on the default silently produces noise that looks like
data.

**The token is short-lived** — the one issued expires the hour it was made, and
`fb_exchange_token` needs the app secret to trade up to sixty days. Get the
secret from the app's Settings → Basic and store it beside the token, or every
session starts by minting a new one.

## Meta — the scraper, as a second path

`curious_coder/facebook-ads-library-scraper` via Apify reads the public web UI,
so it needs no token and no ID review, and it returns `collation_count` —
Meta's own grouping of near-identical copy, which is the variant count the
sweeps want. It costs $0.75 per 1K ads. Use it where the API is awkward: it is
the fallback, not the instrument.

## Where it lands

Pull to plain JSON, index it as a corpus beside `hormozi`, query it through the
`rag` server. A rented index (Foreplay, AdSpy, BigSpy) answers one question and
keeps the answer; this one goes on answering.

## Findings

None yet.
