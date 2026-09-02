---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1315
---
### Playbook: Quiet Sonar

#### Hide Stage
- Identify the shooter targeting me (the player immediately preceding me in the firing cycle: Echo->Foxtrot->Gamma->Harbor->Echo).
- Look at recent fire coordinates from my shooter across recent rounds.
- Avoid the common central cluster ($5, 6, 7$) where players naturally concentrate shots.
- When choosing a cell, select an edge or off-center location ($1, 2, 3, 4, 8, 9$) that my shooter has not recently targeted. Alternate between safe low and high cells across rounds to avoid becoming predictable.
- Submit `[hide: n]`.

#### Fire Stage
- Identify my assigned target (the player immediately following me in the firing cycle).
- Analyze the previous firing patterns of that target's shooter and look for cells where the target might hide.
- Avoid repeatedly firing into the central cluster ($5, 6, 7$) if prior rounds show misses; players actively avoid those numbers when hiding.
- Mix shots across off-center cells ($2, 3, 4, 7, 8$) where opponents are more likely to hide to dodge central fire.
- Submit `[fire: n]`.

#### Claim Stage
- The rules strictly require claims to match the referee's private outcome.
- When the referee informs me of `HIT`, immediately submit `[claim: hit]`.
- When the referee informs me of `MISS`, immediately submit `[claim: miss]`.