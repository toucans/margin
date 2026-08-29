#!/usr/bin/env python3
"""§3 triage, in the brief's order. Prints what each rule removed."""
import json, sys, re, pathlib, collections

ROWS = [json.loads(l) for l in open(sys.argv[1])]

# 2. B2C wellness at app pricing / consumer product, wrong market
PRODUCT = re.compile(r"\b(shop now|free shipping|add to cart|discount|% off|"
                     r"gummies|supplement|tincture|mushroom|elixir|drink|"
                     r"non-?alcoholic|mocktail|beer|wine club|tea|skincare|"
                     r"subscribe (?:and|&) save|order now|buy \d|bundle)\b", re.I)
APP = re.compile(r"\b(download the app|app store|google play|free trial|"
                 r"7-day trial|habit tracker|journal(?:ing)? app|meditation app)\b", re.I)
# 3. selling to coaches
TO_COACHES = re.compile(r"\b(coaches|therapists|practitioners|your clients|"
                        r"fill your calendar|client acquisition|"
                        r"grow your practice|course creators|book more clients|"
                        r"6-figure (?:coach|business)|scale your (?:coaching|practice))\b", re.I)
# 4. therapy directories and clinics
CLINIC = re.compile(r"\b(therapist directory|find a therapist|insurance|"
                    r"in-network|treatment cent(?:er|re)|rehab|detox|"
                    r"clinic|psykolog(?:hj%C3%A6lp|hjælp)?|behandlingscenter|"
                    r"outpatient|inpatient|licensed clinician)\b", re.I)

def text(r):
    return " ".join(filter(None, [r.get("hook_first_line"), r.get("headline"),
                                  r.get("body_full"), r.get("cta_text"),
                                  " ".join(r.get("page_categories") or [])]))

drops = collections.Counter()
kept = []
for r in ROWS:
    t = text(r)
    if (r.get("days_live") or 0) < 45:
        drops["1. under 45 days live"] += 1;  continue
    if APP.search(t) or PRODUCT.search(t):
        drops["2. B2C wellness / consumer product"] += 1; continue
    if TO_COACHES.search(t):
        drops["3. selling to coaches"] += 1; continue
    if CLINIC.search(t):
        drops["4. therapy directory / clinic"] += 1; continue
    kept.append(r)

print(f"in: {len(ROWS)}")
for k in sorted(drops): print(f"  drop {k}: {drops[k]}")
print(f"survivors: {len(kept)}")
json.dump(kept, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
