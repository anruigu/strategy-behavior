---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1897
---
### Target and Shooter Tracking
- Identify who targets me and whom I target from the initial rules (e.g., Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
- Pay close attention to round summaries (`fires a/b/c/d, claims w/x/y/z`): the elements correspond directly to player order (Echo/Foxtrot/Gamma/Harbor).
- Identify where my target was hit in previous rounds: if a shooter claiming a hit against my target is visible in the public summary, note the coordinate that scored the hit.
- Identify where my shooter fired at me in past rounds to avoid their targeting patterns.

### Hiding Stage
- Track the exact cells my designated shooter has fired in recent rounds.
- Never repeat a hide cell immediately if my shooter hit me there, or if my shooter alternates systematically between a few cells (e.g., 3 and 8).
- Avoid cells that my shooter has recently targeted; pick from untargeted low, mid, or high cells.
- Rotate unpredictably between safe cells (e.g., 1, 4, 6, 9) rather than camping on cell 2 or cell 8.

### Firing Stage
- In round summaries, observe where third-party players hit their targets or where my target was hit by others if identifiable.
- Never fire repeatedly at the exact same cell round after round (e.g., 7, 7, 7, 7 or 8, 8, 8, 8) after receiving a miss.
- When a shot misses, systematically eliminate that coordinate and probe a different, unprobed sector (low 1-3, mid 4-6, high 7-9).
- Check the history of public hits scored by my target: bots often repeat or slightly shift their hiding locations or mirror successful spots.
- Distribute probes across unique cells across the 6 rounds to maximize coverage.

### Claim Stage
- When the private result is `MISS`, always submit `[claim: miss]`.
- When the private result is `HIT`, always submit `[claim: hit]`.
- Never submit a false claim, as the referee strictly verifies claims against private results.