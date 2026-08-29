#!/usr/bin/env python3
"""Emit the findings artifact, reading hooks straight from the CSV so every
quoted line stays verbatim."""
import csv, json, html, collections

rows = {(r["cluster"], r["advertiser"]): r for r in csv.DictReader(open("collapsed.csv"))}

# hand-curated: genuine framing matches, keyword artifacts removed (§5 trap 3)
KEEP = {
 "C1": ["Metacognitive Therapy","Peak Performance Hypnosis","Clear Minds Hypnotherapy"],
 "C2": ["karl_williams_leadership_coach","Kara Kuipers","Mindstar Hypnotherapy",
        "Sleep Oracles","Always Greater","Domus Focus","John Davidson","JCC Academy"],
 "C3": ["Laura Lange"],
 "C4": ["Dr. Sara B","Luke Roe","The Bio-Axis","Stan Taylor","Amy Thiessen"],
 "C5": ["Sarah Rusbatch","Just the Tonic","Mindful Drinking Community",
        "Dr. Alex Morgan","Alcohol Free Daily","Ask Dr. Whitmore"],
 "C6": ["PDF Guide Sanctuary","Medifit Rehabilitation Center","Rewired Woman","The Tired Years"],
 "C7": ["Human Behavior Lab"],
 "C8": ["Mellem-Rummet Retreat, Samsø","Lind & Dahl","Stærkt Sind","Djøf"],
}
LABEL = {
 "C1":"the decision that reopens at 2 a.m.","C2":"can't switch out of work mode",
 "C3":"checking the same metric or thread","C4":"the body captured before the mind notices",
 "C5":"performing under pressure, same habit next day","C6":"burnout as an unbreakable loop",
 "C7":"ADHD founder","C8":"Denmark",
}
ADV = {}   # advertisers surviving triage per cluster, from the full run
for r in csv.DictReader(open("collapsed.csv")):
    ADV.setdefault(r["cluster"], set()).add(r["advertiser"])

out = []
for cid in sorted(KEEP):
    items = []
    for name in KEEP[cid]:
        r = rows.get((cid, name))
        if not r:
            continue
        items.append({
            "adv": r["advertiser"], "days": int(r["longest_run_days"]),
            "variants": int(r["variants"]), "countries": r["countries"],
            "hook": r["framing (verbatim hook)"], "lp": r["LP type"] or "—",
            "dom": r["domain"] or "—", "eu": r["eu_reach"] or "",
        })
    items.sort(key=lambda x: -x["days"])
    out.append({"id": cid, "label": LABEL[cid], "items": items,
                "advertisers": len(ADV.get(cid, []))})
json.dump(out, open("report_data.json","w"), ensure_ascii=False, indent=1)
print("clusters:", [(c["id"], len(c["items"])) for c in out])
