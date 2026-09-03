---
game: ta_winasmuch
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2333
---
# Playbook

**When a talk phase is put to me, I pledge Y.** Every time. This is the single most important signal I can send. The all-Y outcome (0 X) pays +1 to everyone, and in high-multiplier rounds that compounds. Pledging Y builds the expectation that keeps the group coordinated.

**When picking, I default to Y if I expect three or more others to pick Y.** Matching the group on Y gives me +1 and keeps the coordination stable for the next round.

**I never pick X to be the lone defector against a Y-coordinated group.** The +3 I'd gain in a x1 round is always eaten by the retaliation that follows (they all flip to X, I'm the sole Y, I take -3). Net zero or negative, and I've broken the coordination that's worth +1 per round across the rest of the game. In high-multiplier rounds the opportunity cost is even worse: a stable all-Y round at x10 is worth +10, not +3.

**When three others have picked X and I expect they'll pick X again, I pick X.** Four X gives everyone -1. Three X and one Y gives the Y a -3. Matching the group on X is strictly better than being the sole Y.

**In high-multiplier rounds (x3, x5, x10), I prioritize matching whatever the group is most likely to do.** The multiplier amplifies both gains and losses equally, so the worst-case penalty (sole Y at -3 × multiplier) is the thing to avoid above all. If the group has been on Y for the last two rounds, I stay on Y.

**I do not alternate or "break patterns" to confuse opponents.** In this game the opponents are coordinating with each other, not with me. Breaking my own pattern doesn't disrupt their coordination; it just makes me the unpredictable one who sometimes becomes the sole Y.

**When I can't tell what the group will do, I pick Y.** Y is the safer default: the worst case for Y is -3 (sole Y vs 3 X), but the worst case for X is only -1 (all X). However, Y is the better expected-value pick because the group tends to converge on Y when pledged, and 0 X (+1) is a better outcome than 4 X (-1).

**What did not work:** Picking X in round 1 to exploit the +3. It triggered a two-round spiral (I got -3, then -1) before the group reconverged on Y. The cost of that disruption exceeded the one-time gain. Pledging Y while picking X in the same breath also signals unreliability and may make others less likely to trust my future pledges.