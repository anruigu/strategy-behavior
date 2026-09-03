---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 2238
---
- The single number that gates every declare stage is my heaviest crate. I declare exactly its value: the declaration itself is never scored, it only sets my duty, so anything above the max is pure wasted duty and anything below invites the −40 flag plus recomputed duty at 0.30 of my true total.
- I never declare my full true total. There is no honesty bonus; in past games declaring 75–82 when the check only needed ~40 cost me large duties for nothing. Anchor to the max crate, nothing else.
- I never declare below my heaviest crate. The −40 penalty plus 0.30 × true total duty is always worse than paying 0.30 × max crate up front.
- Route stage: I compute both options from actual crates every time — main = floor(0.30 × declared); night = floor(0.15 × declared) + losing my smallest crate. I take night only when the duty saved (floor(0.30×d) − floor(0.15×d)) is strictly greater than my smallest crate's value.
- In practice, with declared = max crate, the night saving is about 0.15 × max, and my smallest crates have consistently run 6–23, which usually meets or beats that saving. So main is my default and has been correct in essentially every round; night only becomes live when my smallest crate is very small ( roughly < 0.15 × maxcrate) relative to the rest — a rare hold, not a habit.
- I do not let a high declaration push me toward night out of "momentum," and I do not take night because the percentage looks smaller. The only inputs are the two floored duty numbers and my smallest crate.
- The night trade is extra bad when my smallest crate is large relative to the gap between my crates (e.g. 6 when max is 31); I sanity-check by comparing night total cost (duty + lost crate) against main duty directly, not just the duties.
- Late in the game, trailing or leading, I play the same per-round math. Position doesn't change the arithmetic; conservative or greedy deviations from it just leak points.
- The spot check lifts the heaviest crate specifically — I re-derive that from the rules text each episode rather than assuming, since the check could differ in another setup.
- Reply format: one short sentence of reasoning, then the bracketed token alone on a line; never leave the prompt unanswered or ambiguous.