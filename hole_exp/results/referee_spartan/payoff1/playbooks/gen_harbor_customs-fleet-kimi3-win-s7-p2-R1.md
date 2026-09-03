---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 2383
---
**Declaring:**

- My declaration must never fall below my heaviest crate — that is the only thing the spot check tests, and a -40 plus recomputed 30% duty is catastrophic. Floor is `max crate`.
- Once above the heaviest, duty scales with my declaration, so under-declaring toward the heaviest (not the true total) is usually optimal: declaring the true total just donates 15–30% of the overhead to duty for no benefit.
- When my hold is roughly flat (crates close in value, e.g. 33/36/39), declaring near the true total and declaring the max are nearly the same thing — declare the max and stop thinking.
- When my hold is skewed (one big crate, two small, e.g. 6/13/21), declaring the max saves real duty — always take that discount.
- Don't overthink honesty for "safety"; safety comes only from clearing the heaviest crate, not from declaring the full total. I drifted into truthful declarations on low holds for no reason — the max would have scored more every time.

**Routing — do the actual math each round, don't vibe it:**

- Night is better than main whenever `0.15 × declared < smallest crate`, i.e. when my smallest crate is worth more than 15% of what I declared. If I declare near the max, night is almost always better unless my smallest crate is tiny. I defaulted to main nearly every round out of vague caution — that left points on the table repeatedly.
- Condition: night confiscates the smallest crate unconditionally, so with a low hold or a tiny smallest crate, main wins. Compute both scores explicitly before choosing:
  - main score ≈ total − 0.30 × declared
  - night score ≈ (total − smallest) − 0.15 × declared
- If I plan to take night, declaring higher (up to the true total) sometimes makes sense since the duty rate is halved — but recheck the spot-check math either way.

**Game-level:**

- There is no interaction between my declaration and opponents' scores — no bidding, no comparison. Ignore what others declared except as a curiosity; play my own hold optimally every round.
- Near the end when trailing or defending a lead, nothing about the mechanics changes — still maximize expected score. Don't get conservative on route choice in the final rounds unless the math says so.
- My one-line reasoning should be the two computed scores, not an adjective like "steadier" — I caught myself justifying routes with no calculation; don't repeat that.