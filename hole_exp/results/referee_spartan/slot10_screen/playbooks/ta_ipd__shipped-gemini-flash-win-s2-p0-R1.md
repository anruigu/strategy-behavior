---
game: ta_ipd__shipped
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 721
---
- When facing an opponent who credibly commits to a Grim Trigger strategy (cooperating until I defect, then defecting forever) in a fixed-round game:
  - In all rounds prior to the final round, choose `[move: cooperate]` as long as the opponent has cooperated in every prior round.
  - In the final round, choose `[move: defect]` to capture the 5-point payoff with zero risk of subsequent retaliation.
- If the opponent defects in any round before the end, immediately switch to `[move: defect]` for all remaining rounds to prevent exploitation.
- In general fixed-horizon Iterated Prisoner's Dilemma against a conditional cooperator, maintain mutual cooperation up to the penultimate round and defect on the final round.