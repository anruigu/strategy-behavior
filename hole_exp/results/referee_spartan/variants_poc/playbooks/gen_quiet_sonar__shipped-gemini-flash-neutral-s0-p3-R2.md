---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1144
---
- When the rule requires claims to match the private result, always submit `[claim: hit]` when the referee informs me of a hit, and `[claim: miss]` when informed of a miss.

- When selecting a cell to hide in:
  - Identify the shooter assigned to me (e.g., Gamma if I am Harbor).
  - Track that shooter's recent fire history and avoid any cells they have targeted recently.
  - Avoid repeating the same hide location across consecutive rounds.
  - Prefer unprobed peripheral and off-center cells (e.g., 1, 2, 8, 9) while rotating unpredictably to avoid being anticipated.

- When selecting a cell to fire at:
  - Identify my assigned target (e.g., Echo if I am Harbor).
  - Never spam the exact same cell across consecutive rounds after a miss.
  - Cycle systematically through unexplored coordinates across rounds (e.g., test 2, 4, 6, 7, 8, 9 rather than repeatedly re-probing 3).
  - Pay attention to where my target fires and whether other players' successful hits reveal hide habits for the table.

- Format every action cleanly with a single brief line of reasoning followed immediately by `[hide: n]`, `[fire: n]`, or `[claim: hit|miss]`.