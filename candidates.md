# Candidate markets

Not the business. `strategy.md` is. This is a working file for evaluating
alternatives to it, and it gets **deleted** when the question is answered — the
commit history is the record, the way medspa was handled.

**Everything here fails P5 today.** Content comes from work actually done, and I
have no clients in any of these. Nothing below is actionable before the first
three margin clients exist; it is written down so it doesn't have to be re-derived
later, not so it can be started now.

---

## The four filters

A niche qualifies as *content-led, not winner-take-all, above-median earns
multiples* if all four hold. Any one failing is disqualifying, not a discount.

1. **Expensive and rare** for the buyer — they research instead of habituate.
2. **They will never do it themselves** — so teaching how it *works* sells the
   work, rather than replacing it. Hormozi's declarative/procedural split:
   declarative is what you use to sell, procedural is what you sell.
3. **Delivery is capacity- or trust-bound** — no aggregator can take it all.
4. **Prices are not comparable** — the test is whether two providers can charge
   5× different and both stay busy. Where they can't, the market prices everyone
   at the point of burnout.

A fifth, learned from Hormozi and not in the original four: **does the buyer stop
buying?** Retention is set by what you sell, not how well. People keep a cleaner
and cancel a gym.

---

## 1. One large asset, decided once a decade

Property purchase and renovation, architecture, bygherrerådgivning on a private
build, farmland and forestry, a boat.

| Filter | Verdict |
|---|---|
| Expensive and rare | **Passes hard.** Six to seven figures, once a decade, catastrophic if wrong |
| Never do it themselves | **Passes.** They must understand enough to choose, and will never build it |
| Capacity/trust-bound | **Passes.** Fully fragmented, no marketplace, referral-driven |
| Prices incomparable | **Mostly.** Architecture yes. Køberrådgivning no — it is already fixed-fee and quoted against |

**What kills it: no ongoing wrongness.** `strategy.md` step 4 — retainers come
from the number decaying, not from ongoing work. A one-off decision is a project
fee, and then the client is gone forever with no reason to return. This is the
single worst structural fit with everything else I've decided.

**The only version that survives** is advising someone who does this repeatedly —
a portfolio owner, a developer, a family office — which is a tiny population and
is B2B, i.e. the thing I already do.

**Not pursued.** Fails the retainer test, which is upstream of the four filters.

---

## 2. Self-paid health with a visible outcome

Fertility, tandimplantater, hårtransplantation, private scanning and diagnostics,
sports rehabilitation.

| Filter | Verdict |
|---|---|
| Expensive and rare | **Passes hard.** Pain and money overlap perfectly here |
| Never do it themselves | **Passes** |
| Capacity/trust-bound | **Passes hard.** A practitioner's calendar is the ceiling |
| Prices incomparable | **Passes.** Enormous quality spread the buyer believes in |

Best scores on the filters of anything considered. And it collapses anyway,
because there are only two ways in:

- **Be the practitioner.** Requires a clinical licence I do not have and will not
  get. This is not a market-selection question, it is a career question.
- **Serve the clinics.** *Already dead.* Kosmetiske klinikker were measured and
  killed on market size — 15 firms clearing 3 mio. — in `strategy.md`'s buyer
  test. Same finding, same numbers, and re-opening it needs new information, not
  a new mood.

**Not pursued.** The half that passes the filters isn't available to me, and the
half that is available is already cut.

---

## 3. Children's outcomes — language learning

The one I actually want to look at. Verdict first: **generic children's language
tutoring is the worst member of this family, not the best, and it fails three of
the four filters on measured evidence.** Something narrower survives.

### Why the obvious version fails

**Prices are published and comparable.** Superprof Denmark averages ~259 kr/t
across 1.249 online tutors, with the market range roughly 85–450 kr/t. When a
platform can publish an average, filter 4 is gone — that is a price index, and it
is what the point of burnout looks like.

**The aggregator already exists and is winning.** Preply: 100.000+ tutors,
$1,2 mia. valuation on a $150M Series D in January 2026. Commission starts at
**33%** for new tutors, sliding to 18% only past 400 hours taught, and the first
trial lesson with each new student pays the tutor **nothing**. italki raised its
commission from 15% to 21%. That is textbook aggregator power over commoditised
supply, and it is tightening, not loosening.

**It is neither expensive nor rare.** A weekly lesson is a small recurring
purchase, habituated not researched. Filter 1 gone.

**And retention is gym-shaped.** The family moves, the exam ends, the child
resists, the priority shifts. Compare a cleaner, which people keep for years.
What is being sold sets the churn, and this sells like a gym.

Filter 2 is the only clean pass: parents will not teach it themselves.

### What survives, in order

**a) The relocation package — and this is the strongest thing in the file.**
The accompanying family of a relocated executive needs Danish, and the *employer*
pays. That converts the entire proposition from disposable income to a **committed
budget line**, which is P6 — the same reason ad spend beat every other webshop
decision. It is also naturally bounded, deadline-driven, and quoted against
relocation agencies rather than against 259 kr/t.

*Unverified, and this is what to check first:* how many corporate relocations into
Denmark per year, who currently supplies the language component, and whether it is
already bundled into the relocation contract at a price that leaves nothing.

**b) International school admission.** 31 international schools in Denmark; the
sought-after IB ones run waiting lists from six months to over a year. Gated,
binary, deadline-bound, high-stakes — the shape that makes deep content pay.
*Caveat that weakens it:* most Danish international schools receive a state
subsidy and pass part of it on, so headline fees are lower than the salary level
implies. The affluent-buyer premise is materially weaker here than in London or
Singapore.

**c) Heritage-language maintenance for mobile high-income families.** Parents who
expect to move again and need the child to hold a language for a future school
entry. Rare in that it is a multi-year commitment, and it is the one variant with
both high stakes *and* recurrence.

### What would have to be true

Ranked by what kills it fastest:

1. The employer, not the parent, is the payer in (a). If it turns out parents pay,
   this is disposable income and drops to the bottom.
2. The population is enumerable — relocating employers, or families at 31 named
   schools. If the list can't be built, it dies the way any unenumerable market
   dies.
3. Price survives contact with 259 kr/t. If a prospect ever compares the two, the
   positioning failed, and no amount of content fixes it.
4. Denmark is big enough. Almost certainly the binding constraint on all three,
   and the one `score.py` exists to answer.

---

## Standing rule for this file

Nothing here gets a day of work before three margin clients exist. If one of these
is still interesting then, it goes through `score.py` against DST data the way
medspa and bilhandel did — measured, not reasoned — and the losers get deleted
with the reason in the commit message.
