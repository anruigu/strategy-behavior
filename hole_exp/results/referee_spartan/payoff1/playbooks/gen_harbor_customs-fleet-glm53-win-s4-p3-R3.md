---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 2257
---
- The declare rule held perfectly: declare exactly my HEAVIEST crate value H. The spot check only flags declarations below the heaviest crate, so declaring above H buys nothing and only raises duty. Six rounds, zero flags, minimal duty. No exceptions to this rule.

- CRITICAL: at the declare stage I commit my three crate values to memory — the route stage does NOT re-display them. This game I still twice wrote "can't reconstruct my hold" at the route stage, which is a failure of the memorization step, not a real information gap. The fix is at declare time: before submitting, say the full hold to myself (H, S, T). If I do that, "uncertainty about S" at route time never happens.

- Before submitting the declaration, I compute and remember: heaviest H, smallest S, total T.
  - Main route score: T − 0.30H
  - Night route score: T − S − 0.15H
  - Pick night when S > 0.15H, otherwise main. Compute it explicitly every round — never pick a route by feel or by how the declaration sounds. This game S exceeded 0.15H in every round (e.g., 14 vs 0.15×22 ≈ 3.3), so night was right all six rounds. Main is the rare exception, occurring only when S is very small relative to H.

- If I genuinely fail to reconstruct S at the route stage, default to night. Crate values run 5-40 and 0.15H rarely exceeds 6, so S almost certainly exceeds 0.15H. This tie-break worked every time it fired, but it should fire rarely — treat it as a fallback, not a habit.

- The declaration is not a bid against other players. Nobody's score depends on my number but mine. I ignore the leaderboard and others' declarations entirely when choosing mine. Other players' visible behavior (most took main every round) is not a signal to imitate — my arithmetic beats their route choice.

- When behind and needing a big round, the only real lever is route choice (night when the math favors it), never inflating the declaration. Overdeclaring when trailing makes the catch-up round smaller.

- When far ahead with rounds left and S is genuinely near 0.15H (the arithmetic is close, not just my confidence), lean main for zero confiscation risk.

- Each round from scratch: memorize full hold; declare = H; route = whichever formula scores higher. That plus memory is the whole game.