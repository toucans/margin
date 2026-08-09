"""Weighted scorecard over Danish industries.

Measured from DST: bruttofortjeneste/firm, firm count, 5-yr growth.
Judged by hand (marked JUDGED): whether an outsider is already paid from a
measurable budget line, and whether the population is enumerable.
"""
import csv, collections

# --- weights, and why -------------------------------------------------------
W = {
    "koebekraft": 0.30,   # what killed medspa; Hormozi's resume-writer story
    "budgetlinje": 0.22,  # ecommerce.md step 3 - an outsider already paid from it
    "kanikkeselv": 0.15,  # messy enough to be hard, lean enough to outsource
    "antal": 0.18,        # need >=800 so 10-20 clients is a small share
    "vaekst": 0.08,       # Hormozi: a normal market is fine
    "findbar": 0.07,      # medspa showed a clean register is worth real time
}

# JUDGED, 0-1. Does producing the number require reconciling messy,
# business-specific data the client's own systems do not already spit out?
ROD = {
    "47008": 1.00, "47005": 0.85, "47007": 0.85, "46004": 0.70, "46003": 0.70,
    "46006": 0.70, "46007": 0.70, "46005": 0.70, "46001": 0.55, "55000": 0.60,
    "47001": 0.60, "41000": 0.60, "42000": 0.60, "43001": 0.60, "58002": 0.50,
    "78000": 0.50, "62000": 0.50, "71000": 0.50, "25000": 0.50, "28002": 0.50,
    "33000": 0.45, "49003": 0.45, "52000": 0.45, "53000": 0.45, "69001": 0.40,
    "63000": 0.40, "77000": 0.40, "35001": 0.30, "45002": 0.35, "72000": 0.35,
    "58001": 0.45,
    "45001": 0.25,  # DMS already knows margin per car: no returns, no shipping,
                    # no SKU explosion. The hard half of the job is missing.
}

# sector gross margin %, DST REGN80 2023
MARGIN = {"45": .19, "46": .22, "47": .30, "55": .69, "56": .69, "35": .12,
          "41": .43, "42": .43, "43": .43, "25": .47, "28": .47, "33": .47,
          "62": .70, "63": .70, "58": .70, "71": .77, "69": .77, "70": .77,
          "72": .77, "77": .79, "78": .65, "49": .68, "52": .68, "53": .68}

# JUDGED, 0-1. Is there a recurring budget line, paid to an outsider, whose
# performance is arguable? And can the population be enumerated?
BUDGET = {
    "47008": (1.00, "media agency paid from ad spend; ROAS is the metric and it is wrong"),
    "45001": (0.90, "Bilbasen listing fees + Meta/Google; close is offline so attribution breaks"),
    "55000": (0.80, "OTA commission is literally a CAC line, but contractual not optimisable"),
    "58002": (0.70, "big user-acquisition spend, but sophisticated and often in-house"),
    "47005": (0.60, "advertises, but online-to-store attribution is a harder problem"),
    "47007": (0.60, "same"),
    "78000": (0.60, "buys both candidate and client leads"),
    "63000": (0.50, "mixed"),
    "58001": (0.50, "mixed"),
    "47001": (0.50, "chains, in-house marketing teams"),
    "77000": (0.50, "some lead buying"),
    "35001": (0.40, "retailers advertise, but the count is mostly grid companies"),
    "45002": (0.40, "local lead gen, small budgets"),
    "41000": (0.35, "buys leads, small budgets - ecommerce.md already cut haandvaerkere"),
    "42000": (0.35, "mostly tender"),
    "43001": (0.35, "same"),
    "69001": (0.30, "some, mostly referral"),
    "53000": (0.20, "little"),
    "62000": (0.20, "they are the outsiders; referral and tender"),
    "46001": (0.15, "agency trade, no consumer ad spend"),
    "46003": (0.15, "sells through reps and relationships"),
    "46004": (0.15, "same"), "46005": (0.15, "same"),
    "46006": (0.15, "same"), "46007": (0.15, "same"),
    "71000": (0.15, "tender and referral"),
    "49003": (0.10, "no"), "52000": (0.10, "no"),
    "25000": (0.10, "no"), "28002": (0.10, "no"), "33000": (0.10, "no"),
    "72000": (0.05, "no"),
}
FINDBAR = {
    "45001": 0.95, "55000": 0.95, "47008": 0.85, "47007": 0.80, "47005": 0.80,
    "47001": 0.85, "69001": 0.90, "71000": 0.85, "62000": 0.70, "45002": 0.85,
    "58001": 0.70, "58002": 0.60, "78000": 0.75, "35001": 0.60, "63000": 0.50,
    "77000": 0.50, "41000": 0.60, "42000": 0.60, "43001": 0.60, "25000": 0.50,
    "28002": 0.50, "33000": 0.45, "49003": 0.55, "52000": 0.45, "53000": 0.55,
    "72000": 0.40, "46001": 0.40, "46003": 0.45, "46004": 0.45, "46005": 0.45,
    "46006": 0.45, "46007": 0.40,
}

