# Medspa — candidate market

**Status: evaluated, not adopted.** Danish webshops remain the business. This
file exists so the option can be killed or adopted on evidence instead of mood.
Nothing here is a commitment.

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

Not run yet, 2026-08-08. Everything below waits on it.

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

## The ceiling problem — the real objection

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

Any one of these ends it. Record the date here when it fires.

- Ad Library check shows the 40 chains barely advertising.
- Fewer than 40 companies clear a bruttofortjeneste bar supporting 10k DKK/month.
- 100 researched first touches produce no call.

## Open

- Danish supply/demand. Unverified. Blocks everything.
- Whether clinics buy advisory at all, or file it as an accountant task.
- What a Danish clinic actually spends on Meta per month. If it is 20k DKK, a
  15k DKK/month retainer to measure it is absurd on its face.

Contacts, prices and how anyone opens go in `contact.md`, not here.
