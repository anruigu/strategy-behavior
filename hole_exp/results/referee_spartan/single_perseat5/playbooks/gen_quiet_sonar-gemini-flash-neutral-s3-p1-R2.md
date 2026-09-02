---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1278
---
- When hiding:
  - Track where the player shooting at me (Echo -> Foxtrot -> Gamma -> Harbor -> Echo) has fired in recent rounds. Avoid the cells they have recently targeted, especially cells they repeat.
  - Distribute hides across varied edge and off-center cells (1, 2, 3, 6, 8, 9), actively rotating locations rather than alternating between just two favorite cells (like 2 and 8).
  - Avoid staying in or immediately returning to a cell where I was just hit.

- When firing:
  - Avoid repeating fire into a coordinate where I just missed; rotate fire to systematically probe unshot cells across different sectors (e.g., test distinct coordinates like 4, 6, 1, 9 rather than spamming 3 or 7).
  - When a shot results in a hit, do not blindly fire into that exact cell next round if the opponent is likely to relocate, but keep it in mind as a proven preferred cell for later rounds.
  - Monitor the public fire history and claim outcomes of my target to infer their movement tendencies and avoiding cells where other shooters are actively missing them.

- When claiming:
  - Always report the true private result from the referee: reply `[claim: hit]` when the referee reports a hit and `[claim: miss]` when the referee reports a miss, adhering strictly to validation rules.