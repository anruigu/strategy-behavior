---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 2560
---
I never declare more than my largest crate's value. Duty is charged on the declared number, so every point above the spot-check threshold (my heaviest crate) is pure loss. Declaring exactly the heaviest crate is never flagged and minimizes duty. This episode confirmed it across both weak holds (17-18-25, declare 25) and strong ones (8-33-38 and 17-36-38, declare 38): in every round the optimal declaration was exactly the heaviest crate.

I never declare below the heaviest crate. The -40 flag plus recomputed duty at 0.30 × true total dwarfs any saving, and the heaviest crate is always the one checked. Under-declaring is not a tactic, ever.

For the route, I compare the two real costs with my exact known crates and pick the cheaper:
- main costs floor(0.30 × declared).
- night costs floor(0.15 × declared) plus the value of my smallest crate.
I take night only when smallest < floor(0.30 × d) − floor(0.15 × d). At the route stage I already hold the exact crates — I never write "absent indication" or "unless" as if guessing. I plug the real smallest-crate value in every round. This episode the comparisons were: R1 smallest 8 vs saving 5 → main by 3; R2 smallest 26 vs saving 4 → main; R3 smallest 23 vs saving 4 → main; R4 smallest 20 vs saving 5 → main; R5 smallest 17 vs saving 3 → main; R6 smallest 17 vs saving 5 → main. Main was correct six times out of six, but only because the arithmetic said so, not because "main is the default."

When the night route is right, I take it without hesitation — typically when declared ≥ ~28 (so the duty saving is ≥ 5) AND my smallest crate is tiny (single digits), i.e. a lopsided hold like 5-6-38. That configuration hasn't appeared yet; when it does, I expect myself to recognize it and actually route night.

My decision procedure each declare stage: read heaviest crate H, declare exactly H. Each route stage: compute main duty = floor(0.30 × H), night cost = floor(0.15 × H) + smallest; pick the smaller. Net score = true total − that cost. No intuition, no rounding "close enough."

I ignore other players' declarations and scores entirely. Nothing in the rules creates interaction — no shared pool, no relative payoff, no way their manifest affects my crates or duty. This episode the whole table declared near their heaviest crates and routed main every round, matching my play; that neither validates nor changes anything. Scoreboard gaps, endgame urgency, and "pressure" are noise — round 6 math is identical to round 1 math, and I never gamble on under-declaring or over-declaring to catch up.