---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2459
---
**Declaring:**

- My declaration must never fall below my heaviest crate — that is the only thing the spot check tests, and -40 plus a recomputed 30% duty is catastrophic. Floor is `max crate`, always.
- Declaring above the max only adds duty; the true total is never useful. **Declare exactly the max, every time.** This episode I reasoned "declare 31" in Round 2 and then declared 75 anyway — the reasoning was right, the action wasn't. Match the token to the math.
- Skewed or flat hold, the answer is the same: declare the max. No exceptions found.

**Routing — do the actual math, with the floor, and then do what it says:**

- Compute exactly, not in decimals:
  - main score = total − floor(0.30 × declared)
  - night score = (total − smallest) − floor(0.15 × declared)
- Night wins exactly when `smallest > floor(0.30 × d) − floor(0.15 × d)`. Since d = max crate, that gap is usually small (d=16: gap 2; d=28: gap 4; d=75: gap 11), so night usually wins — but not always: with d=36 the gap is 5 and smallest 17 clears it, so night was right... yet I wrote "main" in Round 4's reasoning against my own numbers and took main. And in Round 5 (8/9/9, d=9, gap 1, smallest 8 clearly loses... no — night score 17 vs main 24) I computed that main wins and then chose night anyway. **Two lost-round contradictions in six rounds. The failure mode was never the arithmetic — it was outputting the opposite of my computed conclusion.** Before I send a route, re-read my own computed scores and check the token against them.
- Heuristic when in a hurry: with d = max crate, take night unless the smallest crate is under ~half of 0.3×d. Flat low holds (like 8/9/9) are exactly where this fails — smallest is near the max, gap is small, so night fine there too... no: recheck — for 8/9/9 the confiscated crate is worth more than the tiny duty saving only because duties are small either way; compute it, it's two subtractions.

**Game-level:**

- No interaction with opponents — ignore their declarations except as curiosity. My optimum is independent of their play.
- Final rounds are just rounds; the math doesn't change with the standings.
- My written reasoning must contain the two explicit integer scores for the routes before I pick one, and the token must equal the better one. The single new failure I saw this episode was reasoning–action mismatch; the one-line sanity check ("does my token match the bigger number I just wrote?") is now a mandatory step.