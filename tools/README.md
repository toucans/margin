# Tools, and what public data is actually reachable

For the list and the ranking described in `../strategy.md`. That file says what
is sold and to whom; this one says where the data comes from and what has to be
asked for.

Nothing here is a source of truth. Every output is a regenerable cache — rebuild
it, don't commit it.

---

## The four tiers

**1. Public, open API, works today.** No key, no account.

| Source | Gives | Tool |
|---|---|---|
| `distribution.virk.dk/offentliggoerelser` + `regnskaber.virk.dk` | bruttofortjeneste, personaleomkostninger, omsætning per CVR, from the filed XBRL | `bfj.py` |
| `api.statbank.dk` (DST) | firms, turnover, employees per branche, 2019– | `scan.py`, `score.py` |
| `cvrapi.dk` | name → CVR, branchekode, employee band, address. Rate-limits hard | — |

This tier answers **can they pay**, which is the question that killed two markets.
It cannot answer who they are.

**2. Public, but behind a free account you have not opened.** Both are signups,
not technical problems, and both are blocking.

- **CVR bulk by branchekode** — `distribution.virk.dk/cvr-permanent` returns 401.
  Access is free from Erhvervsstyrelsen but requires registering. **This is the
  single missing piece: it is the whole list of 2.493 webshops in one query.**
  Everything downstream is built and waiting for it.
- **Meta Ad Library API** — `ad_type=ALL` returns ordinary commercial ads for EU
  countries, so Denmark qualifies where most of the world does not. Needs a
  developer app plus government-ID verification and a token that expires every
  60 days. The web UI works by hand today for a few dozen names.

**3. Public, but only if you assemble it yourself.** There is no statutory
register of webshops — the clinics had one, this market does not. The list has to
be built from Trustpilot, e-mærket, FDIH and platform footprints, and then each
name enriched from its own site. That enrichment is `probe.py`.

**4. Only from the client.** No amount of public data substitutes.

- COGS per SKU
- Returns per SKU **with dates** — the timing is the whole problem
- Payment fees, from the PSP settlements
- Shipping actually paid, against shipping charged
- Ad spend per channel
- Order lines with dates and a customer id, for cohorts

**That split is the business.** Tiers 1–3 rank the list and open the
conversation. Only tier 4 produces the number. If the number could be computed
from public data, it would already be software.

---

## `bfj.py` — can they pay

    python3 bfj.py <list.csv> [out.csv]

Any CSV with a `cvr` column. Class B firms merge everything above
bruttofortjeneste, which is the figure wanted; class C firms publish a full P&L
and often omit that line, hence the revenue fallback. **Sole traders file
nothing** — an empty result means too small to be an ApS, not missing data.

## `probe.py` — who they are, before contact

    python3 probe.py coolshop.dk proshop.dk ...

Reads the front page plus the usual terms pages. Returns platform, tracking
stack, consent layer, whether server-side GTM is running, the free-shipping
threshold and the return window.

Measured on six live Danish shops: Magento dominant, GTM on all six, Cookie
Information on four, **server-side GTM on none**. Return windows ranged from 14
to 365 days.

**Caveat that matters:** tags usually load only after consent, so an absent Meta
pixel is not evidence of no Meta pixel. Read a positive as a fact and a negative
as unknown.

## `scan.py`, `score.py` — which market

Filter and rank every Danish industry from DST. Kept because the method is
reusable, not because the market question is open. Fetch instructions are in
`scan.py`'s docstring.

---

## What outreach needs per name

Five fields. Four are free today; the fifth is why tier 2 blocks.

1. CVR, company name, domain
2. **bruttofortjeneste** — ranks the list, decides who is worth a researched touch
3. **Evidence of ad spend** — sustained creatives and how long each has run
4. **One number about them, off public record** — the first line of the message
5. A contact route, usually the owner on LinkedIn

For (4) the public candidates, best first:

- **Return window against the returns-timing problem.** A shop advertising 365
  days is booking returns up to a year after the sale. That is the pitch, in
  their own published terms, and it costs nothing to find.
- **Free-shipping threshold** against a plausible basket — a threshold set below
  contribution margin is a subsidy they chose and did not price.
- **Sustained Meta activity against published bruttofortjeneste** — what share of
  gross profit is going to Meta. Needs tier 2.

The first two work right now, on any domain, with no account.
