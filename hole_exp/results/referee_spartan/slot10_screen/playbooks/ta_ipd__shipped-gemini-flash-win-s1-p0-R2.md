---
game: ta_ipd__shipped
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1264
---
### Strategy Playbook: Iterated Prisoner's Dilemma

- When facing an opponent who commits to Grim Trigger, Tit-for-Tat, or conditional cooperation:
  - Play `[move: cooperate]` in every round from round 1 up to the penultimate round ($N-1$).
  - Play `[move: defect]` on the final round ($N$), capturing the 5-point defection payoff (or protecting against mutual defection) with zero risk of future retaliation.

- If the opponent defects unexpectedly on any round before the final round:
  - Abandon cooperation immediately and play `[move: defect]` on every remaining round to avoid sucker payoffs (0 points) and guarantee at least mutual defection payoffs (1 point per round).

- When the total number of rounds is unknown or indefinite:
  - Maintain mutual cooperation via `[move: cooperate]` until the opponent defects, at which point switch permanently to `[move: defect]`.

- What does not work:
  - Do not defect early against a Grim Trigger opponent; defecting early collapses the payoff stream from 3 points/round to 1 point/round across all subsequent rounds.
  - Do not cooperate on the final round when the game horizon is fixed and known; cooperating on round $N$ leaves 2 points on the table regardless of whether the opponent cooperates or defects.