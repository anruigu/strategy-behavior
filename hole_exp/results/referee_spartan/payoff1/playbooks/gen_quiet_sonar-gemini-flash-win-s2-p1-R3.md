---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1568
---
# Playbook: Quiet Sonar

### Rules and Setup
- The numbers 1–9 represent a line of 9 spatial board cells.
- The targeting cycle is fixed (e.g., Echo->Foxtrot->Gamma->Harbor->Echo). Always verify who is firing at me and who my target is.
- A claim strictly must match the private result: `[claim: hit]` on a private hit, `[claim: miss]` on a private miss.

### Hiding
- Identify my direct attacker and track their firing history shown in round summaries.
- If my attacker is fixated on a specific cell or zone (e.g., constantly shooting 5 or 7), hide far away in a cold sector (such as 1, 2, 8, or 9).
- Even when safe, vary my hiding spot across safe sectors periodically to avoid becoming predictable if the attacker suddenly switches.
- If my attacker changes targets or hunts dynamically, randomize across distant unprobed cells.

### Firing
- Identify my direct target. Track where they hide (deduced from where they shoot, if they follow patterns, or from where they are attacked).
- Do not repeat a fire coordinate immediately after a miss. Systematically probe across unsearched zones (low: 1–3, mid: 4–6, high: 7–9).
- Observe the target's firing choices: opponents often avoid hiding where they fire, or conversely mirror their own fire coordinate; test these hypotheses when probing.
- Once a hit is confirmed, decide whether to re-target the same cell (if the player tends to stay) or target adjacent cells ±1 to catch a shift.

### Claiming
- When the referee reports `HIT`, submit `[claim: hit]`.
- When the referee reports `MISS`, submit `[claim: miss]`.