rows = list(csv.reader(open("gf11.csv", encoding="utf-8-sig"), delimiter=";"))[1:]
D, name = collections.defaultdict(dict), {}
for br, unit, tid, val in rows:
    code = br.split(" ", 1)[0]
    name[code] = br.split(" ", 1)[1] if " " in br else br
    try:
        D[code][(unit.split(" ")[0], tid.split(" ")[0])] = float(val)
    except ValueError:
        pass

INFLATION = 20.0  # Danish CPI, 2019 -> 2024, approx
cands = []
for code in BUDGET:
    d = D[code]
    f, t, t0 = d.get(("AFI", "2024")), d.get(("OMS", "2024")), d.get(("OMS", "2019"))
    e = d.get(("AFU", "2024")) or 0
    m = MARGIN.get(code[:2], .45)
    bfj = (t / f) * m                          # mio DKK gross profit per firm
    g = (t / t0 - 1) * 100 - INFLATION         # real growth, pct points
    cands.append(dict(
        code=code, name=name[code], firms=int(f), bfj=bfj, real=g,
        fte=e / f,
        s_koeb=min(bfj / 12, 1.0),             # 12 mio DKK bfj saturates
        s_antal=min(f / 4000, 1.0),            # 4000 firms saturates
        s_vaekst=max(0, min((g + 10) / 60, 1)),
        s_budget=BUDGET[code][0], s_findbar=FINDBAR[code],
        s_kanikkeselv=ROD[code] * max(0.4, min(1.0, 1 - (e / f - 5) / 33)),
        rod=ROD[code], why=BUDGET[code][1]))

for c in cands:
    c["score"] = (W["koebekraft"] * c["s_koeb"] + W["budgetlinje"] * c["s_budget"]
                  + W["kanikkeselv"] * c["s_kanikkeselv"]
                  + W["antal"] * c["s_antal"] + W["vaekst"] * c["s_vaekst"]
                  + W["findbar"] * c["s_findbar"])

cands.sort(key=lambda c: -c["score"])
print(f"{'':2} {'code':>5} {'industry':<44} {'score':>6} {'bfj/firm':>9} "
      f"{'firms':>6} {'real g':>7} {'FTE':>5} {'rod':>5}")
print("-" * 92)
for n, c in enumerate(cands[:18], 1):
    print(f"{n:>2} {c['code']:>5} {c['name'][:44]:<44} {c['score']:>6.3f} "
          f"{c['bfj']:>8.1f}m {c['firms']:>6} {c['real']:>+6.0f}p {c['fte']:>5.1f} "
          f"{c['s_kanikkeselv']:>5.2f}")
print("\nTop three, the judged input that drives them:")
for c in cands[:3]:
    print(f"  {c['code']} {c['name'][:34]:34s} budget={c['s_budget']:.2f}  {c['why']}")
