#!/usr/bin/env python3
"""Normalise a spilled get-dataset-items file into the §4 per-creative schema.

Rows are keyed by (ad_archive_id, country) — §5 says do not dedupe across
countries, since one creative live in six is the stronger signal.
"""
import json, sys, re, datetime, pathlib, urllib.parse

HERE = pathlib.Path(__file__).parent
TODAY = datetime.date(2026, 8, 29)
CLUSTERS = json.loads((HERE / "clusters.json").read_text())
TERM2CLUSTER = {}
for cid, c in CLUSTERS.items():
    for t in c["terms"]:
        TERM2CLUSTER.setdefault(t.lower(), cid)


def parse_url(u):
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
    term = (qs.get("q", [""])[0]).strip('"')
    return term, qs.get("country", [""])[0]


def strip_utm(u):
    if not u:
        return None
    p = urllib.parse.urlparse(u)
    keep = [(k, v) for k, v in urllib.parse.parse_qsl(p.query)
            if not k.lower().startswith(("utm_", "fbclid", "gclid", "hsa_"))]
    return urllib.parse.urlunparse(p._replace(query=urllib.parse.urlencode(keep)))


def first_line(t):
    if not t:
        return ""
    for ln in t.split("\n"):
        if ln.strip():
            return ln.strip()
    return ""


def norm(it):
    url = it.get("url", "")
    term, country = parse_url(url)
    if not it.get("ad_archive_id"):
        return None  # empty query — the row is just a URL echo
    body = it.get("snapshot.body.text") or ""
    cards = it.get("snapshot.cards.body")
    if not body.strip() or "{{" in body:
        # catalog/DPA ad: real copy lives in the cards
        if isinstance(cards, list) and cards:
            body = next((c for c in cards if c and "{{" not in c), body)
        elif isinstance(cards, str):
            body = cards
    sd = it.get("start_date")
    ed = it.get("end_date")
    days = (TODAY - datetime.date.fromtimestamp(sd)).days if sd else None
    link = it.get("snapshot.link_url")
    if not link:
        cl = it.get("snapshot.cards.link_url")
        link = cl[0] if isinstance(cl, list) and cl else cl
    return {
        "cluster_id": TERM2CLUSTER.get(term.lower(), "?"),
        "keyword_hit": term,
        "advertiser_name": it.get("page_name"),
        "page_id": it.get("page_id"),
        "ad_archive_id": it.get("ad_archive_id"),
        "started_running": datetime.date.fromtimestamp(sd).isoformat() if sd else None,
        "ended": datetime.date.fromtimestamp(ed).isoformat() if ed else None,
        "still_active": it.get("is_active"),
        "days_live": days,
        "countries": country,
        "surfaces": it.get("publisher_platform"),
        "variant_count": it.get("collation_count"),
        "total_active_time": it.get("total_active_time"),
        "query_total": it.get("total"),
        "hook_first_line": first_line(body),
        "body_full": body,
        "headline": it.get("snapshot.title"),
        "cta_text": it.get("snapshot.cta_text"),
        "destination_url": strip_utm(link),
        "page_categories": it.get("snapshot.page_categories"),
        "eu_reach": it.get("aaa_info.eu_total_reach"),
    }


def main(paths, out):
    seen, rows = set(), []
    if pathlib.Path(out).exists():
        for ln in open(out):
            r = json.loads(ln)
            seen.add((r["ad_archive_id"], r["countries"], r["keyword_hit"]))
            rows.append(r)
    added = 0
    for p in paths:
        d = json.load(open(p))
        for it in d["items"]:
            r = norm(it)
            if not r:
                continue
            k = (r["ad_archive_id"], r["countries"], r["keyword_hit"])
            if k in seen:
                continue
            seen.add(k)
            rows.append(r)
            added += 1
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"+{added} new, {len(rows)} total -> {out}")


if __name__ == "__main__":
    main(sys.argv[2:], sys.argv[1])
