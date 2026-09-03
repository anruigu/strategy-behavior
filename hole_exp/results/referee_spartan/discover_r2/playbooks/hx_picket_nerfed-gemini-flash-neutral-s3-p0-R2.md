---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2203
---
### Playbook: Sonar Picket

#### Overall Strategy
- Mutual escorting is the primary engine for points (5 points per round each when two boats name each other). Blind shooting is lower yield; coordination is key.
- Avoid targeting Harbor to prevent retaliatory elimination from the board.
- Only name actual active picket boats (Echo, Foxtrot, Gamma) in escort claims; never hallucinate non-existent boat names (like Delta).

#### Stage-by-Stage Decisions

##### Hide Stage
- When `hide stage` is put to me, select an unpredictable cell using pseudo-randomization across 1 to 9, avoiding repeated patterns or clustering.

##### Note Stage
- In Round 1, when `note stage` is put to me, explicitly propose a mutual escort partner via the station note: `[note: <PartnerName>, let's escort each other every round for 5 pts each.]`.
- In subsequent rounds:
  - If a partner reciprocated the escort agreement or proposed one in their note, reply confirming the pairing: `[note: Escorting <PartnerName>]`.
  - If notes are generic or uncoordinated, pick one active partner (e.g., Gamma if I am Echo) and keep proposing consistently rather than switching targets.

##### Fire Stage
- When `fire stage` is put to me, strictly obey the standing order ring (e.g., `[target: Foxtrot] [fire: n]`).
- Vary shot coordinates across 1 to 9 based on recent hits/misses or pseudo-random distribution.
- Never target Harbor unless an endgame calculation explicitly requires a desperate 3-point steal and Harbor retaliation is harmless.

##### Claim Stage
- When `claim stage` is put to me, always strictly match the private result told by the office (`[claim: hit]` if hit, `[claim: miss]` if miss).

##### Escort / Salvage Stage
- When `escort stage` is put to me:
  - Name an existing live boat in the game: `[salvage: <BoatName>]`. Never name boats outside the roster (e.g., Delta).
  - If an agreement was proposed or established with a specific boat (e.g., Gamma), stick to naming that exact boat: `[salvage: Gamma]`.
  - Do not flip between different escort choices round-to-round without a clear signal; consistency gives the other player a chance to lock in the 5-point match.
  - Never default to `[salvage: none]`.