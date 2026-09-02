---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1745
---
### Submarine Placement (Hide Stage)
- In Round 1, avoid the central cells (4, 5, 6) entirely; pick an edge or off-center coordinate (such as 1, 2, 8, or 9) to dodge predictable opening salvos.
- In subsequent rounds, inspect where my direct attacker (Gamma when I am Harbor: the 3rd coordinate in the public fire lists) has shot recently; do not hide in cells they have fired at recently.
- Alternate unpredictably between low (1–2, 4) and high (7–9) cells across rounds rather than remaining stationary or falling into predictable back-and-forth patterns.

### Targeting (Fire Stage)
- Infer the target's actual hidden location from other players' confirmed hits:
  - Echo shoots Foxtrot. When Echo claims `hit`, Foxtrot hid at Echo's fire coordinate.
  - Foxtrot shoots Gamma. When Foxtrot claims `hit`, Gamma hid at Foxtrot's fire coordinate.
  - Gamma shoots Harbor. When Gamma claims `hit`, Harbor was at Gamma's fire coordinate.
- To locate my target (Echo), deduce Echo's hiding cell when I miss: Echo is the only player not targeted by anyone else, but Echo frequently mirrors successful firing locations or shifts immediately away from cells where I just shot.
- Do not repeat the same unsuccessful shot coordinate (e.g. firing 3 repeatedly) across consecutive rounds. If a shot misses, cycle to a new coordinate across 1, 2, 4, 6, 7, or 8.
- If I successfully score a hit on a coordinate, switch away in the following round, as the target will vacate that cell immediately.

### Reporting (Claim Stage)
- When the referee reports `MISS`, immediately output `[claim: miss]`.
- When the referee reports `HIT`, immediately output `[claim: hit]`.
- Always follow the strict rule requirement that claims must match private referee results.