# Which Danish market, from public data only

**Disposable.** Written to be read once and deleted; the reusable parts are
`tools/`. Nothing here overrides `strategy.md`.

The question: pretend no market has been chosen. Score every Danish industry
against the criteria for picking a market, weight the criteria by how much they
actually matter, and see what comes out.

---

## Answer

**47008 Internethandel, postordre mv.** — Danish webshops. It ranks first, and
it ranks first under 91% of twenty thousand randomly drawn weightings, i.e.
without assuming anything about which criterion matters most.

The runner-up is **45001 Bilhandel** — car dealers — and it is closer than
comfortable. One judgment separates them. It is named at the bottom.

## Method

Everything measured comes from Danmarks Statistik's open API, no key:

- **GF11** — firms, full-time employees and turnover for 160 industries
  (DB07 127-grouping), 2019–2024. 109 of those are leaf industries.
- **REGN80** — bruttoavance in percent by sector, 2023. Used to convert turnover
  into gross profit, because turnover is not what a buyer can pay out of.

Two inputs are judgment, not data, and are marked as such in `tools/score.py`:
whether an outsider is *already* paid from a recurring budget line, and whether
the population can be enumerated. DST publishes no advertising-cost line item,
so there is no way to measure the first one. That is a real limitation.

## The criteria, and what each is worth

| Weight | Criterion | Why that weight |
|---|---|---|
| 30% | **Purchasing power** — bruttofortjeneste per firm | The one that killed medspa. Hormozi's resume-writer story: massive pain, easy to target, growing, and nobody could pay |
| 22% | **A budget line an outsider is already paid from** | `strategy.md` step 3. Without it there is no budget to move and no incumbent to displace |
| 18% | **Enough buyers** — firm count | Need ≥800 so ten to twenty clients is a small share, not a quarter of the market |
| 15% | **They cannot do it themselves** — mess × leanness | Added mid-analysis; see the caveat |
| 8% | **Growing** | Deliberately low. Hormozi: *"you can be in a normal market that's growing at an average rate and still make crazy money. Every market I have been in has been a normal market"* |
| 7% | **Enumerable** | Medspa showed a clean register is worth real time, but it is not decisive |

## Result

Real growth is nominal growth minus ~20pp of inflation over 2019–2024.

| # | Industry | Score | Bruttofortj./firm | Firms | Real growth | FTE/firm |
|---|---|---|---|---|---|---|
| 1 | **47008 Internethandel** | **0.794** | 6,9m | 2.493 | **+110p** | 3,9 |
| 2 | 45001 Bilhandel | 0.736 | 15,8m | 2.348 | +15p | 9,9 |
| 3 | 58002 Computerspil og software | 0.687 | 15,6m | 995 | +59p | 8,9 |
| 4 | 41000 Byggeentreprenører | 0.684 | 11,5m | 3.993 | −1p | 6,4 |
| 5 | 77000 Udlejning og leasing | 0.655 | 9,8m | 3.486 | +26p | 2,3 |
| 6 | 46004 Engros, tekstil og bolig | 0.651 | 16,7m | 3.882 | +10p | 11,3 |
| 7 | 47005 Detailh. tekstil og bolig | 0.644 | 5,4m | 6.301 | +5p | 6,7 |
| 9 | 55000 Hoteller | 0.621 | 8,6m | 1.742 | −6p | 9,0 |

Industries eliminated by the two hard filters are as informative as the winner.
**Læger og tandlæger** (19.545 firms, 2,2 mio turnover each), **frisører**
(11.980, 1,2 mio), **restauranter** (12.480, 4,9 mio) and **virksomheds-
konsulenter** (14.547, 6,2 mio) all fail on purchasing power — plenty of buyers,
none who can pay. At the other end, **skibsfart** (1.172 mio per firm, 319 firms)
and **telekommunikation** (145 mio, 303 firms) fail for the reason medspa failed:
too few buyers.

## Why webshops win

**They are the only industry that is simultaneously rich, lean and growing.**
57,4 mia DKK of turnover across 2.493 firms and only 9.772 full-time employees —
**5,9 mio DKK of revenue per employee.** At 3,9 employees per firm there is
nobody inside to do this work. That is the whole thesis in one ratio: enough
money to pay, too few people to do it in-house.

And the trend is sharper than the level:

| | 2019 | 2024 |
|---|---|---|
| Firms | 2.341 | 2.493 (peak 2.808 in 2021) |
| Turnover | 25,0 mia | 57,4 mia |
| Turnover per firm | 10,7 mio | **23,0 mio** |

Firm count peaked in 2021 and has fallen 11% since, while turnover more than
doubled. The market is consolidating: fewer webshops, each much larger. Two
consequences. The survivors are precisely the ones who can afford a retainer,
and the shakeout itself is the pain — a shop that could not tell which channel
lost money is a shop that did not survive to 2024.

It also settles the original instinct honestly. Running a webshop *is*
winner-take-all, and the falling firm count is that curve made visible. Selling
to the winners is the opposite trade.

## The judgment the answer hangs on

Bilhandel beats webshops on the single heaviest criterion: **15,8 mio DKK of
gross profit per firm against 6,9.** Car dealers are more than twice as rich,
just as numerous, just as findable, and they do buy advertising with a broken
attribution story, because the close happens offline in a showroom.

Webshops win because of the criterion added late: **is the number hard to
produce?** A dealer's DMS already knows the margin on every car. No returns, no
shipping subsidies, no SKU explosion, no COGS buried in the wrong month. The
messy half — the half that is the moat and the reason this is a retainer rather
than a one-off — does not exist there.

Remove that criterion and **bilhandel wins.** Double the weight on purchasing
power and **bilhandel wins.** Strip out all three judged criteria and leave only
the measured ones and *engroshandel* wins, which is obviously wrong — wholesalers
have no ad budget at all, which is exactly what the measured data cannot see.

So the honest statement is: webshops are the right market **if** the mess is the
moat. `strategy.md` step 5 already asserts that. This scan does not prove it —
it shows that it is the load-bearing assumption, and that nothing else in the
Danish economy scores better under it.

## Caveats

- The moat criterion was added after seeing the first ranking, which put
  bilhandel first. That is the honest order of events. It is defensible on the
  grounds that `strategy.md` argued it before this scan existed, but a criterion
  invented after seeing results deserves the suspicion.
- Bruttofortjeneste per firm is turnover per firm times a *sector* margin, so it
  is an average over an industry that is not uniform. Real per-company figures
  are available and should replace it — `tools/bfj.py` pulls them.
- DST publishes no advertising line, so the second-heaviest criterion is entirely
  judged. It is the weakest part of this.
- 2024 GF11 figures are provisional in places.
