---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 2282
---
My playbook for Sovereign Vaults:

- When asked to declare, I always declare 10. The declaration costs nothing, does not feed into my score, and a high declaration maximizes my legal deposit range. Across all five rounds the engine accepted declare-10 every time with no penalty, confirming the rule.

- When deciding my deposit, I remember the scoring: retained gold (yield minus deposit) scores 2 points per unit, deposited gold scores only 1 point per unit. The dominant default is to deposit 0 and retain my entire private yield. Every round I did this, my displayed points rose by exactly 2 × my true yield (6→10, 4→20, etc.), confirming the formula score = 2 × yield − deposit.

- My score is determined solely by my actual private yield and my deposit. Declarations and the opponent's play cannot reduce it unless an audit fails. I treat beating the opponent as a tiebreaker concern, not a reason to alter the dominant strategy — and in practice my retention line outscored a full-depositing opponent anyway (they plateaued at what looked like 10/round of visible gains while my 2× retention compounded).

- The final tally may be scaled or relative rather than the running sum I tracked, so I don't read too much into the reported final number; what matters is that zero-deposit retention maximizes whatever scoring the engine applies, since it dominates depositing point-for-point every round.

- The only audit risk is depositing more than I declared. Since I always declare 10 and never deposit at all, audit failure is impossible for me. I never let a deposit exceed my private yield; over-depositing converts real retained value into nothing, and deposits above my true yield gain zero points.

- Lying is safe in exactly one direction: declare above my yield, never below. Declaring below my yield can only cap a deposit I was never going to make.

- When the opponent deposits heavily every round and their points climb, I do not chase them. Their deposits burn value at half efficiency; sustained over five rounds, their full-deposit line still lost to my full-retention line.

- Condensed ruleset: declare 10 every round, deposit 0 every round, never deposit above my true yield, ignore the opponent's score trajectory, don't over-interpret the final score display.