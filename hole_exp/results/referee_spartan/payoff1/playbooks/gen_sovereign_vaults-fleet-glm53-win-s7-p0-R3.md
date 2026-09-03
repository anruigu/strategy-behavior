---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 1769
---
**Playbook for gen_sovereign_vaults**

- Scoring rule confirmed across all 5 rounds of this episode: truthful declaration plus deposit 0 scores exactly 2 × true yield each round (deltas 20, 2, 14, 14, 8 for yields 10, 1, 7, 7, 4 — final +58, matching 2 × 29 total). Declare-true / deposit-0 is the dominant line.

- At the declare stage: declare my true private yield. Underdeclaring caps retained-gold scoring at the declared amount; overdeclaring gains nothing since I deposit 0 anyway and only adds audit-failure surface. Truthful declaration has no observed downside.

- At the deposit stage: deposit 0 whenever I declared truthfully. Retained gold scores 2/unit versus 1/unit for deposits, so every deposited gold piece halves its value. Deposits only feed the treasury/shared pool — my opponent (always declared 1, deposited 0) scored 2/round, and nothing in my payoffs rewarded the treasury.

- Track the scoreboard deltas every round to verify the rule still holds (delta should equal 2 × my yield when I declare true and deposit 0). If a deposit threshold, multiplier, or shared-pool bonus ever shows up in my or the opponent's delta, reconsider depositing — but don't assume generosity without evidence in the deltas.

- Never declare below my yield "for safety": the only audit risk is a deposit exceeding the declaration, and I control that fully by depositing 0. There is no penalty for truthful declaration.

- If the opponent deposits heavily and starts gaining more than my retained 2/unit, revisit; otherwise the declare-true, deposit-0 line dominates.

- Watch my own arithmetic when logging round scores — earlier I mis-summed the round deltas (wrote 84 for what was actually 58). Always recompute totals from the point deltas shown, not from memory.