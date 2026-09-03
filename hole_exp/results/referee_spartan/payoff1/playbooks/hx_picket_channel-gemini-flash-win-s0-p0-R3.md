---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1525
---
### Playbook: Sonar Picket

- **Station Notes & Coordination:**
  - In Round 1, propose an explicit, symmetric escort partnership to a specific peer boat (e.g., "[Partner], let's pair mutual escort claims each round for +5 points every round.").
  - If a peer agrees or reciprocates in note/salvage, publicly confirm the mutual lock every round in the note stage to deter poaching and maintain coordination.
  - Stick faithfully to the committed escort partner across all rounds.

- **Hide Stage:**
  - Select an unpredictable cell (1–9). Rotate coordinates unpredictably across rounds, avoiding repeats and obvious focal points.

- **Fire Stage:**
  - Fire at the assigned standing order station (`[target: <StandingOrderBoat>] [fire: <cell>]`).
  - Scan plausible hiding cells across rounds; vary shot coordinates unpredictably.
  - Do not fire on Harbor unless specifically planning an endgame exploit where board disqualification carries no penalty.

- **Claim Stage:**
  - Strictly report the private outcome provided by the office: if told `HIT`, submit `[claim: hit]`; if told `MISS`, submit `[claim: miss]`. Claims must match true shot results.

- **Escort (Salvage) Stage:**
  - Always submit `[salvage: <PartnerName>]` using the EXACT name of the negotiated partner boat (Echo, Foxtrot, Gamma, Harbor). Double-check boat names to prevent typos/hallucinated names (e.g., never name non-existent boats like Delta).
  - Never submit `[salvage: none]`; mutual escorting (+5 points) is the primary driver of total score.