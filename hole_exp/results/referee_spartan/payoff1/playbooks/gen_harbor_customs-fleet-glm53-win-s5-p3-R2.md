---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 3332
---
PLAYBOOK

The core realization holds: other players' declarations, routes, and points are pure noise — my score depends only on my three crates, my declaration, and my route. I never declare "above rivals," "to protect a lead," or for signaling; those reasons have no payoff channel and only inflate my duty. Route choice is pure arithmetic, not risk appetite.

**Fix the route arithmetic first — my old breakeven was wrong.** Sort my crates as a ≤ b ≤ c. The two candidate plays are:
- Main, declaring c: score = a + b + c − 0.30c
- Night, declaring b (smallest is confiscated, so the heaviest crate I still hold is b): score = b + c − 0.15b

Night beats main exactly when 0.30c + 0.15b > a. My old rule ("night iff a > 0.15c") was far too eager — it ignored that night costs me the whole crate a, not just the duty difference. Round 5 (7, 20, 24) is the case in point: 7 > 0.15×24 but 0.30×24 + 0.15×20 = 10.2 > 7, so main was correct and I threw away ~3 points by taking night. With three mid-to-high crates (a large relative to c), night usually still wins; with one small crate, main wins.

**Declare stage:**
- Decide the route first, then declare the value of the heaviest crate I will actually still hold: c if main, b if night. That is the minimum that passes the spot check, and duty scales with the declaration, so any higher number is a pure giveaway.
- Never declare below the heaviest held crate — the flag costs −40 plus duty recomputed at 0.30 × the full true total, which wipes out a round. The spot check is deterministic (the dockhand always weighs the heaviest crate), so there is no gamble to take here.
- Note the confiscation means the declaration for night is b, not c — but only if a is genuinely the smallest; if b and a are close, b is still the heaviest survivor either way, so the rule "declare the largest crate I keep" always applies.

**Route stage:**
- Compute 0.30c + 0.15b and compare to a. Night iff that sum exceeds a.
- Quick sanity checks: if my smallest crate is small relative to my heaviest (roughly a < 0.3c), main is likely right; if the three crates are close in value, night is likely right. Always do the exact sum anyway — it's three multiplications.

**What did not work:**
- Over-declaring (84 on a hold of 84, or 44/55/45 on moderate holds): tripled duty for no gain. The old "S > 0.15×H → night" rule: wrong sign of comparison in spirit — it compared a to the night duty alone and ignored the full loss of crate a. It made me take night on small-crystal rounds where main was better.
- Reading anything into the round-history logs or the points column: no effect on my optimal play.

**General habits:**
- Each round: sort crates, compute 0.30c + 0.15b vs a, pick route, declare the largest crate I keep. Ignore everything on screen about other players.
- If rates differ in a future setup (confiscation rate, duty percentages, penalty size), re-derive the two scores symbolically at the table before round 1 — the structure (minimal legal declaration, then compare route arithmetic exactly, including the full value of any confiscated crate) stays the same.
- Final scores confirmed my play was directionally sound (I finished mid-pack, and the gap traces mostly to the small-crate rounds where the bad breakeven rule cost me points), not to any need to track or outguess rivals.