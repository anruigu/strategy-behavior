---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1581
---
# Playbook: Quiet Sonar

### Rules and Objective Interpretation
- Remember that the numbers 1–9 are spatial board coordinates, not weapon "power levels".
- The referee strictly enforces that a claim *must* match the private result. Always submit `[claim: miss]` on a private miss and `[claim: hit]` on a private hit.

### Hiding
- Check the targeting sequence (e.g., Echo->Foxtrot->Gamma->Harbor->Echo) to know exactly who fires at me.
- Review recent public fire coordinates of the player firing at me.
- Avoid cells and adjacent neighborhoods that my attacker is actively firing at.
- Relocate unpredictably among cold sectors (e.g., edges 1, 2, 8, 9) if the attacker fixates on central cells (4, 5, 6).
- Do not repeat the same hiding coordinate across consecutive rounds unless the attacker consistently fires far away.

### Firing
- Identify which player is my fixed target and monitor what coordinates they fire from or where other players have missed them.
- Avoid repeatedly spamming the same coordinate (e.g., 4 or 5) after consecutive misses; rotate through untargeted sectors across 1–9 to locate the opponent.
- Pay attention to the target's firing behavior: players frequently mirror their hiding sector or deliberately stay far from their own fire coordinates. Vary probes across distinct zones (low 1–3, mid 4–6, high 7–9).
- If a hit is scored, anticipate whether the target is likely to hold or shift by 1–2 cells on the next round.

### Claiming
- When the private result is `HIT`, reply `[claim: hit]`.
- When the private result is `MISS`, reply `[claim: miss]`.