---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 1987
---
**Playbook for Harbor Customs**

When it's time to declare, I write exactly the value of my heaviest crate. There is no benefit to declaring higher — the score is based on my actual crate values, not my declaration, and a higher declaration only raises my duty. The only risk is declaring below the heaviest crate (which triggers the -40 flag and recomputes duty at 30% of true total), so the heaviest crate is the minimum safe number and also the optimal one.

When it's time to choose a route, I compute the following precisely, no estimation:

- Let H = my heaviest crate, S = my smallest crate.
- Night threshold T = 0.15 × H.
- If S > T: take main. I keep all three crates and the extra duty (0.30 × H − 0.15 × H = 0.15 × H, floored) is less than the value of the crate I'd lose.
- If S < T: take night. The lost crate is worth less than the duty savings.
- If S = T (within rounding): compute both scores explicitly and pick the higher. When they tie, take main (the floor function on the 30% duty usually rounds down more than the 15% duty, making main marginally better or equal).

I must actually perform this arithmetic every round. In a recent episode I had crates 5, 15, 38 and said "my smallest is almost certainly above 5.7" without checking — it wasn't (5 < 5.7), and I lost a point. The threshold can be as high as 6 (when H = 40) and the smallest crate can be as low as 5, so misses are realistic.

I do not over-declare in later rounds to "extend my lead" or "maximize upside." There is no upside. The declared number only determines the duty I pay and whether I get flagged. Every point above my heaviest crate is pure loss.

I do not let my current ranking distort my choices. Whether I'm leading or trailing, the per-round optimal is the same: declare the heaviest crate, pick the route by the 15% rule. There is no strategic interaction between players' declarations — the spot check is mechanical (heaviest crate on the scale vs. declared number), not comparative.