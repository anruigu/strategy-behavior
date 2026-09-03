---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2557
---
- The spot check only flags me if my declaration is below my HEAVIEST crate. Declaring anything above that heaviest crate buys nothing — it only raises duty. So when the declare stage is put to me, I declare exactly my heaviest crate value. No exceptions. This held up all six rounds this game: no flags, minimal duty.

- CRITICAL: at the declare stage I write down my three crate values (or commit them to memory deliberately). The route stage does NOT re-display them. Twice this game I "forgot" my smallest crate S and defaulted to main out of caution; that cost me points whenever S > 0.15 × H. When I reach the route stage, I reconstruct my hold from the declare stage — the values ARE known, just not repeated.

- Before submitting the declaration, I check: heaviest crate = H, smallest = S, total = T.
  - Main route score: T − 0.30H
  - Night route score: T − S − 0.15H
  - I pick night when S > 0.15 × H (the crate I lose is worth more than the duty I save), otherwise main. I compute this explicitly each round instead of picking a route by "feel" or by how big my declaration sounds. In practice S is usually well above 0.15H (e.g., 12 vs 0.15×36 ≈ 5.4 in round 6), so night is the usual answer — main is the exception, not the default.

- "Can't verify S" is not a reason to pick main. The route prompt not showing crates is a memory test, not new information. If I truly cannot reconstruct S, I should assume it exceeds 0.15 × H (crate values run 5-40, and 0.15H rarely exceeds 6), so the tie-break under genuine uncertainty is night, not main.

- "Declare high to compete" and "night route suits high declarations" are nonsense I invented. The declaration number is not a bid against other players; nobody's score depends on my declaration but mine. I ignore the leaderboard and other players' declarations entirely when choosing mine.

- When I am behind and need a big round, the only real lever is route choice (night when the math favors it) — not inflating the declaration. Overdeclaring when trailing is exactly backwards: it makes my catch-up round smaller.

- When I am far ahead with rounds left and the night-vs-main comparison is genuinely close (S near 0.15H), I lean main, since main has no confiscation risk. But "close" means the arithmetic is close — not that I feel unsure.

- Each round I recompute from scratch: declare = heaviest crate H; carry S and T forward in memory; route = whichever of the two formulas gives more points. That single rule, plus remembering my hold into the route stage, is all there is to this game.