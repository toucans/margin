"""Filter every Danish industry down to those that could sustain a high-price,
low-client-count practice. Source: DST GF11 - firms, full-time employees and
turnover by DB07 127-grouping, 2019-2024. Open API, no key.

Fetch the input first:

    curl -X POST https://api.statbank.dk/v1/data \\
      -H 'Content-Type: application/json' \\
      -d '{"table":"GF11","format":"CSV","valuePresentation":"CodeAndValue",
           "variables":[{"code":"BRANCHEDB071019127","values":["*"]},
                        {"code":"MAENGDE4","values":["*"]},
                        {"code":"Tid","values":["*"]}]}' -o gf11.csv

(the second variable code carries a Danish AE ligature; copy it from
https://api.statbank.dk/v1/tableinfo/GF11?format=JSON if the shell mangles it)

score.py then ranks what survives. This one only filters.
"""
import csv, collections

rows = list(csv.reader(open("gf11.csv", encoding="utf-8-sig"), delimiter=";"))[1:]
D = collections.defaultdict(dict)          # branche -> (unit, year) -> value
name = {}
for br, unit, tid, val in rows:
    code = br.split(" ", 1)[0]
    name[code] = br.split(" ", 1)[1] if " " in br else br
    u = unit.split(" ", 1)[0]
    y = tid.split(" ")[0]
    try:
        D[code][(u, y)] = float(val)
    except ValueError:
        pass

YR, BASE = "2024", "2019"
out = []
for code, d in D.items():
    f = d.get(("AFI", YR))          # firms
    t = d.get(("OMS", YR))          # turnover, mio DKK
    e = d.get(("AFU", YR))          # full-time employees
    f0, t0 = d.get(("AFI", BASE)), d.get(("OMS", BASE))
    if not f or not t or f < 50:
        continue
    out.append(dict(
        code=code, name=name[code], firms=int(f),
        oms=t, oms_pr_firma=t / f,
        fte_pr_firma=(e / f) if e else 0,
        vaekst=((t / t0 - 1) * 100) if t0 else None,
    ))

# 127-grouping leaf codes are numeric; letters/aggregates are roll-ups.
leaves = [r for r in out if r["code"].isdigit() and len(r["code"]) >= 5]
print(f"leaf industries: {len(leaves)}  (of {len(out)} rows incl. aggregates)\n")

DKK = lambda v: format(int(v), ",d").replace(",", ".")

def band(r):
    """Firms big enough to pay 120-300k DKK/yr, and enough of them."""
    return r["oms_pr_firma"] >= 8 and r["firms"] >= 800

print("=" * 108)
print("PASS THE TWO HARD FILTERS: >=800 firms  AND  >=8 mio DKK turnover/firm")
print("=" * 108)
print(f"{'code':>5} {'industry':52s} {'firms':>7} {'oms/firm':>9} {'FTE/f':>6} {'growth':>8}")
cand = sorted([r for r in leaves if band(r)], key=lambda r: -r["oms_pr_firma"])
for r in cand:
    g = f"{r['vaekst']:+.0f}%" if r["vaekst"] is not None else "  n/a"
    print(f"{r['code']:>5} {r['name'][:52]:52s} {r['firms']:>7} "
          f"{r['oms_pr_firma']:>8.1f}m {r['fte_pr_firma']:>6.1f} {g:>8}")

print(f"\n{len(cand)} of {len(leaves)} industries pass.\n")

print("=" * 108)
print("FAIL ON SIZE ONLY (>=8 mio/firm but under 800 firms) - too few buyers")
print("=" * 108)
for r in sorted([r for r in leaves if r["oms_pr_firma"] >= 8 and r["firms"] < 800],
                key=lambda r: -r["oms_pr_firma"])[:12]:
    print(f"{r['code']:>5} {r['name'][:52]:52s} {r['firms']:>7} {r['oms_pr_firma']:>8.1f}m")

print("\n" + "=" * 108)
print("FAIL ON PURCHASING POWER (many firms, but too small to pay)")
print("=" * 108)
for r in sorted([r for r in leaves if r["firms"] >= 2000 and r["oms_pr_firma"] < 8],
                key=lambda r: -r["firms"])[:14]:
    print(f"{r['code']:>5} {r['name'][:52]:52s} {r['firms']:>7} {r['oms_pr_firma']:>8.1f}m")
