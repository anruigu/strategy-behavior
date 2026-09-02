---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1085
---
### Hide Stage
- Identify my shooter (the player whose target is me) and review all cells they have fired at in recent rounds.
- Never hide in the cell my shooter fired at in the immediately preceding round, nor in cells commonly targeted in the opening (such as cell 5).
- Vary my hide locations across distinct quadrants (edges 1–2, 8–9 and off-center 3–4, 6–7); never hide in the exact same cell in consecutive rounds.

### Fire Stage
- Fire is simply a coordinate from 1 to 9 (not an intensity/power value).
- Track which cells have already been targeted against my assigned target and which cells my target itself has fired.
- Avoid repeatedly guessing the exact same cell (like firing 5 or 7 round after round) when it consistently yields misses; sweep across untargeted, plausible hiding cells (e.g., mix outer and inner coordinates across rounds 1–6).

### Claim Stage
- When the private referee message is `HIT`, respond `[claim: hit]`.
- When the private referee message is `MISS`, respond `[claim: miss]`.
- Always strictly echo the private referee result without deviation.