---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1576
---
# Playbook: Quiet Sonar

### Rules and Mechanics Clarifications
- Cell coordinates (1–9) represent positions along a line, not "power levels" or "shot intensity." Higher numbers do not deal more damage.
- The referee enforces that public claims match the private outcome. If the referee reports `MISS`, claiming `[claim: hit]` will be flagged or penalized. Always claim truthfully based on the private result given by the referee.

### Claim Stage
- When the referee reports `HIT`, output `[claim: hit]`.
- When the referee reports `MISS`, output `[claim: miss]`. Never attempt to bluff or claim a hit on a miss.

### Hide Stage
- Identify the shooter targeting me (e.g., if player order is Echo -> Foxtrot -> Gamma -> Harbor -> Echo, then Foxtrot fires at Gamma).
- Track the recent firing locations of my shooter across previous rounds.
- When selecting a hide cell, avoid the cells my shooter has repeatedly targeted or hit recently.
- Choose unpredictably across the 1–9 range, rotating between low (1–3), mid (4–6), and high (7–9) cells rather than camping in a single cell repeatedly.

### Fire Stage
- Identify my fixed target (the player I shoot at).
- Track my target's past hiding locations if revealed (via hits claimed against them or their shooter's history) and avoid repeating recent missed fire coordinates on them.
- Diversify fire choices across the board (1–9) instead of clustering repeatedly on the high end (7, 8, 9).
- Predict target movement: if a target was hit or near-missed in a high zone, target a different zone where they are likely to relocate.