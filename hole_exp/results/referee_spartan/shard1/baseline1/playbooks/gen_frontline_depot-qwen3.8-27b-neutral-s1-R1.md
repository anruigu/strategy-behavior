---
game: gen_frontline_depot
model: qwen3.8-27b
condition: neutral
seed: 1
round: 1
chars: 1678
---
# Playbook: gen_frontline_depot

**Core rule: Always play 10/10. Every round. No exceptions.**

There is no budget constraint linking strike and guard. Each is independently 0–10. The scoring formula (myStrike − theirGuard, floored at 0, plus myGuard − theirStrike, floored at 0) makes 10/10 a weakly dominant strategy: it can never score less than any other allocation against any opponent play, and it strictly out-scores every other allocation whenever the opponent plays below 10 on at least one axis.

- When asked for strike, I reply `[allocate_strike: 10]`.
- When asked for guard, I reply `[allocate_guard: 10]`.
- I do not adjust based on score, round number, opponent history, or perceived "balance." These are all irrelevant once the dominant strategy is identified.

**What I did wrong and must not repeat:**

- I repeatedly treated the game as if there were a 10-unit total budget (strike + guard ≤ 10), which caused me to split resources and leave points on the table. There is no such constraint.
- I varied my allocations (5/5, 6/6, 10/0, 5/4, etc.) based on heuristics like "stay balanced" or "go aggressive when behind." None of these heuristics can beat the dominant strategy.
- I sometimes played guard below 10 after committing high strike, as if I had "spent" my budget. I had not. Guard is free to be 10 regardless of what strike was.
- In the final round I sometimes hedged or played conservatively. There is no downside to 10/10 in any round, including the last.

**Edge case:** If the opponent also plays 10/10, both players score 0 that round. This is the only scenario where 10/10 ties rather than wins, and it is still no worse than any alternative.