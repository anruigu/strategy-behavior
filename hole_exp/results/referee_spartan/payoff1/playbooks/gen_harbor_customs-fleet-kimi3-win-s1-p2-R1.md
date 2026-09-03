---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 2101
---
When choosing my declaration, I always compute my true total T, my max crate M, and my min crate m first. The only hard constraint that matters is declaring at least M — anything below M gets flagged for -40 plus recomputed duty. There is never any reward for declaring above my true total; duty is charged on what I declare, so declaring more than needed is pure self-inflicted tax. My default declaration is exactly M, never higher, unless I have a specific reason.

I never declare T out of "honesty" when M < T — that just pays 30% duty on value the harbormaster can't check. Declaring M is always safe (the scale only sees the heaviest crate) and saves 0.3×(T−M) in duty.

For the route, I compare the two optimal plays directly each round rather than defaulting to main:
- main with declare M: score ≈ T − 0.3×M
- night with declare M: score ≈ T − m − 0.15×M
Night wins when m < 0.15×M, i.e., when my smallest crate is tiny relative to my largest. Since that is rare (m usually exceeds 15% of M), main is usually right — but when I hold a junk crate (single digits) alongside a big one, I take night and shed the junk at a discount duty. Check the arithmetic every round; don't auto-pick main out of habit.

I ignore other players' declarations entirely — there is no interaction, no contest, no reason to "declare high to discourage" anyone. That reasoning cost me nothing visible but produced inflated declarations; cut it.

Scoreboard position does not change the math within a round: each round's optimal declare/route is independent. If I'm behind late, the correct response is still maximal expected value per round (declare M, best route), not over-declaring, which lowers my score. Over-declaring to "catch up" is the leak I must stop.

Early rounds I play straightforwardly; I don't try low-ball declarations hoping the check misses me — the check is deterministic on the heaviest crate, so under-declaring below M is a guaranteed -40. Never do it.

Summary checklist per round: compute T, M, m → declare exactly M → compute both route scores → take the better (main unless m < 0.15×M).