"""Score offer candidates that `score.py` cannot represent.

`score.py` ranks Danish industries from DST: bruttofortjeneste per firm, firm
count, growth, branchekode. It is the right instrument for the margin offer and
the wrong one for anything whose buyer is not a Danish company — there is no
branchekode for "people who cannot sleep", and bruttofortjeneste per firm is
undefined for an individual. Running it on those would produce a number with no
referent.

Two deliberate differences from `score.py`.

**Gates before weights.** principles.md orders the list: the buyer, then
evidence the problem is already paid for. Those are not weighted terms that a
strong score elsewhere can compensate for - fail either and the candidate is
dead. Medspa did not lose on points, it lost on being unable to pay.

**Adherence is a scored term, at the heaviest weight.** The strongest measured
result in the Synthesizer corpus is that showing up repeatedly separates people
far more than market choice does: the spread across markets is 45-67%, the
spread between posting once and posting three or more times is 33-68%. If that
holds even partly, then "will I still be doing this in eighteen months" belongs
in the model rather than in a footnote. Its confound is stated at the bottom and
is not small.

Adherence is scored from revealed preference, not from stated enthusiasm.
Everything anyone says about what they enjoy is uncalibrated; years already
spent doing something unpaid is not.

    python3 tools/candidate_score.py
"""

# --- gates ------------------------------------------------------------------
# principles.md items 1 and 2. Binary. A candidate failing either is not
# ranked, because nothing below the top of that list matters when the top is
# wrong.

GATES = {
    "buyer_named": "Can you name people already paying someone for this?",
    "problem_paid": "Is there evidence the problem is already paid for?",
}

# --- weights, and why -------------------------------------------------------
W = {
    "adherence": 0.30,   # the measured dominant variable; see module docstring
    "koebekraft": 0.25,  # what killed medspa; Hormozi's resume-writer story
    "moat": 0.15,        # principles.md 7 - nobody can copy what you have done
    "price_anchor": 0.15,# what the market already pays for the nearest thing
    "reachable": 0.15,   # can the buyer be enumerated or reliably reached
}

# --- candidates -------------------------------------------------------------
# All JUDGED. This file makes the judgement explicit and comparable; it does
# not make it objective. Where a number is a guess it says so in the note.

C = [
    dict(
        key="margin",
        name="Danish ecom profitability retainer",
        buyer_named=1, problem_paid=1,
        koebekraft=0.90, moat=0.75, price_anchor=0.70, reachable=0.95,
        # Revealed: no unpaid years in this. Day: spreadsheets, ledgers,
        # outreach to strangers about their returns accounting.
        revealed=0.10, day_shape=0.35,
        note="Buyer test passed on published accounts. CVR + Meta Ad Library "
             "is a real data moat. Adherence is the weak leg and always was.",
    ),
    dict(
        key="contemplative",
        name="Contemplative psychology, English market",
        buyer_named=1, problem_paid=1,
        koebekraft=0.45, moat=0.15, price_anchor=0.55, reachable=0.40,
        # Revealed: years of unpaid study and an archive built for its own
        # sake. That is the strongest adherence evidence available for any
        # candidate here, and it was not collected in order to win an argument.
        revealed=0.95, day_shape=0.85,
        note="Buyer gate passes in English (Waking Up, Ten Percent Happier, "
             "MBSR, retreats) and fails in Thai, where dhamma is given not "
             "sold. Koebekraft is the risk and depends on which buyer, not "
             "which subject. Moat scored 0.15, not 0.70: an index over a "
             "public YouTube channel is a few prompts of work and machine "
             "translation is closing the language gap anyway. Reachable is "
             "low - no register, no enumerable list, unlike Danish webshops.",
    ),
]


def adherence(c):
    """Revealed preference dominates stated preference, 60/40.

    Someone who has already done a thing for years without being paid has
    demonstrated the trait the score is trying to predict. Someone forecasting
    that they would enjoy a job they have never done is guessing, and guessing
    optimistically, which is why day_shape is the lighter half.
    """
    return 0.6 * c["revealed"] + 0.4 * c["day_shape"]


def main():
    live, dead = [], []
    for c in C:
        c["adherence"] = adherence(c)
        (dead if not (c["buyer_named"] and c["problem_paid"]) else live).append(c)
        c["score"] = sum(W[k] * c[k] for k in W)

    live.sort(key=lambda c: -c["score"])

    cols = ["adherence", "koebekraft", "moat", "price_anchor", "reachable"]
    head = f"{'candidate':<38}{'score':>7}  " + "".join(f"{k[:9]:>10}" for k in cols)
    print(head)
    print("-" * len(head))
    for c in live:
        print(f"{c['name'][:38]:<38}{c['score']:>7.3f}  "
              + "".join(f"{c[k]:>10.2f}" for k in cols))
    for c in dead:
        print(f"{c['name'][:38]:<38}{'GATED':>7}")

    print("\nWithout the adherence term (i.e. the old way of scoring):")
    w2 = {k: v for k, v in W.items() if k != "adherence"}
    tot = sum(w2.values())
    alt = sorted(live, key=lambda c: -sum(w2[k] * c[k] for k in w2) / tot)
    for c in alt:
        print(f"  {c['name'][:38]:<38}{sum(w2[k]*c[k] for k in w2)/tot:>7.3f}")

    # The only number here that changes a decision: how much you have to
    # believe adherence matters before the ranking flips.
    print("\nSensitivity - where the ranking changes hands:")
    base = {k: v for k, v in W.items() if k != "adherence"}
    tot = sum(base.values())
    for w in [x / 100 for x in range(0, 61, 5)]:
        scores = {
            c["key"]: w * c["adherence"] + (1 - w) * sum(base[k] * c[k] for k in base) / tot
            for c in live
        }
        top = max(scores, key=scores.get)
        lead = sorted(scores.values(), reverse=True)
        print(f"  adherence weight {w:>4.0%}   winner: {top:<14} "
              f"margin of victory {lead[0]-lead[1]:.3f}")

    print("""
Read this as a disqualifier, not a ranker. The gates did the real work; the
weights only order what survived them. A scorecard anyone could run selects for
markets everyone can see - principles.md, "how you found it predicts how
crowded it is" - so a high score is weak evidence of opportunity and a failed
gate is strong evidence of its absence.

The adherence confound: people who get early traction keep going, so activity
may be a consequence of winning rather than a cause. Weighting it at 0.30
assumes at least part of the arrow points the other way. That assumption is
doing real work here and is not established.""")


if __name__ == "__main__":
    main()
