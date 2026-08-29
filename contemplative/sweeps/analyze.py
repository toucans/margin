#!/usr/bin/env python3
"""§3 triage, §5 traps, §6 collapse.

Triage order is the brief's. Every drop is counted so an empty cluster can be
told apart from a cluster that was filtered away.
"""
import json, sys, re, collections, datetime, pathlib

TODAY = datetime.date(2026, 8, 29)
rows = [json.loads(l) for l in open(sys.argv[1])]

# --- §3 drop rules, applied in order -------------------------------------
APP = re.compile(r"\b(download the app|app ?store|google play|habit tracker|"
                 r"journal(?:ing)? app|meditation app|free 7[- ]day|"
                 r"\$?\d+(?:\.\d+)?/(?:mo|month)\b)", re.I)
PRODUCT = re.compile(r"\b(shop now|free shipping|add to cart|% off|use code|"
                     r"gummies|supplement|tincture|capsules|mushroom|elixir|"
                     r"non[- ]?alcoholic|mocktail|seltzer|kombucha|beer|"
                     r"skincare|serum|collagen|subscribe (?:and|&) save|"
                     r"order now|bundle|shipping)\b", re.I)
TO_COACHES = re.compile(r"\b(coaches|therapists|practitioners|your clients|"
                        r"fill your calendar|client acquisition|grow your practice|"
                        r"book more clients|course creators|scale your (?:coaching|practice)|"
                        r"6[- ]figure|coaching business|get clients)\b", re.I)
CLINIC = re.compile(r"\b(find a therapist|therapist directory|insurance|in[- ]network|"
                    r"treatment cent(?:er|re)|rehab|detox|outpatient|inpatient|"
                    r"licensed (?:therapist|clinician)|psykolog|behandlingscenter|"
                    r"psykiater|lægehus)\b", re.I)
REMOVED = re.compile(r"(didn't follow our Advertising Standards|"
                     r"we later disabled|This ad was run by an account)", re.I)

def blob(r):
    return " ".join(filter(None, [r.get("hook_first_line"), r.get("headline"),
                                  r.get("body_full"), r.get("link_description"),
                                  r.get("destination_domain")]))

drops = collections.Counter()
kept = []
for r in rows:
    t = blob(r)
    if not (r.get("body_full") or "").strip():
        drops["0. no creative text returned"] += 1; continue
    if REMOVED.search(t):
        drops["0. creative removed by Meta"] += 1; continue
    if (r.get("days_live") or 0) < 45:
        drops["1. under 45 days live"] += 1; continue
    if APP.search(t) or PRODUCT.search(t):
        drops["2. B2C wellness / consumer product"] += 1; continue
    if TO_COACHES.search(t):
        drops["3. selling to coaches"] += 1; continue
    if CLINIC.search(t):
        drops["4. therapy directory / clinic"] += 1; continue
    kept.append(r)

print(f"IN {len(rows)}")
for k in sorted(drops):
    print(f"  drop {k}: {drops[k]}")
print(f"SURVIVORS {len(kept)}\n")

# --- §5 trap 1: relaunch vs continuity ------------------------------------
# longest_single_creative_days = max run of ONE archive id
# total_span_days = earliest start -> latest end for the same copy under a page
by_copy = collections.defaultdict(list)
for r in kept:
    by_copy[(r["page_id"], r["copy_hash"])].append(r)
for group in by_copy.values():
    starts = [datetime.date.fromisoformat(g["started_running"]) for g in group if g["started_running"]]
    ends = [datetime.date.fromisoformat(g["stopped_running"]) if g.get("stopped_running")
            else TODAY for g in group]
    span = (max(ends) - min(starts)).days if starts else None
    longest = max((g["days_live"] or 0) for g in group)
    ids = len({g["ad_archive_id"] for g in group})
    for g in group:
        g["longest_single_creative_days"] = longest
        g["total_span_days"] = span
        g["archive_ids_same_copy"] = ids
        g["relaunch"] = ids > 1 and span > longest

# variant_count: distinct copy hashes under one advertiser within a cluster
var = collections.defaultdict(set)
for r in kept:
    var[(r["page_id"], r["cluster_id"])].add(r["copy_hash"])
for r in kept:
    r["variant_count"] = len(var[(r["page_id"], r["cluster_id"])])

# §5 trap 4: Danish aftenskole seasonality — flag, do not rank
AFTEN = re.compile(r"\b(FOF|AOF|LOF|aftenskole|folkeuniversitet)", re.I)
for r in kept:
    r["aftenskole_flag"] = bool(AFTEN.search(r.get("advertiser_name") or ""))

# §5 trap 2: do NOT dedupe across countries — count countries per creative copy
ctry = collections.defaultdict(set)
for r in kept:
    ctry[(r["page_id"], r["copy_hash"])].add(r["countries"])
for r in kept:
    r["countries_live"] = sorted(ctry[(r["page_id"], r["copy_hash"])])
    r["country_count"] = len(r["countries_live"])

json.dump(kept, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)

# --- coverage note --------------------------------------------------------
print("=== coverage: rows returned per country (pre-triage) ===")
cc = collections.Counter(r["countries"] for r in rows)
for k in ["DK","DE","NL","GB","US","AU"]:
    print(f"  {k}: {cc.get(k,0)}")
print("\n=== survivors per cluster ===")
sc = collections.Counter(r["cluster_id"] for r in kept)
rc = collections.Counter(r["cluster_id"] for r in rows)
for k in sorted(rc):
    print(f"  {k}: {sc.get(k,0)} survivors of {rc[k]} raw")
