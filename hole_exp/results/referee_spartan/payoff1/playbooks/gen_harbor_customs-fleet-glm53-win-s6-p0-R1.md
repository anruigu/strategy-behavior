---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 1
chars: 2417
---
Write the playbook.</think>**Playbook for harbor customs:**

The core mechanic I underused: the spot check only flags a manifest whose declared value is below the heaviest crate. Duty is charged on the *declaration*, not the truth. So the dominant declare is almost always **exactly the value of my heaviest crate** — the minimum legal number that avoids the flag. When I declared my true total (a big number) I paid duty on value I didn't need to declare, and it cost me real points.

Route choice is pure arithmetic, and I should compute it every time rather than guessing by "feel" or "variance":
- main costs 0.30 × declared.
- night costs 0.15 × declared + my smallest crate (lost).

So when the route decision is put to me, I take **night iff (smallest crate) < 0.15 × declared**, otherwise **main**. With a declaration equal to my heaviest crate, that means: night when the smallest crate is small relative to the heaviest (a lopsided hold), main when the hold is balanced or the smallest crate is chunky. In the final episode I took night on a flat hold (8, 8, 15) — giving up an 8 crate to save about 5 duty — exactly backwards; I also took night in the middle episode with a declaration that made no sense to pair with it. Never pick the route on narrative intuition ("high declared number → night route"); the route doesn't interact with what I declared except through that one formula.

Penalty math: getting flagged costs -40 plus duty recomputed at 0.30 × the *true* total, on top of losing the smallest crate if I went night. That's catastrophic. Never declare below the heaviest crate, not even slightly to look poor — the hiding is worth at most a few points of duty, the flag is worth a huge swing. My "declare modestly to hide strength" plays were dominated by just declaring the heaviest crate.

Endgame adjustment: if I'm comfortably ahead on the final rounds, the flag-avoidance rule still holds (a -40 can flip a lead), but I can be more willing to take main (certain, lower-variance payoff) even when night is arithmetically a point or two better. If I'm behind, take the arithmetically optimal line and accept the variance.

One-round summary:
1. Declare = max crate value. (Deviate only if truly desperate and behind, and even then rarely.)
2. Route: night iff smallest crate < 0.15 × declared; else main.
3. Never reason about routes from the size of my declaration alone — run the numbers.