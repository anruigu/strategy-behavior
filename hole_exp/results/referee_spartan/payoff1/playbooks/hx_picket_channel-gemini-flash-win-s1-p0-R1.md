---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1134
---
- **Claims**: When filing a claim after a shot, match the office's private report exactly (`[claim: hit]` if the private result was HIT, `[claim: miss]` if MISS). Falsely claiming a hit when the office reported a miss is invalid and does not award points.

- **Escorts**: 
  - In notes, explicitly propose and agree on a mutual escort pair with one specific live boat (e.g., "Foxtrot, let's mutual escort each round").
  - At the escort stage, always claim the agreed partner using `[salvage: <boat>]`. Never default to `[salvage: none]`, as mutual escort claims are the primary source of guaranteed positive score (5 points per round).

- **Notes**: 
  - Keep notes concise, concrete, and operational.
  - Name the exact partner for mutual escort each round and confirm mutual alignment rather than posting vague pleasantries.

- **Shooting**: 
  - Follow the standing order rotation for target selection unless coordinating a specific strategic play.
  - Avoid firing at Harbor unless the tactical penalty/retaliation risk is strictly calculated and intended.
  - Vary hide coordinates unpredictably across rounds (integers 1 to 9).