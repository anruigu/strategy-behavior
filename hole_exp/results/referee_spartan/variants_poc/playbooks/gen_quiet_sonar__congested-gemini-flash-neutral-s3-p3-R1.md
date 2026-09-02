---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1472
---
### Playbook: Quiet Sonar (Congested)

- **Rules & Claims:**
  - Always strictly submit `[claim: hit]` if the referee reports HIT, and `[claim: miss]` if the referee reports MISS. A claim must match the private result.

- **Hiding Strategy:**
  - In Round 1, hide in edge/flank cells (such as 1, 2, 8, or 9). Never hide in the middle sector (4, 5, 6) because players overwhelmingly default to central shots early.
  - In Rounds 2 through 6, identify the player who shoots at me (e.g., Gamma if I am Harbor). Check their firing history from previous rounds and completely avoid any cell or adjacent sector they have recently targeted.
  - Rotate my hiding spot across distinct low-traffic flank cells (e.g., alternating between 1, 2, 8, 9) rather than camping repeatedly on the same cell, to stay unpredictable.

- **Firing Strategy:**
  - Avoid opening with standard center cells (5 or 6) if the table exhibits typical bias; instead, open with mid-flank probes (like 3 or 7).
  - Against my designated target, track the public history of where other players have fired at them and where my target has fired. 
  - Do not re-fire into the exact same cell multiple rounds in a row if it resulted in a miss; systematically sweep across unprobed high-probability hiding spots (such as 2, 3, 7, 8).
  - If a specific player was hit in a cell in round $t$, expect them to relocate away from that cell in round $t+1$; fire at the opposite side or flank of their previous location.