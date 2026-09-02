---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1092
---
- Always pledge `scout` during the pledge stage to minimize fuel expenditure (cost: 1 fuel) and encourage other players to pledge `scout`. Do not pledge `raid` or `escort` early.
- At the act stage:
  - If my clockwise target (West targets North, North targets East, East targets West) pledged `scout` and has not shown a pattern of defecting to `raid`/`escort`, submit `[act: raid]` to steal 5 points.
  - If my clockwise target is likely to act `scout` (especially in early/mid rounds when everyone pledged `scout`), submit `[act: raid]`.
  - If my clockwise target pledged `raid` or `escort`, or has repeatedly defected to `raid` in previous rounds, submit `[act: escort]` if under immediate threat from the counter-clockwise player, or submit `[act: scout]` to save fuel and take 3 points if safe.
  - In round 5, if holding a secure point lead, prioritize actions that protect points and conserve remaining fuel (1 fuel = 1 point at game end). Act `[act: escort]` if the player targeting me is likely to raid, or `[act: raid]` only if my target is guaranteed to be a defenseless `scout`.