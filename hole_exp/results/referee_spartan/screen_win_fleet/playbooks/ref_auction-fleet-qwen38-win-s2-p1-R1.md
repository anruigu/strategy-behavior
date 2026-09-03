---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 1854
---
# Playbook

**Budget tracking**
My budget is my starting cash minus the total I have actually paid for lots I have won. A bid that I do not win does not cost me anything. Before every decision, recompute: budget = 30 − (sum of winning prices I have paid). Do not subtract bids that lost. If I find myself reporting a budget that doesn't follow from this formula, stop and recompute before acting.

**When the standing bid is below my valuation**
- If it is round 1 and the standing bid is well below my valuation, bid an amount that is meaningfully below my valuation (roughly 60–70% of it) to establish presence without overcommitting in case the other bidder is willing to go high.
- If it is round 2 (final) and the minimum winning bid is at or below my valuation, bid my valuation (or the minimum winning bid if that is lower). The goal is to win at the cheapest price that still beats the other bidder. Do not leave value on the table by bidding only the minimum when I could have bid higher to be safe against a late outbid — actually, in a 2-round format there is no "late" outbid, so bid exactly the minimum winning bid if it is ≤ my valuation.

**When the standing bid is at or above my valuation**
Pass. Do not bid above what the lot is worth to me, even if it is the last lot or I feel I "should" win something.

**When there is no standing bid**
Open at roughly 50–60% of my valuation. This is low enough to leave room to raise in round 2, high enough to signal I am a real competitor.

**General aggression**
In this game I won nothing and scored 0 because I was too timid in the final round of lots where the price was below my value. When the final round comes and the minimum winning bid is below my valuation, I commit to winning. The score is value minus price; any win at a price below value adds to my score, and passing adds nothing.