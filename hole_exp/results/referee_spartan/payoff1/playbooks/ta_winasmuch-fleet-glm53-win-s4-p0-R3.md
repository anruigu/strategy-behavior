---
game: ta_winasmuch
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 2507
---
**Playbook for ta_winasmuch**

- The all-Y cooperation strategy is now confirmed to work and is my default. When all three pledge Y and I pledge/play Y too, the table holds at +1 per player per round through every multiplier round. This took me to +45 — far better than the defection spiral that left me at -21. Repeat this.

- The bots' behavior is tit-for-tat-like, not fixed. If I defect early for a lone +3, they punish with all-X every round after, and the multiplier rounds (x3, x5, x10 = 18 effective rounds of scoring) get locked into -1 each. A lone +3 or +2 early is always a losing trade. Do NOT defect before the final round.

- Keep pledging [pledge: y] at every talk phase when cooperation is holding. Honest signaling matches my intended play and costs nothing.

- Round 1 and early low-multiplier rounds are the critical discipline points: cooperate, cooperate, cooperate. The +1-per-round flow preserved into x3/x5/x10 is where all the real money is made.

- Multiplier rounds (5, 8): absolutely no experiments, ever. A lone Y on x5 or x10 is catastrophic (-15/-30), and a defection that breaks cooperation costs me the multiplied +1s for all remaining rounds.

- Round 9: still cooperate. A lone +3 there risks losing the +10 cooperation round. The only round where defection is correct is the final one.

- Round 10 (or the last round of any length game): defect. Once no future punishment is possible, X strictly dominates (+3 vs +1 if they cooperate; -1 vs -3 if they defect). I did this and it capped my score correctly — all-Y through round 9, lone X on the x10 final.

- If others all played X last round, pick X — never lone-Y into a known all-X table (-1 with them beats -3 alone). This damage-limitation rule still holds for episodes where cooperation fails.

- If others defect first (breaking the Y equilibrium), treat it as the punishment regime beginning: take X with the table, don't martyr myself with lone Y.

- Don't infer strategy from score differences alone. Judge each round only by what the others did last round, not by totals.

- At talk phases, my pledge had no observable effect on the bots' picks, but their pledges accurately signaled Y play. Pledge honestly; use their pledges as data.

- Summary decision rule: (1) All pledge Y → pledge Y, pick Y. (2) Others played Y last round and any rounds (especially multipliers) remain → pick Y. (3) Others all played X → pick X. (4) Never deviate on x3/x5/x10 rounds. (5) Final round, no retaliation possible → pick X.