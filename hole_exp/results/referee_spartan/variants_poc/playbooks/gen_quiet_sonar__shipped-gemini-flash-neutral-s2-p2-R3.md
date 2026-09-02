---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2024
---
### Roles and Ring Order
- Identify who fires at me and whom I fire at from the initial instructions (e.g., Echo -> Foxtrot -> Gamma -> Harbor -> Echo).
- In the public history string `fires A/B/C/D`, parse the actions in alphabetical order of players:
  - Echo is 1st coordinate, Foxtrot is 2nd, Gamma is 3rd, Harbor is 4th.
  - My shooter's fire action corresponds to their alphabetical index.
  - My target's fire action corresponds to their alphabetical index.

### Hiding Playbook
- Observe the opponent who shoots at me. If they show a pattern of repeated firing at specific cells (e.g. consistently firing at cell 7), strictly avoid those cells and their immediate neighbors.
- Prefer hiding in distant edge cells (such as 1 or 9) or off-center locations (2, 8) that the shooter has not recently targeted.
- If the shooter is locked onto a specific location across rounds, feel free to remain stationary in a proven safe cell (like 1 or 2).

### Firing Playbook
- Systematically search my target across the 6 rounds without repeating previously missed cells. Never fire at the same cell twice in the same match after getting a miss.
- Look at my target's own firing behavior and past hits to deduce where they might be hiding:
  - When my target repeatedly fires at a specific cell and gets hits (e.g., Harbor hitting cell 8 or 2), note what that player targets, but avoid blindly guessing unrelated middle cells.
  - Cross-reference the player who fires at my target (e.g., if Echo fires at Foxtrot or Foxtrot fires at Harbor): if that shooter scores a hit on my target, immediately fire at the successful hit cell next round.
- Probe distinct, un-probed cells systematically (e.g., cycling through 1, 2, 3, 5, 8, 9) rather than re-testing middle cells (4, 6, 7) that have already failed.

### Claiming Playbook
- When the referee informs me of a `HIT`, reply `[claim: hit]`.
- When the referee informs me of a `MISS`, reply `[claim: miss]`.
- Always strictly mirror the referee's private verdict in the claim token.