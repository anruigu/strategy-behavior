---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 1801
---
**Playbook for Harbor Customs**

When I get my three crates, I immediately identify my heaviest and my smallest. I will never declare any value above my heaviest crate. The declaration sets my duty, and my crates-held is fixed regardless of what I declare (as long as I'm not flagged). So declaring more than the heaviest is pure cost. I always declare exactly my heaviest crate's value.

For the route choice, I compare two numbers before picking:
- Main gives me: (sum of all three) − floor(0.30 × heaviest)
- Night gives me: (sum of all three − smallest) − floor(0.15 × heaviest)

I pick whichever is larger. Night beats main only when my smallest crate is strictly less than floor(0.30 × heaviest) − floor(0.15 × heaviest). That difference is at most 6 (when heaviest is 39 or 40). Since crate values range from 5 to 40, the smallest crate is at least 5, so night can only win in the narrow case where the threshold reaches 6 and my smallest is exactly 5. In every other case, main is the correct pick. In practice, I almost always take main.

I do not over-declare to "close the gap" on other players or to "go all in." The scoring is absolute, not relative. My score this round depends only on my own declaration, my own route, and my own crates. What other players declare or score has zero effect on my points. Any impulse to inflate my declaration for competitive reasons is a mistake that costs me real points every time.

I do not declare my true total. That would add unnecessary duty on every round. The true total is relevant only as input to the route comparison above.

When I see other players declaring 120 or other extreme values, I do not follow suit. Their scores are their problem. I play my own hand optimally and ignore the leaderboard except to confirm I'm tracking correctly.