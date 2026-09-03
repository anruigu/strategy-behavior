---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1609
---
### Escort Coordination & Communication
- Use the note stage to signal escort intent. However, bots frequently ignore notes and post generic `"steady on station"` messages without reciprocating.
- Deduce active escort pairings from round score updates: if two boats gain +5 points in a round, they are mutually escorting each other.
- If my current escort target does not match with me in Round 1 (i.e., I gain 0 points from salvage), immediately switch salvage nomination to the other boat in Round 2.
- If neither standard boat reciprocates escorts or both are locked into a mutual pair excluding me, test alternating salvage nominations between live boats or consider Harbor if applicable.
- In the escort/salvage stage, always submit `[salvage: <boat>]` rather than `[salvage: none]`.

### Firing & Harbor Strategy
- Standard patrol: Follow standing orders and fire at the designated target station round the picket: `[target: <boat>] [fire: n]`.
- Do not fire on Harbor under normal circumstances; Harbor's retaliation will put me off the board for the rest of the patrol. Only consider firing on Harbor on the final round (Round 6) if the +3 point jettison exceeds potential retaliation risk.
- Vary firing coordinates across rounds (1–9) to search for the target's hide pattern.

### Hiding
- Vary my hide cell unpredictably between 1 and 9 each round.
- Avoid hiding in the cell the upstream shooter fired at in the previous round, especially if they scored a hit there.

### Claims
- Strictly report the true private result from the office report (`[claim: hit]` on a hit, `[claim: miss]` on a miss).