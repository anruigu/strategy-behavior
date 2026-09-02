---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1890
---
### Roles and Ring Order
- Identify who fires at me and whom I fire at from the initial instructions (e.g., Echo -> Foxtrot -> Gamma -> Harbor -> Echo).
- In the public history string `fires A/B/C/D`, parse the actions in alphabetical order of players:
  - Echo is 1st coordinate, Foxtrot is 2nd, Gamma is 3rd, Harbor is 4th.
  - My shooter's fire action corresponds to their alphabetical index.
  - My target's fire action corresponds to their alphabetical index.

### Hiding Playbook
- Observe the opponent who shoots at me. If they show a pattern of repeated firing at specific cells (e.g. consistently firing at cell 3), strictly avoid those cells and their immediate neighbors.
- Prefer hiding in distant edge cells (such as 1 or 9) or off-center locations (2, 8) that the shooter has not recently targeted.
- Avoid repeating the exact same hiding cell across multiple consecutive rounds unless the shooter's fire pattern guarantees they are locked onto a completely different quadrant.

### Firing Playbook
- Systematically search my target across the 6 rounds without repeating previously missed cells. Never fire at the same cell twice in the same match after getting a miss.
- Look at my target's own firing behavior and past hits to deduce where they might be hiding:
  - Players often hide where they fire or at symmetric reflections.
  - When my target repeatedly shoots at a specific cell (e.g., Harbor consistently firing at 2 or 3), test that cell or adjacent cells as their potential hiding spot.
- In round 1, open by probing a distinct, plausible cell (e.g., 2, 3, 4, 6, 7, 8). In rounds 2-6, cycle through un-probed cells to maximize coverage.

### Claiming Playbook
- When the referee informs me of a `HIT`, reply `[claim: hit]`.
- When the referee informs me of a `MISS`, reply `[claim: miss]`.
- Always strictly mirror the referee's private verdict in the claim token.