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

**Tokens last sixty days, and renewing one is a single command.** The Ad
Library refuses app tokens and system-user tokens outright — `code 10,
subcode 2332004`, *App role required*. It is gated behind an ID-verified
person on purpose, so there is no never-expiring credential to be had. The
long-lived user token is the whole of the durable path:

    # Graph API Explorer -> app "breeze" -> Generate Access Token, then:
    python3 sweeps/meta_ads.py exchange <fresh-short-token>
    python3 sweeps/meta_ads.py status      # prints hours left

Exchange a token while it is *fresh*. A near-expiry token failed the exchange
repeatedly with a transient-flagged error that never cleared; a newly minted
one traded for sixty days on the first try. If it errors, re-mint before
debugging the app.

`exchange` refuses to write a short or empty response over the existing token.
That guard exists because the naive version wiped a working token when a failed
call fell through to the file write.

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

Swept 2026-08-29 via the Ad Library API: 291 keyword queries (8 clusters ×
6 countries, Denmark-only for C8), active and inactive passes, 163,508 ads
returned, 0 query errors. Machinery and raw CSV in `sweeps/`.

**The buyer is not settled, so read these as a menu.** Founders and operators are
the working hypothesis in `contemplative.md`, not a decision. Scored that way, the
result is uncomfortable: **the strongest markets found here are not founder markets.**
Drinking-as-the-off-switch and the body-under-stress carry the proven money, and both
sell to women in midlife. The founder lane is real — the few in it run long — but it is
eight advertisers across 163,508 ads, the thinnest of the viable options rather than the
richest. Choosing it is choosing the harder market deliberately.

**Each framing drags its own audience along.** Drinking brings midlife women. Nervous
system brings trauma and parenting. Burnout named for a role brings executives. Nobody
reaches a founder through the mechanism; they reach them through the habit or the job
title. That is the same rule `contemplative.md` already states — *the problem you lead
with is the business you get* — now with the audiences attached by observation.

**§0.1 resolved to API, and the API was not the constraint.** Every country
returned commercial ads. The DK/DE/NL-carry-the-study worry was unfounded.

**C2 is the live market, not C1.** *Can't switch off* is the deepest cluster by
a distance — 41 advertisers survived triage, with runs of 191, 160, 159, 151,
124 days. The 2 a.m. decision (C1) has almost no one selling against it: what
looks like C1 volume is hypnotherapists and bathroom fitters whose copy happens
to contain *spiralling*. **The framing johan leads with is the one nobody has
priced.** That is either the opening or the warning — this sweep cannot tell
which, only that the money is next door.

**C5 confirms the method.** Sarah Rusbatch ran one creative 123 days in GB and
AU at once — *"relying on that evening glass of wine more and more to switch off
at the end of the day"* — into a gated application. The control passed, so a
thin cluster elsewhere is a real reading, not a coverage artifact.

**C5 also shows what a worked lane looks like.** Four separate pages — Mindful
Drinking Community, Dr. Alex Morgan, Alcohol Free Daily, Ask Dr. Whitmore — run
the same hook, *"Tired of feeling held back by your drinking habits?"*, into the
same destination, `calmio.ai`, across DK DE NL GB US for 60–68 days. One
operator wearing four faces. Where a framing pays, it gets industrialised.

**C3 is empty and the emptiness is real.** One advertiser survived across all
six countries. Nobody sells against compulsive checking directly — it is a
symptom people recognise but will not buy a cure for on its own.

**Note the crossover.** Rusbatch sells *drinking* by promising *switching off*;
Rewired Woman sells *burnout* to *executive women*, 7 variants over 5 countries.
The buyer is reached through the habit or the role, not through the mechanism.

**Denmark is thin and mostly institutional.** Of 12 survivors, the unions (Djøf,
CA) and the aftenskole cycle account for most volume — flagged, not ranked, per
the seasonality trap. One real framing match: Mellem-Rummet Retreat, 194 days,
*"noget i dig, som altid er på overarbejde, aldrig kan slappe helt af"*.

**Caveats.** `price_visible` is weak: the API exposes only the display domain,
so the landing-page pass reads the domain root, not the creative's actual
destination, and the regex mistakes stray `$1` strings for prices. Treat the
price column as unread until a run through the scraper recovers true
`link_url`s. Variant counts are copy-hash groupings, not Meta's own
`collation_count`.
