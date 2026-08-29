#!/usr/bin/env python3
"""§6 output: the raw CSV in the §4 schema, and the collapsed one-row-per-framing table."""
import json, csv, collections, sys

rows = json.load(open("framed_active.json"))
lp = {l["destination_url"]: l for l in json.load(open("lp_results.json"))}

# ---- artifact 1: raw CSV, §4 schema, one row per creative
cols = ["cluster_id","keyword_hit","advertiser_name","page_id","ad_archive_id",
        "started_running","still_active","days_live","countries","surfaces",
        "variant_count","hook_first_line","headline","destination_url","eu_reach",
        "longest_single_creative_days","total_span_days","relaunch","country_count",
        "aftenskole_flag","target_ages","target_gender","lp_h1","lp_page_type","price_visible"]
with open("ad_evidence.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        d = dict(r)
        d["destination_url"] = r.get("destination_domain")
        d["surfaces"] = "|".join(r.get("surfaces") or [])
        d["target_ages"] = "-".join(r.get("target_ages") or [])
        l = lp.get((r.get("destination_domain") or "").strip(), {})
        d["lp_h1"] = l.get("lp_h1"); d["lp_page_type"] = l.get("lp_page_type")
        d["price_visible"] = l.get("price_visible")
        w.writerow(d)
print(f"ad_evidence.csv: {len(rows)} creatives")

# ---- artifact 2: collapsed, one row per framing (advertiser x cluster)
agg = {}
for r in rows:
    k = (r["cluster_id"], r["page_id"])
    a = agg.setdefault(k, {"cluster": r["cluster_id"], "adv": r["advertiser_name"],
                           "longest": 0, "span": 0, "variants": 0, "countries": set(),
                           "hook": "", "dom": r.get("destination_domain"),
                           "relaunch": False, "eu": None, "aften": r.get("aftenskole_flag")})
    if (r["longest_single_creative_days"] or 0) >= a["longest"]:
        a["longest"] = r["longest_single_creative_days"] or 0
        a["hook"] = r["hook_first_line"]
        a["dom"] = r.get("destination_domain") or a["dom"]
    a["span"] = max(a["span"], r.get("total_span_days") or 0)
    a["variants"] = max(a["variants"], r.get("variant_count") or 0)
    a["countries"] |= set(r.get("countries_live") or [])
    a["relaunch"] = a["relaunch"] or bool(r.get("relaunch"))
    if r.get("eu_reach"): a["eu"] = max(a["eu"] or 0, r["eu_reach"])

out = sorted(agg.values(), key=lambda a: (a["cluster"], -a["longest"]))
with open("collapsed.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["cluster","framing (verbatim hook)","advertiser","longest_run_days",
                "total_span_days","relaunch","variants","countries","eu_reach",
                "price","LP type","lp_h1","domain"])
    for a in out:
        l = lp.get((a["dom"] or "").strip(), {})
        w.writerow([a["cluster"], a["hook"], a["adv"], a["longest"], a["span"],
                    a["relaunch"], a["variants"], "".join(sorted(a["countries"])),
                    a["eu"], l.get("price_visible"), l.get("lp_page_type"),
                    l.get("lp_h1"), a["dom"]])
print(f"collapsed.csv: {len(out)} advertiser-framings")
