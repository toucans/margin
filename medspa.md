# Medspa — candidate market

**Status: KILLED 2026-08-08, on market size.** Danish webshops remain the
business. Kept as a record so it is not re-derived from scratch in six months,
and because the list method below is reusable.

**What killed it.** The 523 companies were joined to their published accounts.
Roughly **15 genuine clinics have a bruttofortjeneste above 3M DKK** — the
rough floor for a 10k DKK/month retainer to be anything other than absurd. The
pre-registered criterion was forty. Detail under *The join*.

Un-killing requires new information named in the commit message. A better
message is not new information.

**Read `strategy.md` first.** How the business runs — offer architecture,
guarantee, outreach cadence, pricing, the cut list — applies unchanged. This
file records only what is *different*. Where the two disagree, `strategy.md`
wins until this one is promoted.

---

## What decides it

One question: **are Danish cosmetic clinics supply- or demand-constrained?**

The US read is supply-constrained with near-zero CAC — owners at $6M topline who
"put the sign up and people came in." If that holds in Denmark, measurement is
not the pain and the offer does not land. If it does not hold, they are buying
customers and do not know what one is allowed to cost.

**The test is free.** Run the 40 multi-site operators through Meta Ad Library,
filtered to DK.

- Little or no sustained creative → supply-constrained → the offer is wrong for
  this market as written, and the real opportunity is paid acquisition, which is
  not what I sell.
- Sustained multi-creative activity → demand-constrained → the offer transfers.

Never run — the size question below answered first and cheaper. Noted because
the test itself is sound and reusable on any list keyed by CVR.

## The list — better than the webshop list

Statutory and exhaustive. Anyone performing kosmetisk behandling must register
with Styrelsen for Patientsikkerhed.

**Source:** Behandlingsstedsregisteret — `stps.dk` → *Dataudtræk om
behandlingssteder*. One xlsx, free, 19.820 rows. Filter `Enhedstype = "Kosmetisk
klinik"`.

It carries **CVR-nummer** on the same row as name, address, kommune and website.
So the CVR × Ad Library join needs no fuzzy name matching here — it is a direct
key. That is the one thing genuinely easier than webshops, where the list has to
be assembled from Trustpilot, Shopify footprints and FDIH.

As of the 03-08-2026 extract:

| | |
|---|---|
| Sites | 644, all private |
| Companies, distinct CVR | 523 |
| Multi-site operators | 40, covering 161 sites |
| Website listed | 319 of 644 |
| København / Aarhus / Frederiksberg | 137 / 52 / 47 |

The category is noisy — a neurophysiology clinic registers as one, presumably
botox for migraine. Eyeball before touching.

The extract is a regenerable cache. Rebuild it from the xlsx; do not commit it.

## The join — how the market was sized

Two public, unauthenticated endpoints. No key, no scraping, no vendor.

- `distribution.virk.dk/offentliggoerelser/_search?q=cvrNummer:<cvr>` — which
  annual reports exist, with a link to the XBRL.
- `regnskaber.virk.dk/…xml` — the report itself. Tag `GrossProfitLoss` is
  bruttofortjeneste; `EmployeeBenefitsExpense` is personaleomkostninger, a decent
  capacity proxy. Match `contextRef` to the reporting period or you read last
  year's figure.

Same join works on the webshop list. It is the missing half of the ranking in
`strategy.md` — that section describes reading bruttofortjeneste off CVR by hand.
This does all of them in ten minutes.

Result across the 523, latest filed accounts (mostly FY2025):

| | |
|---|---|
| File accounts with a gross-profit line | 209 |
| File no annual report at all | 283 |
| Median bruttofortjeneste of those 209 | 487.830 DKK |
| ≥ 3M DKK | 20 companies |
| ≥ 5M DKK | 11 |
| ≥ 10M DKK | 6 |

The 283 non-filers are personally owned — sole traders do not file — so they are
one room and one pair of hands. That is over half the register.

