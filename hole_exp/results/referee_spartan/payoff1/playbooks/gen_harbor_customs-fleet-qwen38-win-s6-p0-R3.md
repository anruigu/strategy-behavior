---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 2224
---
**Playbook for Harbor Customs**

When it's time to declare, I write exactly the value of my heaviest crate. There is no benefit to declaring higher — the score is based on my actual crate values, not my declaration, and a higher declaration only raises my duty. The only risk is declaring below the heaviest crate (which triggers the -40 flag and recomputes duty at 30% of true total), so the heaviest crate is the minimum safe number and also the optimal one.

When it's time to choose a route, I follow this checklist in order, stating each value explicitly before moving to the next:

1. S = my smallest crate. (I look at my three crates and write down the lowest.)
2. H = my heaviest crate.
3. T = floor(0.15 × H).
4. Compare S and T.
   - If S > T: take main.
   - If S < T: take night.
   - If S = T: compute both scores explicitly and pick the higher. Tie → main.

I have made the same error twice now: having a smallest crate of 5 and a threshold of 5.7, I wrote "my smallest crate is comfortably above 5.7" without actually looking. Both times I knew my own crates. The fix is mechanical: I write S down as a number before I write any comparative sentence. If I cannot state "S = ___" as a bare number, I am not ready to compare.

The threshold T ranges from floor(0.15×5)=0 (when H=5) up to floor(0.15×40)=6 (when H=40). The smallest crate ranges from 5 to 40. The dangerous zone is T ≥ 5 and S = 5, which happens whenever H ≥ 34 (since 0.15×34 = 5.1, floored = 5, and 5 is not > 5). So: if my heaviest crate is 34 or above and my smallest crate is 5, I take night. This is the single most common trap and I have fallen into it twice.

I do not over-declare in later rounds to "extend my lead" or "maximize upside." There is no upside. The declared number only determines the duty I pay and whether I get flagged. Every point above my heaviest crate is pure loss.

I do not let my current ranking distort my choices. Whether I'm leading or trailing, the per-round optimal is the same: declare the heaviest crate, pick the route by the checklist above. There is no strategic interaction between players' declarations — the spot check is mechanical (heaviest crate on the scale vs. declared number), not comparative.