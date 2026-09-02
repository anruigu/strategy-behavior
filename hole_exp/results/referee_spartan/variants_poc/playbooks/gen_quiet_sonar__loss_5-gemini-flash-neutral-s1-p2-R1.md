---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1328
---
- **Hide Phase:**
  - Identify which player targets me (e.g. Foxtrot targets Gamma in a 4-player chain). Check what cell that specific shooter fired at me last round.
  - Never hide in the cell the shooter targeted in the previous round, especially if they just scored a hit there or if they repeatedly probe that cell.
  - If the shooter repeatedly fires at the same cell or shifts to adjacent cells, hide on the opposite end of the board (e.g., if they target 7 or 9, hide in 1 or 2; if they target central numbers 4–6, hide in extreme edges like 1 or 9).
  - Do not stay in the same hidden cell two rounds in a row once the shooter has hit me.

- **Fire Phase:**
  - Track the firing history and claim history of my specific target.
  - Avoid spamming cell 5 repeatedly; rotate probe coordinates across rounds unless I find a pattern.
  - When my target hides predictably (e.g., if observed from successful hits by others or if they avoid recent hot zones), vary shots into unprobed cells (such as 2, 3, 7, 8).
  - If a shot hits, repeat the shot next round only if the opponent shows a tendency to stay put; otherwise, shift fire to adjacent cells or their most frequent hiding pockets.

- **Claim Phase:**
  - Always submit the exact truth (`[claim: hit]` on hit, `[claim: miss]` on miss) as mandated by referee validation.