Of the 20 above 3M, four or five are not medspas at all: a medical-supply
distributor, a skincare manufacturer, a private hospital, a dermatology practice.
**Roughly fifteen real ones.** The largest by a distance is N'AGE at 64,8M, then
CeriX at 31,4M; below the top six it falls off a cliff.

## The ceiling problem — confirmed by the join

523 companies, not a few thousand. At twenty first touches a day the **entire
market is contacted in about five weeks.**

That cuts both ways. Complete coverage is achievable, so the demand question gets
a definitive answer instead of a statistical one. But there is no room for a bad
message: burn the list and the cycle is three months.

Worse, most of the 523 are one nurse in one room and cannot pay 10–25k DKK/month.
The plausible pool is the 40 chains plus whatever single sites clear the bar on
bruttofortjeneste — call it 40–80 companies. Ten to twenty clients out of that is
a 25–50% share of the addressable market, against under half a percent for
webshops.

**This is the strongest argument against the market, and it is checkable now**
by joining the 523 CVRs to datacvr.virk.dk. Do that before any outreach.

## What would be sold

Not allowable CAC as written. Two candidates, same craft, different inputs:

1. **Contribution margin per treatment, and the attach rate.** The popular
   treatments are the least profitable; the entry treatment can lose money and
   only works if the upsell covers it. Returns and shipping drop out; attach rate
   and service mix replace them. Cohort survives. Closest to what is already
   sold.
2. **Utilisation — sessions per hour per technician.** Needs the booking system
   plus the ledger, so the both-halves moat holds.

The Danish localisation moat is unchanged. Kontoplan, moms, e-conomic and Dinero
are a Danish SMB moat, not an ecom one.

**Not sold: technician pay and retention.** Real problem, and the one the
category talks about. But it is not provable on their data in a week and not
sellable without a track record in the category. The destination, never the
offer.

The tracking front-end transfers unchanged in role, and the differentiation claim
is stronger here than in ecom. The work shifts from purchase events to booking
events plus offline conversion import from the booking system.

## Kill criteria

- ~~Ad Library check shows the 40 chains barely advertising.~~ Never run. The
  size question landed first and made it moot.
- **Fewer than 40 companies clear a bruttofortjeneste bar supporting 10k
  DKK/month. → FIRED 2026-08-08. About fifteen.**
- ~~100 researched first touches produce no call.~~ Not reached.

The criterion was written down before the data was pulled. That is the only
reason to trust the answer.

## The American version — considered, does not reopen

Ten to fifteen thousand US medspas against fifteen Danish ones is a real
argument, and it is the obvious response to the number above. It still loses,
on grounds already in `strategy.md` → *Why Denmark*.

The moat is the localisation cost — kontoplan, moms, e-conomic, Dinero. In the
US that knowledge is QuickBooks and a US chart of accounts, which every American
bookkeeper already has. Same learning cost, no advantage bought. It converts the
only defensible position into a red ocean where the sole edge is price, which is
P9's no-floor case.

Against it also: no local-trust discount on a cold approach, no referrals, no
case studies, US agencies already swarming that buyer, and sales calls at 22:00
CET for years.

The rule stands unchanged — **reopen geography when capacity, not demand, is
what stops me.** Zero clients is not a capacity problem. Nothing found here is
new information about geography; it is information about a vertical.

## What this leaves

Danish webshops, unchanged, for the reason the join makes concrete: a few
thousand of them, where ten to twenty clients is under half a percent rather
than a quarter of the market.

Two things were worth the detour and are kept:

- **The bruttofortjeneste join above.** Point it at the webshop list.
- Medspa is a **capacity** business, webshops a goods-margin one. Naming that
  sharpened what is actually being sold: not a number, but the specific
  arithmetic of one kind of business.

Contacts, prices and how anyone opens go in `contact.md`, not here.
