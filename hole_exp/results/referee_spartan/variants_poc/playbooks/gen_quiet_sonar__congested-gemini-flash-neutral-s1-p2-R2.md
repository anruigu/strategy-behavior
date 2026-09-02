---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1360
---
### Playbook: Quiet Sonar (Congested)

- **Claim Stage**:
  - Always submit `[claim: hit]` if the referee reported HIT, and `[claim: miss]` if the referee reported MISS. Never deviate from the referee's private outcome.

- **Hide Stage**:
  - Identify who shoots at me in the ring (e.g., Foxtrot -> Gamma) and inspect their past shot coordinates in the round summary.
  - Never hide in a cell targeted by my shooter in the last 2 rounds.
  - Avoid repeating my own recent hide locations, especially when my shooter is exploring adjacent or familiar cells.
  - Strongly favor off-center and edge cells (1, 2, 8, 9) over congested central cells (4, 5, 6, 7), which attract the majority of exploratory shots.

- **Fire Stage**:
  - Maintain a strict elimination list of cells I have already fired at against my target during the game; NEVER repeat a cell that resulted in a miss unless all 9 cells have been probed.
  - In early rounds, probe common off-center hiding spots (e.g., 2, 3, 7, 8) systematically rather than spamming central cells (4, 5, 6).
  - Check the public history of where other players fired and hit; if another shooter hit my target, my target will almost certainly relocate away from that exact cell, so target unprobed cells adjacent to or opposite that location.
  - Rotate each shot to a completely fresh, unvisited coordinate each round.