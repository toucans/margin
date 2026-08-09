"""Join any list of Danish CVR numbers to their published bruttofortjeneste.

    python3 bfj.py <input.csv> [output.csv]

Input needs a `cvr` column; every other column is carried through untouched.
This is the ranking step in ecommerce.md - the one that decides which names on
the list are worth a researched first touch.

Two public, unauthenticated sources, no key and no vendor:
  1. distribution.virk.dk/offentliggoerelser  -> which annual reports exist
  2. regnskaber.virk.dk/<id>.xml              -> the XBRL itself

Pulls GrossProfitLoss (bruttofortjeneste), EmployeeBenefitsExpense
(personaleomkostninger, a decent capacity proxy) and Revenue for the latest
reporting period. Class B firms usually merge everything above
bruttofortjeneste, which is exactly the figure wanted; class C firms publish a
full P&L and often omit that merged line, hence the revenue fallback.

Caveat: sole traders file no annual report at all, so an empty result means
"too small to be an ApS", not "no data".
"""
import csv, gzip, io, json, re, sys, time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

SEARCH = "http://distribution.virk.dk/offentliggoerelser/_search?size=25&q=cvrNummer:{}"
UA = {"User-Agent": "margin-research/1.0 (7derpy@gmail.com)",
      "Accept-Encoding": "gzip"}


def get(url, timeout=45):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw


def latest_xbrl(cvr):
    """Newest annual report for cvr -> (xml_url, start, end)."""
    d = json.loads(get(SEARCH.format(cvr)))
    best = None
    for h in d["hits"]["hits"]:
        s = h["_source"]
        if s.get("offentliggoerelsestype") != "regnskab":
            continue
        per = (s.get("regnskab") or {}).get("regnskabsperiode") or {}
        end = per.get("slutDato")
        xml = next((doc["dokumentUrl"] for doc in s.get("dokumenter", [])
                    if doc.get("dokumentMimeType") == "application/xml"), None)
        if not (end and xml):
            continue
        if best is None or end > best[2]:
            best = (xml, per.get("startDato"), end)
    return best


def facts(xml_url, start, end):
    """GrossProfitLoss + EmployeeBenefitsExpense for the period [start, end]."""
    body = get(xml_url).decode("utf-8", "replace")

    # context id -> (startDate, endDate); only durations, ignore instants
    ctx = {}
    for m in re.finditer(r'<[^>]*:context[^>]*id="([^"]+)"(.*?)</[^>]*:context>',
                         body, re.S):
        cid, inner = m.group(1), m.group(2)
        if "<" in inner and "explicitMember" in inner:
            continue  # dimensional context: segment breakdowns, not the total
        sd = re.search(r"startDate>([\d-]+)<", inner)
        ed = re.search(r"endDate>([\d-]+)<", inner)
        if sd and ed:
            ctx[cid] = (sd.group(1), ed.group(1))

    def pick(tag):
        cands = []
        for m in re.finditer(
                r'<[a-zA-Z0-9]+:%s\b[^>]*contextRef="([^"]+)"[^>]*>(-?[\d.]+)<' % tag,
                body):
            cid, val = m.group(1), m.group(2)
            if cid not in ctx:
                continue
            cs, ce = ctx[cid]
            if ce == end and (start is None or cs == start):
                cands.append(int(float(val)))
        return cands[0] if cands else None

    # Class C filers publish a full P&L and often omit the merged
    # bruttofortjeneste line, so fall back to revenue.
    return (pick("GrossProfitLoss"), pick("EmployeeBenefitsExpense"),
            pick("Revenue"))


def one(row):
    cvr = (row["cvr"] or "").strip()
    out = dict(row, bruttofortjeneste="", personale="", omsaetning="", periode="", note="")
    if not cvr:
        out["note"] = "no cvr"
        return out
    try:
        found = latest_xbrl(cvr)
        if not found:
            out["note"] = "no annual report"
            return out
        xml, start, end = found
        gp, emp, rev = facts(xml, start, end)
        out["periode"] = end
        out["bruttofortjeneste"] = "" if gp is None else gp
        out["personale"] = "" if emp is None else emp
        out["omsaetning"] = "" if rev is None else rev
        if gp is None:
            out["note"] = "revenue only" if rev is not None else "no P&L tags"
    except Exception as e:
        out["note"] = f"error: {type(e).__name__}"
    return out


src = sys.argv[1] if len(sys.argv) > 1 else "liste.csv"
dst = sys.argv[2] if len(sys.argv) > 2 else src.replace(".csv", "") + "-bfj.csv"
rows = list(csv.DictReader(open(src, encoding="utf-8")))
print(f"joining {len(rows)} companies from {src}...", file=sys.stderr)
done = []
with ThreadPoolExecutor(max_workers=6) as ex:
    for n, r in enumerate(ex.map(one, rows), 1):
        done.append(r)
        if n % 50 == 0:
            print(f"  {n}/{len(rows)}", file=sys.stderr)

flds = list(rows[0].keys()) + ["bruttofortjeneste", "personale", "omsaetning",
                               "periode", "note"]
with open(dst, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=flds)
    w.writeheader()
    w.writerows(done)
print(f"written {dst}", file=sys.stderr)
