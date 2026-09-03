---
game: ta_staghunt__shipped
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 979
---
### Playbook: Iterated Stag Hunt

- **Round 1 Strategy:**
  - If the opponent signals cooperation/commitment to stag before the game starts, play `[hunt: stag]`.
  - In the absence of a negative signal, default to `[hunt: stag]` on Round 1 to establish the pareto-optimal equilibrium.

- **Subsequent Rounds Strategy:**
  - If the opponent played stag in the preceding round, continue playing `[hunt: stag]`.
  - If the opponent defected to hare in the preceding round, switch to `[hunt: hare]` to protect against exploitation (avoiding the 1-point sucker payoff) until mutual cooperation is re-signaled or established.

- **Final Round / Endgame:**
  - If mutual stag hunting has held up to the final round, play `[hunt: stag]` through the end rather than defecting, maintaining the 10/10 mutual payoff.

- **Formatting:**
  - Keep reasoning to at most one concise line.
  - End every response strictly with the required bracketed action token: `[hunt: stag]` or `[hunt: hare]`.