---
game: ta_winasmuch
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2777
---
**Playbook for ta_winasmuch**

- The bots' behavior is tit-for-tat-like, not fixed. In my episode they all played Y in round 1 (matching their pledges), I defected with lone X for +3, and they punished me by picking all-X every round after. My lone +3 was followed by nine rounds of -1/-3 — a terrible trade. Do NOT assume defection is free.

- Their "[pledge: y]" broadcasts may be genuine signals of intended cooperation, not noise. Test this in round 1: if the situation repeats (all three pledge Y), consider picking Y in round 1 to establish cooperation. If everyone plays Y, everyone gets +1 per round — vastly better than the mutual-X death spiral that left me at -21.

- The critical decision is round 1 and early low-multiplier rounds. If I defect early for +3 and trigger permanent all-X punishment, the multiplier rounds (x3, x5, x10 = 18 effective rounds of scoring) get locked into -1 each — that's where the real damage accumulates. Cooperation preserved into the multipliers is worth far more than a lone +3 or +2 early.

- Once the table is locked into all-X, my choice is X with all (-1) or lone Y (-3). Lone Y is strictly worse; never defect into a known all-X table no matter how far behind. Damage limitation: take the -1 with them. I did this correctly and it holds.

- Multiplier rounds: absolutely no experiments. A lone Y on a x5 or x10 round is catastrophic (-15/-30). Discipline matters most exactly when stakes are highest.

- Don't infer strategy from score differences alone. I was behind despite recent identical picks (the gap came from earlier rounds) and that reasoning was false. Judge each round only by what the others did last round, not by totals.

- If the table does show Y behavior (others actually picked Y), lone X is the money play — but weigh the +3 against the risk of triggering a permanent punishment regime. Milking +3 for one round and losing cooperation for the remaining multiplier-heavy rounds is a losing trade. Only defect near the very end (round 9-10) if a punishment regime can't hurt me much, or if they've already defected.

- At talk phases, my pledge had no observable effect on the bots' subsequent picks. Pledge whatever matches my intended play (honest signaling); don't spend effort crafting signals, but don't assume pledges are meaningless as data about their intended first-round moves either.

- Summary decision rule: (1) If others pledged Y and I have no evidence yet they'll defect, try Y in round 1 to build cooperation. (2) If others played Y last round and multipliers remain far off, weigh lone X (+3) against losing the +1-each cooperation — cooperate if the multipliers are still ahead. (3) If others all played X last round, pick X — never lone-Y into all-X. (4) Never deviate on x3/x5/x10 rounds.