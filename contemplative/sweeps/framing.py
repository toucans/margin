#!/usr/bin/env python3
"""§5 trap 3: a keyword hit is not a framing match.

Keep a row only where the HOOK PROMISES the cluster's problem to a person about
their own life — not where the term merely appears. "Nervous system" selling a
supplement is neither C4 nor output.
"""
import json, re, sys, collections

PROMISE = {
 "C1": r"(overthink|can'?t stop thinking|replay|second[- ]guess|decision(s)? (that|keep|you)|"
       r"racing (mind|thoughts)|lying awake|3 ?a\.?m|2 ?a\.?m|wake up at|spiral)",
 "C2": r"(switch off|shut off|always on|still (working|thinking) (in your|about work)|"
       r"after work|out of work mode|log off|laptop|weekend|holiday|clock off|"
       r"mental load|never really off|can'?t relax)",
 "C3": r"(check(ing)? (your |my |the )?(phone|email|inbox|metric|numbers|stats|dm|message)|"
       r"refresh(ing)?|notification|doom ?scroll|screen time|pick up your phone)",
 "C4": r"(nervous system|dysregulat|fight[- ]or[- ]flight|freeze response|somatic|vagus|"
       r"regulat(e|ing) your|body (keeps|remembers|holds)|survival mode|cortisol)",
 "C5": r"(drink(ing)?|wine|alcohol|sober|booze|glass of|hangover|cut back|"
       r"edge off|nightcap|bottle)",
 "C6": r"(burn(t|ed)? ?out|burnout|exhaust|running on empty|depleted|"
       r"can'?t keep (this |going)|breaking point|overwhelm)",
 "C7": r"(adhd|executive (dys)?function|time blindness|distract|focus|procrastinat|"
       r"start (everything|things)|finish nothing)",
 "C8": r"(stress|overtænk|koble af|arbejdsmiljø|trivsel|udbrændt|pres|"
       r"altid på|slappe af|arbejdsliv)",
}
# the ad must address a person about themselves, not sell an object
PERSONAL = re.compile(r"\b(you|your|you'?re|du|dit|din|dig|dine|deine|dein|je|jij|jouw|i )\b", re.I)
OBJECT = re.compile(r"\b(balustrade|steel|dog|puppy|herding|pet|lash|hair|sinus|snoring|"
                    r"solitaire|game|blanket|mattress|earplug|headphone|magnesium|"
                    r"supplement|arabic|flight|propeller|aviation|escape room|"
                    r"teambuilding|grocery|produce|music video|casino|slot)\b", re.I)

rows = json.load(open(sys.argv[1]))
kept, dropped = [], collections.Counter()
for r in rows:
    text = " ".join(filter(None, [r.get("hook_first_line"), r.get("headline"), r.get("body_full")]))
    pat = PROMISE[r["cluster_id"]]
    if not re.search(pat, text, re.I):
        dropped["term present but no promise of the framing"] += 1; continue
    if not PERSONAL.search(text):
        dropped["not addressed to a person"] += 1; continue
    if OBJECT.search(text):
        dropped["hook sells an object, not the problem"] += 1; continue
    kept.append(r)
print(f"in {len(rows)} -> framing matches {len(kept)}")
for k, v in dropped.items(): print(f"   drop {k}: {v}")
json.dump(kept, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
