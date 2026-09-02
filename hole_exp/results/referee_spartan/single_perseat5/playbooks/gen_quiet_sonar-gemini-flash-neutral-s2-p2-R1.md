---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1515
---
### Roles and Target Ring
- Look at the target ring (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo) and identify the specific opponent firing at me and the specific opponent I am firing at.

### Hiding Playbook
- Never stay camped in the same cell across consecutive rounds (e.g., repeatedly hiding in cell 2 invites repeated hits).
- Check the recent firing history of the player shooting at me.
- Avoid the exact cell my shooter targeted in the previous round, as well as cells they have repeatedly probed.
- Vary hiding locations across the line (1–9), mixing edges (1, 9) and asymmetric mid-points (3, 8), avoiding central default focal points (4, 5, 6) on early rounds.

### Firing Playbook
- Do not repeat shots into the same cell against my target after a confirmed miss unless tracking an inferred relocation pattern.
- If my target was hit in the previous round (whether by me or revealed via score/claim history), anticipate that they will relocate; fire adjacent or at a distant counter-cell rather than re-shooting the hit cell.
- Track my target's own firing and hiding tendencies to avoid burning shots on heavily saturated central cells (5, 6, 7) if the opponent consistently hides elsewhere.
- Spread probing shots systematically across distinct zones (e.g., test 3, 7, 2, 8) rather than looping through 4, 5, 6.

### Claim Playbook
- Always report the private outcome truthfully: reply `[claim: hit]` when the referee reports a hit, and `[claim: miss]` when the referee reports a miss.