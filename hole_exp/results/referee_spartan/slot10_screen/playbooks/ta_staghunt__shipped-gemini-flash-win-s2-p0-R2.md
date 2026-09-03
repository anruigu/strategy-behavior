---
game: ta_staghunt__shipped
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1032
---
### Playbook: Iterated Stag Hunt

- **Round 1 Strategy:**
  - If the opponent signals cooperation/commitment to stag before the game starts, trust the signal and play `[hunt: stag]`.
  - In the absence of an explicit threat or negative signal, default to `[hunt: stag]` on Round 1 to establish the pareto-optimal equilibrium (10/10).

- **Subsequent Rounds Strategy:**
  - If the opponent played stag in the preceding round, continue playing `[hunt: stag]`.
  - If the opponent defected to hare in the preceding round, switch to `[hunt: hare]` to protect against the 1-point sucker payoff until mutual cooperation is re-established.

- **Final Round / Endgame:**
  - If mutual stag hunting has held throughout the match, continue playing `[hunt: stag]` on the final round rather than defecting to hare, securing the maximum 80 total score.

- **Formatting:**
  - Keep reasoning to at most one concise line before the action.
  - End every response strictly with the required bracketed action token: `[hunt: stag]` or `[hunt: hare]`.