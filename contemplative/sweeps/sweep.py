#!/usr/bin/env python3
"""Run the §2 keyword clusters across the §1 countries via the Ad Library API.

Countries are run separately, never merged (§1). Multi-word terms use
KEYWORD_EXACT_PHRASE — KEYWORD_UNORDERED matches loosely and returns ads that
contain neither idea, which would poison every cluster.
"""
import json, sys, pathlib, datetime, hashlib, urllib.parse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from meta_ads import token, GRAPH, FIELDS  # noqa: E402

CLUSTERS = json.loads((HERE / "clusters.json").read_text())
COUNTRIES = ["DK", "DE", "NL", "GB", "US", "AU"]
TODAY = datetime.date(2026, 8, 29)
PER_QUERY_CAP = 500
TOK = token()


def fetch(term, country, status):
    exact = " " in term
    params = {
        "search_terms": term,
        "ad_reached_countries": json.dumps([country]),
        "ad_type": "ALL",
        "ad_active_status": status,
        "search_type": "KEYWORD_EXACT_PHRASE" if exact else "KEYWORD_UNORDERED",
        "fields": ",".join(FIELDS),
        "limit": "100",
        "access_token": TOK,
    }
    url = GRAPH + "?" + urllib.parse.urlencode(params)
    rows, pages, err = [], 0, None
    while url and len(rows) < PER_QUERY_CAP and pages < 8:
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                body = json.load(r)
        except urllib.error.HTTPError as e:
            try:
                err = json.load(e)["error"]["message"][:90]
            except Exception:
                err = f"HTTP {e.code}"
            break
        except Exception as e:  # noqa: BLE001
            err = str(e)[:90]
            break
        rows.extend(body.get("data", []))
        url = body.get("paging", {}).get("next")
        pages += 1
    return rows, err


def job(args):
    cid, term, country, status = args
    rows, err = fetch(term, country, status)
    out = []
    for a in rows:
        sd = a.get("ad_delivery_start_time")
        ed = a.get("ad_delivery_stop_time")
        body = (a.get("ad_creative_bodies") or [""])[0] or ""
        hook = next((l.strip() for l in body.split("\n") if l.strip()), "")
        days = None
        if sd:
            d0 = datetime.date.fromisoformat(sd)
            end = datetime.date.fromisoformat(ed) if ed else TODAY
            days = (min(end, TODAY) - d0).days
        out.append({
            "cluster_id": cid, "keyword_hit": term, "status_pass": status,
            "advertiser_name": a.get("page_name"), "page_id": a.get("page_id"),
            "ad_archive_id": a.get("id"),
            "started_running": sd, "stopped_running": ed,
            "still_active": ed is None, "days_live": days,
            "countries": country,
            "surfaces": a.get("publisher_platforms"),
            "hook_first_line": hook, "body_full": body,
            "headline": (a.get("ad_creative_link_titles") or [None])[0],
            "destination_domain": (a.get("ad_creative_link_captions") or [None])[0],
            "link_description": (a.get("ad_creative_link_descriptions") or [None])[0],
            "ad_snapshot_url": a.get("ad_snapshot_url"),
            "eu_reach": a.get("eu_total_reach"),
            "target_ages": a.get("target_ages"), "target_gender": a.get("target_gender"),
            "target_locations": a.get("target_locations"),
            "languages": a.get("languages"),
            "copy_hash": hashlib.sha1(body.strip().lower().encode()).hexdigest()[:12],
        })
    return (cid, term, country, status, len(out), err), out


def main(status, outfile):
    jobs = []
    for cid, c in CLUSTERS.items():
        countries = ["DK"] if cid == "C8" else COUNTRIES
        for term in c["terms"]:
            for cc in countries:
                jobs.append((cid, term, cc, status))
    print(f"{len(jobs)} queries, status={status}", file=sys.stderr)
    allrows, log = [], []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, (meta, rows) in enumerate(ex.map(job, jobs), 1):
            log.append(meta); allrows.extend(rows)
            if i % 40 == 0:
                print(f"  {i}/{len(jobs)} … {len(allrows)} ads", file=sys.stderr)
    # §1: sort locally by start date ascending — the API will not do it
    allrows.sort(key=lambda r: (r["started_running"] or "9999"))
    with open(outfile, "w") as f:
        for r in allrows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(outfile.replace(".jsonl", "_querylog.json"), "w") as f:
        json.dump([{"cluster": m[0], "term": m[1], "country": m[2], "status": m[3],
                    "n": m[4], "error": m[5]} for m in log], f, indent=1, ensure_ascii=False)
    errs = [m for m in log if m[5]]
    print(f"done: {len(allrows)} ads -> {outfile}; {len(errs)} query errors", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
