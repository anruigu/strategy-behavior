---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1428
---
### Hide Strategy
- Never reuse a hide location in consecutive rounds; strictly rotate hide cells every round.
- Parse the public round logs to track the shooter targeting me (in the fixed order `Echo->Foxtrot->Gamma->Harbor->Echo`, the 2nd fire value is Foxtrot firing at Gamma).
- Explicitly avoid hiding in any cell my shooter fired at recently, especially if they have fired at it multiple times or scored hits there.
- Actively diversify hide choices across the full board (1 through 9); avoid falling into predictable rotation loops (e.g., repeatedly hiding in 8 or 3).

### Fire Strategy
- Do not repeat shots at cells where I previously missed against my target within the same match.
- Maintain a strict elimination list of all coordinates I have already fired at my target; always select an unprobed integer from 1–9.
- Track my target's own firing patterns: bots frequently hide where they fire or in adjacent patterns (e.g., Harbor repeatedly firing at 5/6 while hiding at 8/6).
- If I score a HIT on my target in round $t$, assume the target will relocate in round $t+1$ unless game data proves they are a stationary bot; do not blindly repeat the same fire coordinate unless evidence supports camping.

### Claim Strategy
- Always submit the exact outcome privately reported by the referee: reply `[claim: hit]` if and only if the referee reported HIT, and `[claim: miss]` if and only if the referee reported MISS.