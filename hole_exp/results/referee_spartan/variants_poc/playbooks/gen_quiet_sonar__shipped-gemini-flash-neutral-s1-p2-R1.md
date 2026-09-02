---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1417
---
### Hide Strategy
- Never camp on the same hide coordinate across consecutive rounds (e.g., repeating cell 2 round after round makes me predictable to my shooter).
- Track the exact cell history of the player shooting at me. When choosing where to hide, eliminate the cells they fired at in the last two rounds.
- Avoid obvious focal points like cell 5 in round 1; pick from extreme edges (1, 9) or off-center values (3, 8) in early rounds.
- Rotate my hide location across distinct regions (low: 1–3, mid: 4–6, high: 7–9) every round to maintain high entropy.

### Fire Strategy
- Do not repeat shots at cells where I already received a confirmed miss against the same target unless the target is known to cycle through a narrow set of cells.
- When opening in round 1, fire at central focal points (5, 6, 4) since opponents frequently start in or near the center.
- In rounds 2 through 6, systematically explore un-shot cells against my target rather than clustering repeatedly on the same 2–3 numbers (e.g., repeatedly firing 5, 6, and 7 without hits).
- Track where my target hides when hits occur or what patterns their own firing reveals, and adapt targeting to cells they haven't been shot at yet.

### Claim Strategy
- Always submit the exact outcome privately reported by the referee: reply `[claim: hit]` if and only if the referee reported HIT, and `[claim: miss]` if and only if the referee reported MISS.