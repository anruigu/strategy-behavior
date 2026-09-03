---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1412
---
# Playbook: Quiet Sonar

### Rules and Mechanics Clarifications
- Cell coordinates (1–9) represent discrete positions along a line.
- The referee strictly validates that claims match private outcomes. Truthful reporting is required: never bluff or misreport.

### Claim Stage
- When the referee reports `HIT`, output `[claim: hit]`.
- When the referee reports `MISS`, output `[claim: miss]`.

### Hide Stage
- Identify the player targeting me (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
- Review the past firing history of the player who targets me from the round summaries.
- Avoid the specific cells my shooter has targeted recently (e.g., if they repeatedly fire into the 3–5 range, hide in the low 1–2 or high 7–9 ranges).
- Never hide in the cell my shooter fired at in the previous round.

### Fire Stage
- Identify my fixed target (e.g., if I am Gamma, target is Harbor).
- Track which cells I have already fired at my target and missed. Do not repeatedly probe the exact same cell (like firing 4 or 5 round after round) when it consistently misses.
- Observe other players' hits and fires to infer target behavior: if a player is consistently hit or missing in a specific sector, adjust fire coordinates across untried sectors (rotate through low 1–3, mid 4–6, high 7–9).
- Actively sweep across new coordinates across rounds 1–6 rather than concentrating shots on a single static zone.