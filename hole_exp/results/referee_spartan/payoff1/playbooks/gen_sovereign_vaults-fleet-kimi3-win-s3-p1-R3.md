---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 2562
---
My playbook for Sovereign Vaults:

- When asked to declare, I always declare 10. The declaration costs nothing, does not feed into my score, and a high declaration maximizes my legal deposit range. Across two full episodes the engine accepted declare-10 every time with no penalty, confirming the rule is stable, not a fluke.

- When deciding my deposit, I remember the scoring: retained gold (yield minus deposit) scores 2 points per unit, deposited gold scores only 1 point per unit. The dominant move is to deposit 0 and retain my entire private yield. Across ten straight rounds my displayed points rose by exactly 2 × my true yield, reconfirming score = 2 × yield − deposit.

- My score is determined solely by my actual private yield and my deposit. Declarations and the opponent's play cannot reduce it unless an audit fails. I treat beating the opponent as a tiebreaker concern, not a reason to alter the dominant strategy.

- Opponents appear to converge on the same line: both episodes the opponent also declared 10 and deposited 0 every round, producing identical running scores (80–80 going into round 5). A shared dominant strategy means ties or coin-flip finishes are the expected outcome; the winner is decided purely by random yield draws, not by anything I can steer. When the opponent's score tracks mine exactly, that is confirmation of the equilibrium, not a signal to change.

- Because the outcome hinges on the luck of yield draws once both players play dominantly, there is no profitable deviation and no tilt worth chasing. Any deposit I make can only lower my expected score relative to retention.

- The only audit risk is depositing more than I declared. Since I always declare 10 and never deposit at all, audit failure is impossible for me. I never let a deposit exceed my private yield; over-depositing converts real retained value into nothing, and deposits above my true yield gain zero points.

- Lying is safe in exactly one direction: declare above my yield, never below. Declaring below my yield can only cap a deposit I was never going to make.

- When an opponent deposits heavily and their points climb, I do not chase them; their deposits burn value at half efficiency. And when an opponent mirrors my retention line, I do not deviate either — matching scores just mean the draw decides.

- Condensed ruleset: declare 10 every round, deposit 0 every round, never deposit above my true yield, don't read anything into a tied scoreline, accept that once both sides play the dominant line only the random yields separate us.