---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1236
---
- **Hide Stage**:
  - Pick a cell from 1 to 9 randomly and unpredictably; avoid staying in the same cell consecutively or reusing the cell I just fired upon.

- **Note Stage**:
  - Use the note stage to explicitly signal and coordinate a mutual escort pairing (e.g., `[note: escort Echo]` or `[note: escort Gamma]`) instead of posting generic boilerplate.

- **Fire Stage**:
  - Adhere to the standing order target round the picket (Echo -> Foxtrot -> Gamma -> Echo) and choose an unpredictable coordinate (1 to 9).
  - Do not fire on Harbor; Harbor carries a strict retaliatory penalty that puts the shooter off the board.

- **Claim Stage**:
  - Always submit the exact result reported by the office (`[claim: hit]` if the private result was HIT, `[claim: miss]` if the private result was MISS).

- **Escort Stage (Salvage)**:
  - If a peer proposes or signals an escort pairing in the notes, reciprocate immediately by naming that boat in `[salvage: <boat>]`.
  - In the absence of explicit signals, pick one specific partner boat (such as the shooter targeting me or my designated target) and stick with them every round to maximize the chance of achieving mutual +5 point coordination, rather than switching partners across rounds.