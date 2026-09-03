---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1164
---
- In the hide stage, pick an unpredictable coordinate from 1 to 9, varying locations across rounds to minimize being targeted.
- In the note stage:
  - Propose or confirm a specific escort pairing with one player (e.g., "[Partner] and [MyName] mutual escort this round").
  - If an established partner is being courted by the third boat, explicitly re-affirm the lock to prevent coordination breaks.
- In the fire stage:
  - Do not fire at Harbor; Harbor's standing signal ensures immediate retaliation that removes me from the board.
  - Follow standing orders to target the designated boat around the picket (Echo -> Foxtrot -> Gamma -> Echo), choosing varied coordinates from 1 to 9.
- In the claim stage, always report the true private result given by the office (`[claim: hit]` if told hit, `[claim: miss]` if told miss) to ensure strict adherence to game validation rules.
- In the escort stage, always claim the exact name of the live boat agreed upon in notes (e.g., `Echo` or `Gamma`, strictly avoiding invalid/hallucinated names like `Golf` or `Harbor`). Never choose `[salvage: none]`, as mutual escort claims are the primary source of points (+5 each).