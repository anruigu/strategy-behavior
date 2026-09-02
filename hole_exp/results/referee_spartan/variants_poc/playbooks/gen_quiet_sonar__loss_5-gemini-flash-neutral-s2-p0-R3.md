---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1572
---
- **Claim Stage**:
  - Always claim `hit` if and only if the referee reported `HIT`.
  - Always claim `miss` if the referee reported `MISS`.
  - Never misreport; the claim must strictly match the private referee result.

- **Hide Stage**:
  - Identify who shoots at me based on the firing order (Echo->Foxtrot->Gamma->Harbor->Echo: Harbor shoots at Echo, which corresponds to the 4th value in `fires` and `claims`).
  - Check the score history to detect if the shooter is hitting every round (e.g. Harbor scoring 4 points every round indicates Harbor is always successfully hitting my hidden cell).
  - Note that in standard play, if Harbor always claims `hit`, they are firing at the exact cell I choose; avoid predictable patterns, fixed defaults, or low-range biases (e.g. repeatedly hiding in 2).
  - Actively randomize across all 9 cells (1 through 9) without favoring mid or low clusters. Never reuse the same cell in consecutive or alternating rounds.
  - Do not hide in cells the shooter fired at recently (e.g. 4, 5, 6).

- **Fire Stage**:
  - Observe public claims: look at the target's incoming fire and hits (e.g. Foxtrot fires at Gamma, Harbor fires at Echo).
  - Foxtrot consistently fires at cell 5 every round (fires pattern: `5` in position 2). If Foxtrot hides where they fire or stays static, test cell 5, 6, 4, or track Foxtrot's previous hits.
  - If a shot misses, do not repeat that coordinate; systematically cycle through untried cells across the board (1 to 9).
  - If a hit is achieved, expect the target to relocate rather than stay stationary.