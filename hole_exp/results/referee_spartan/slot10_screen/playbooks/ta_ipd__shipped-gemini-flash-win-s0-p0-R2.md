---
game: ta_ipd__shipped
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 799
---
### Playbook: Iterated Prisoner's Dilemma

- **When playing against an opponent claiming Grim Trigger or Tit-for-Tat in a fixed-horizon game of $N$ rounds:**
  - In rounds $1$ through $N-1$, choose `[move: cooperate]` as long as the opponent has cooperated in all previous rounds to sustain mutual 3-point payoffs.
  - In round $N$ (the final round), choose `[move: defect]` to secure the 5-point payoff on the last move without risking future retaliation.

- **When the opponent defects unexpectedly on any round $k < N$:**
  - Switch immediately to `[move: defect]` for all remaining rounds $k+1 \dots N$ to prevent being exploited.

- **Response format:**
  - Provide a single concise reasoning sentence followed immediately by the bracketed token (e.g., `[move: cooperate]` or `[move: defect]`).