#!/usr/bin/env python3
"""Build Meta Ad Library search URLs for the cluster sweeps.

C8 is Denmark-only (Danish terms); C1-C7 run across all six countries.
Multi-word terms use keyword_exact_phrase so a hit means the framing was
actually written, not that the words co-occur somewhere in the creative.
"""
import json, sys, urllib.parse, pathlib

HERE = pathlib.Path(__file__).parent
CLUSTERS = json.loads((HERE / "clusters.json").read_text())
COUNTRIES = ["DK", "DE", "NL", "GB", "US", "AU"]
BASE = "https://www.facebook.com/ads/library/"


def url_for(term, country, active_status):
    exact = " " in term
    q = f'"{term}"' if exact else term
    params = {
        "active_status": active_status,
        "ad_type": "all",
        "country": country,
        "q": q,
        "search_type": "keyword_exact_phrase" if exact else "keyword_unordered",
        "media_type": "all",
    }
    return BASE + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def build(active_status="active", only=None):
    out = []
    for cid, c in CLUSTERS.items():
        if only and cid not in only:
            continue
        countries = ["DK"] if cid == "C8" else COUNTRIES
        for term in c["terms"]:
            for cc in countries:
                out.append({"cluster": cid, "term": term, "country": cc,
                            "url": url_for(term, cc, active_status)})
    return out


if __name__ == "__main__":
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    status = sys.argv[2] if len(sys.argv) > 2 else "active"
    rows = build(status, only)
    print(json.dumps(rows, ensure_ascii=False))
    print(f"# {len(rows)} urls", file=sys.stderr)
