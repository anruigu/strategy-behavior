---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1599
---
### Escort Coordination & Communication
- Use the note stage to coordinate mutual escorts. Name a specific partner explicitly: `[note: <boat>, escort me and I will escort you each round]`.
- Check incoming notes and point totals to see if bots are coordinating. Notice that bots like Foxtrot and Gamma often post generic `"steady on station"` notes and may default to a fixed pairing (e.g., Gamma and Foxtrot escorting each other, as evidenced by Gamma's score surge).
- If the proposed escort partner does not reciprocate after round 1 or is obviously paired with the other boat, immediately pivot note proposals and salvage nominations to the other boat.
- In the escort/salvage stage, always submit `[salvage: <boat>]` corresponding to the best candidate for mutual matching rather than `[salvage: none]`.

### Firing & Harbor Strategy
- Follow standing orders and fire at the designated target station round the picket: `[target: <boat>] [fire: n]`.
- Do not fire on Harbor under normal circumstances; Harbor's retaliation will put me off the board for the rest of the patrol.
- Vary firing coordinates across rounds (1–9) to search for the target's hide pattern. If a target is hit at coordinate $n$, test adjacent or repeated cells depending on their movement tendency.

### Hiding
- Vary my hide cell unpredictably between 1 and 9 each round.
- Never hide in the cell the upstream shooter targeted last round, especially if they scored a hit on that coordinate.

### Claims
- Strictly report the true private result from the office report (`[claim: hit]` on a hit, `[claim: miss]` on a miss).