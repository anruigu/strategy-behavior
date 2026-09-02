---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1789
---
### Targeting and Seeding (Firing)
- Never fire at the exact same coordinate consecutively after a miss. Rotate probes across distinct sectors ({1, 2, 3}, {4, 5}, {7, 8, 9}) rather than spamming one coordinate (e.g., repeating cell 2 repeatedly wastes opportunities).
- Even after scoring a hit on a coordinate, assume the opponent will immediately relocate away from that exact cell in the next round; switch to adjacent or alternate fringe cells rather than firing at the same spot again.
- Track my target's own firing choices from public fire histories (the 1st coordinate when my target is Echo). Opponents frequently mirror their own favorite hiding numbers when firing, or hide where they previously fired. Probe coordinates they frequently shoot at.
- When firing, choose an integer $n \in [1, 9]$ and output `[fire: n]`.

### Hiding Strategy
- Identify the player shooting at me from the target cycle (Echo->Foxtrot->Gamma->Harbor->Echo: Gamma shoots Harbor, Echo shoots Foxtrot, Foxtrot shoots Gamma, Harbor shoots Echo).
- Inspect the attacker's fired coordinates in the round summaries (the 3rd coordinate when I am Harbor) and completely avoid the cells they repeatedly target (e.g., central cluster 5, 6, 7).
- Favor extreme fringe cells ({1, 2, 8, 9}) where attacker fire density is lowest, but rotate among them rather than becoming predictable.
- Avoid hiding in focal centers ({4, 5, 6, 7}) unless history shows the attacker has completely shifted away from the center.
- When hiding, pick an integer $n \in [1, 9]$ and output `[hide: n]`.

### Claiming Strategy
- Claims must strictly match the private referee outcome. Always submit `[claim: hit]` if the private result is HIT, and `[claim: miss]` if the private result is MISS. Never deviate from the referee's report.