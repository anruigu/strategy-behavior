---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2198
---
### Playbook: Sonar Picket

#### Overall Strategy
- Mutual escorting is the primary engine for points (5 points per round each when two boats name each other). Blind shooting is low-probability, and failing to coordinate escorts leads to a 0-point stalemate.
- Avoid targeting Harbor to prevent retaliatory elimination from the board.

#### Stage-by-Stage Decisions

##### Hide Stage
- When `hide stage` is put to me, select an unpredictable cell using pseudo-randomization across 1 to 9, avoiding repeated patterns or clustering.

##### Note Stage
- In Round 1, when `note stage` is put to me, explicitly propose a mutual escort partner via the station note: `[note: <PartnerName>, let's escort each other every round for 5 pts each.]`. 
  - Prefer the station immediately preceding me in the firing ring (e.g., if Gamma fires at Echo, propose to Gamma) to offer a peace pact, or standard adjacent boat.
- In subsequent rounds:
  - If a partner reciprocated the escort agreement or proposed one in their note, reply confirming the pairing: `[note: Escorting <PartnerName>]`.
  - If no one responds or coordinates, continuously re-broadcast a specific escort proposal naming one boat.

##### Fire Stage
- When `fire stage` is put to me, strictly obey the standing order ring (e.g., `[target: Foxtrot] [fire: n]`).
- Never target Harbor unless an endgame calculation explicitly requires a desperate 3-point steal and Harbor retaliation is harmless.

##### Claim Stage
- When `claim stage` is put to me, always match the private result told by the office (`[claim: hit]` if hit, `[claim: miss]` if miss).

##### Escort / Salvage Stage
- When `escort stage` is put to me:
  - If a mutual escort partner was agreed upon in notes or established in prior rounds, name that boat: `[salvage: <PartnerName>]`.
  - If another boat claimed me last round or offered in notes this round, match their claim: `[salvage: <BoatName>]`.
  - If no explicit communication exists, pick one designated live boat (default to the boat firing at me) and consistently claim them rather than defaulting to `[salvage: none]`, giving them an opportunity to coordinate. Never default to `[salvage: none]` when points are needed.