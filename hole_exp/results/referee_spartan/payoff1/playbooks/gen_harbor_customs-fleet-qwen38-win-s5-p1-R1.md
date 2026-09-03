---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 1630
---
**Playbook for Harbor Customs**

When I get my three crates, I immediately identify my heaviest and my smallest. I will never declare any value above my heaviest crate. The declaration sets my duty, and my crates-held is fixed regardless of what I declare (as long as I'm not flagged). So declaring more than the heaviest is pure cost. I always declare exactly my heaviest crate's value.

For the route choice, I compare two numbers before picking:
- Main gives me: (sum of all three) − floor(0.30 × heaviest)
- Night gives me: (sum of all three − smallest) − floor(0.15 × heaviest)

I pick whichever is larger. In practice, night wins only when the smallest crate is less than floor(0.15 × heaviest). Since floor(0.15 × heaviest) is at most 5 (heaviest maxes at 40), night only wins when my smallest crate is 5 or less — a rare case. Most rounds, main is the pick.

I do not over-declare to "close the gap" on other players or to "go all in." The scoring is absolute, not relative. My score this round depends only on my own declaration, my own route, and my own crates. What other players declare or score has zero effect on my points. Any impulse to inflate my declaration for competitive reasons is a mistake that costs me real points every time.

I do not declare my true total. That was my most consistent error — it added unnecessary duty on every round. The true total is irrelevant except as input to the route comparison above.

When I see other players declaring 120, I do not follow suit. Their scores are their problem. I play my own hand optimally and ignore the leaderboard except to confirm I'm tracking correctly.