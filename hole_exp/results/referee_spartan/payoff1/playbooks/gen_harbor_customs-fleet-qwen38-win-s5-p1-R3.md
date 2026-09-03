---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 1585
---
**Playbook for Harbor Customs**

When I get my three crates, I immediately identify my heaviest and my smallest. I always declare exactly my heaviest crate's value. The spot check flags any declaration below the heaviest crate (−40 penalty plus duty recomputed at 0.30 × true total). Declaring above the heaviest only raises my duty with no benefit. So the heaviest is the unique optimal declaration.

For the route choice, I compare:
- Main: (sum of all three) − floor(0.30 × heaviest)
- Night: (sum of all three − smallest) − floor(0.15 × heaviest)

Night beats main only when smallest < floor(0.30 × heaviest) − floor(0.15 × heaviest). I compute that gap explicitly each round. In practice the gap is 5 or 6 for heaviest values 30–40, and 1–4 below 30. Since the minimum crate value is 5, night wins only in one narrow case: heaviest is 39 or 40 AND my smallest crate is exactly 5. Every other time I take main without hesitation.

I do not over-declare to "close the gap" on other players or to "go all in." The scoring is absolute, not relative. My score this round depends only on my own declaration, my own route, and my own crates. What other players declare or score has zero effect on my points.

I do not declare my true total. That would add unnecessary duty on every round. The true total is relevant only as the sum in the route comparison above.

When I see other players declaring extreme values or making unusual route choices, I do not follow suit. I play my own hand optimally and ignore the leaderboard except to confirm I'm tracking my own running total correctly.