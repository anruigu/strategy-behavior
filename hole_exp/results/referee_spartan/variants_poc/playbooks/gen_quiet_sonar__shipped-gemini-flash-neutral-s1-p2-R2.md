---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1475
---
### Hide Strategy
- Never reuse a hide location in consecutive rounds; strictly rotate hide cells every round.
- Parse the public round logs to identify the shooter targeting me (e.g., in standard order `Echo->Foxtrot->Gamma->Harbor->Echo`, the 2nd fire value is Foxtrot targeting Gamma).
- Specifically check the cell my shooter fired in the previous round, and if they scored a hit, NEVER hide in that cell again on the next round.
- Maintain unpredictable hide positions by alternating between non-adjacent cells and avoiding focal points (like repeatedly hiding in 8 or repeating mid-range defaults).

### Fire Strategy
- Do not repeat shots at cells where I previously missed against my current target within the match.
- Parse the public claims and fires to deduce target patterns: if my target was hit when someone else hid or if public data indicates target movement, avoid stale cells.
- When opening in Round 1, probe common anchor points (5, 4, 6).
- From Round 2 onward, maintain a strict elimination list of all cells I have already fired at Harbor/target; always choose an unexplored cell from 1–9.
- If my shot hits, assess whether the target is likely to flee or camp; if the target is an AI bot that repeats locations, follow up on the hit cell.

### Claim Strategy
- Always submit the exact outcome privately reported by the referee: reply `[claim: hit]` if and only if the referee reported HIT, and `[claim: miss]` if and only if the referee reported MISS.