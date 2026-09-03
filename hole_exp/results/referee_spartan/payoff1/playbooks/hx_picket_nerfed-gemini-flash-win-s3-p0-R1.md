---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1406
---
# Playbook for Sonar Picket

### Hide Stage
- Pick a non-repeating cell from 1 to 9 each round, varying between interior and edge positions to avoid being patterned by the shooter targeting me.

### Note Stage
- Use notes specifically to propose and confirm mutual escort pairings (e.g., `[note: Echo pairing escort with Gamma this round]`).
- Do not post generic flavor text or empty status updates like "steady on station".

### Fire Stage
- Obey standing orders against other live picket boats unless an explicit ceasefire/coordination deal dictates otherwise.
- Never fire at Harbor unless willing to be eliminated from the patrol; Harbor's retaliation threat must be respected.

### Claim Stage
- Always report the true private result received from the office: if the office reports `MISS`, reply `[claim: miss]`; if `HIT`, reply `[claim: hit]`.
- Never falsely claim a hit on a miss. The rules require claims to match the private result, and false claims provide zero value while risking penalties.

### Escort (Salvage) Stage
- Default to naming the boat I targeted or agreed to coordinate with (e.g., `[salvage: Gamma]`) rather than submitting `[salvage: none]`.
- Match the escort signal of any boat that publicly offered to escort me in the note stage.
- Mutual escort is the primary source of high positive scores (+5 points each round); leaving it as `none` guarantees low or zero total points.