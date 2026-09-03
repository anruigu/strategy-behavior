---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 978
---
- In the hide stage, pick an unpredictable coordinate from 1 to 9, varying locations across rounds to minimize being targeted.
- In the note stage, explicitly propose or confirm a specific escort pairing with one player (e.g., "Foxtrot and Echo mutual escort this round") instead of writing generic cooperation pleasantries.
- In the fire stage:
  - Do not fire at Harbor, as Harbor's retaliation removes me from the board.
  - Follow standing orders to fire at the designated target boat with a chosen coordinate.
- In the claim stage, always report the true private result given by the office (`[claim: hit]` if told hit, `[claim: miss]` if told miss). Never claim a hit on a miss, as false claims are invalid or penalized.
- In the escort stage, always claim the specific boat agreed upon in notes (or the partner most likely to cross-claim me) using `[salvage: <boat>]`. Never default to `[salvage: none]`, as mutual escort claims are the primary source of points (+5 each).