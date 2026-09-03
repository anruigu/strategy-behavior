---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2987
---
**Playbook for harbor customs (revised):**

The core mechanic, confirmed across all six rounds: the spot check only flags a manifest whose declared value falls below the heaviest crate, and duty is charged on the *declaration*, not the true total. The dominant declare is almost always **exactly the value of my heaviest crate** — the minimum legal number that avoids the flag. Every round I did this, it held up: no flag, minimal duty. When I feel tempted to declare my true total or something "modest" to hide strength, remember that hiding is worth at most a few points of duty while the flag costs -40 plus duty at 0.30 × the *true* total — a catastrophic swing. Never declare below the heaviest crate, not even slightly.

Route choice is pure arithmetic and I should run it every single time, no intuition:
- main costs 0.30 × declared.
- night costs 0.15 × declared + my smallest crate (lost to confiscation).

So: **night iff (smallest crate) < 0.15 × declared; otherwise main.** With the declaration pinned to my heaviest crate, night is right only when the smallest crate is well under ~15% of the heaviest — a genuinely lopsided hold. Across this episode that condition never came close to holding (smallest crates were 5-20 against break-evens of 3-6), so main was correct every round, and that was borne out. Never pick the route from the "feel" of the declaration ("I declared a big number, so night"); the route interacts with the declaration only through this one formula. Also remember the confiscation happens on the *smallest* crate regardless of the spot check — night's cost is always knowable to me in advance, so there is no uncertainty left in the route decision at all.

Read the other seats' declarations for information, not imitation. Opponents mostly cluster near their heaviest crate too (or round numbers), which tells me the field is playing the same safe line — no exploitable tells emerged, and no reason to deviate from the safe line myself. A seat that flags (-40 swing) loses a round; that's the only large swing in the game besides my own flag risk, which I avoid entirely by the declare rule.

Endgame: the flag-avoidance rule holds even with a lead — a -40 can flip a close scoreboard. If I'm narrowly ahead on the last rounds, prefer main for certainty even if night is arithmetically a point or two better. If I'm narrowly behind, take the arithmetically optimal line and accept the small variance; the game is close enough that a couple of points of duty per round decide it, so never leak duty through sloppy route arithmetic.

One-round summary:
1. Declare = max crate value. Deviate only in true desperation, and almost never even then.
2. Route: night iff smallest crate < 0.15 × declared; else main. Compute it; don't guess.
3. Track opponents' declarations for patterns, but the safe line stays optimal until someone proves otherwise.
4. Never reason about the route from the size of the declaration alone — the formula is the whole story.