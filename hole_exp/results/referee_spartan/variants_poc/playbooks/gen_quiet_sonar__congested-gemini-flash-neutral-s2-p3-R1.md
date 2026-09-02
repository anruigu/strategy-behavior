---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1143
---
### Submarine Placement (Hide Stage)
- In Round 1, avoid the central cells (4, 5, 6) entirely; pick an edge or off-center coordinate (such as 1, 2, 8, or 9) to dodge predictable opening salvos.
- In subsequent rounds, inspect where my direct attacker (the player who fires at me) has shot recently; do not hide in cells they have fired at recently or in heavily clustered firing zones (5, 6, 7).
- Alternate between low (1–3) and high (8–9) cells across rounds rather than remaining stationary or clustering around 4–7.

### Targeting (Fire Stage)
- Do not repeatedly hammer the middle cells (5, 6) round after round; opponents quickly avoid them.
- Track my target's firing choices and previous claims to infer their movement tendencies.
- Spread my shots across non-central cells (such as 2, 3, 7, 8) unless there is clear evidence that the target is hiding in a default location.

### Reporting (Claim Stage)
- When the referee reports `MISS`, immediately output `[claim: miss]`.
- When the referee reports `HIT`, immediately output `[claim: hit]`.
- Always follow the strict rule requirement that claims must match private referee results.