#!/usr/bin/env python3
"""Triage the LinkedIn sweep and score each framing for a real founder market.

LinkedIn publishes dates/impressions/targeting only for EU-served ads, so
longevity is measurable on DK/DE/NL and copy-only elsewhere. Rows without dates
are kept for the buyer-density read but cannot pass the 45-day test.
"""
import json, sys, re, datetime, collections, pathlib

HERE = pathlib.Path(__file__).parent
CL = json.loads((HERE / "clusters.json").read_text())
TERM2C = {}
for cid, c in CL.items():
    for t in c["terms"]:
        TERM2C.setdefault(t.lower(), cid)

# does the copy address a founder / owner / executive about their own working life?
FOUNDER = re.compile(r"\b(founder|co-?founder|ceo|business owner|owner-?manager|"
                     r"entrepreneur|scale-?up|startup|executive|c-?suite|"
                     r"managing director|leader|leadership|board|your team|"
                     r"your business|running a business|high[- ]achiev)\b", re.I)
# selling TO coaches, or recruiting, or plain corporate services — not our buyer
EXCLUDE = re.compile(r"\b(coaches|therapists|practitioners|your clients|fill your calendar|"
                     r"client acquisition|recruit(ing|ment)?|hiring|candidates|"
                     r"webinar for hr|hr teams|employee (benefit|assistance)|"
                     r"book a demo|saas platform|software)\b", re.I)

def load(paths):
    rows = []
    for p in paths:
        d = json.load(open(p))
        rows.extend(d["items"] if isinstance(d, dict) else d)
    return rows

def days(a):
    fs, ls = a.get("firstSeen"), a.get("lastSeen")
    if not (fs and ls):
        return None
    try:
        return (datetime.date.fromisoformat(ls[:10]) - datetime.date.fromisoformat(fs[:10])).days
    except Exception:
        return None

def main(paths, out):
    rows = load(paths)
    seen, keep = set(), []
    for a in rows:
        aid = a.get("adId")
        if aid in seen:
            continue
        seen.add(aid)
        body = " ".join(filter(None, [a.get("body"), a.get("headline"),
                                      a.get("headlineDescription")]))
        if not body.strip():
            continue
        q = (a.get("query") or "").lower().replace("keyword: ", "").strip()
        keep.append({
            "cluster_id": TERM2C.get(q, "?"), "keyword_hit": a.get("query"),
            "advertiser": a.get("advertiserName"), "slug": a.get("advertiserSlug"),
            "ad_id": aid, "first_seen": a.get("firstSeen"), "last_seen": a.get("lastSeen"),
            "days_live": days(a), "impressions": a.get("impressionsRange.label")
                                  or (a.get("impressionsRange") or {}).get("label"),
            "body": body, "hook": next((l.strip() for l in (a.get("body") or "").split("\n")
                                        if l.strip()), ""),
            "click_url": a.get("clickUrl"), "paid_by": a.get("paidBy"),
            "targeting": a.get("targeting"), "format": a.get("format"),
            "founder_facing": bool(FOUNDER.search(body)) and not EXCLUDE.search(body),
            "has_dates": days(a) is not None,
        })
    json.dump(keep, open(out, "w"), ensure_ascii=False, indent=1)

    print(f"unique ads: {len(keep)}  (with dates: {sum(1 for r in keep if r['has_dates'])})")
    print(f"founder-facing: {sum(1 for r in keep if r['founder_facing'])}\n")
    print(f'{"cl":4}{"ads":>6}{"founder":>9}{"%":>6}{"dated":>7}{"45d+":>6}{"90d+":>6}  longest')
    for cid in sorted({r["cluster_id"] for r in keep}):
        g = [r for r in keep if r["cluster_id"] == cid]
        f = [r for r in g if r["founder_facing"]]
        fd = [r for r in f if r["has_dates"]]
        o45 = [r for r in fd if r["days_live"] >= 45]
        o90 = [r for r in fd if r["days_live"] >= 90]
        longest = max((r["days_live"] for r in fd), default=0)
        pct = round(100 * len(f) / len(g)) if g else 0
        print(f'{cid:4}{len(g):>6}{len(f):>9}{pct:>5}%{len(fd):>7}{len(o45):>6}{len(o90):>6}  {longest}d')

if __name__ == "__main__":
    main(sys.argv[2:], sys.argv[1])
