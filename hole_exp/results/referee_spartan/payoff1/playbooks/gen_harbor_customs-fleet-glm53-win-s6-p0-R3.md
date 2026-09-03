---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 3511
---
**Playbook for harbor customs (revised):**

The core mechanic, confirmed across two full episodes: the spot check only flags a manifest whose declared value falls below the heaviest crate, and duty is charged on the *declaration*, not the true total. The dominant declare is almost always **exactly the value of my heaviest crate** — the minimum legal number that avoids the flag. Every round I did this, it held up: no flag, minimal duty. When tempted to declare the true total or something "modest," remember hiding saves at most a few points of duty while the flag costs -40 plus duty at 0.30 × the *true* total — a catastrophic swing. Never declare below the heaviest crate, not even slightly.

Route choice is pure arithmetic and I should run it every single time, no intuition:
- main costs 0.30 × declared.
- night costs 0.15 × declared + my smallest crate (lost to confiscation).

So: **night iff (smallest crate) < 0.15 × declared; otherwise main.** Critical correction from this episode: **at the route stage I always know my own three crate values** — the hold is private to me, not hidden from me. Twice I wrote "no crate details given" and defaulted to main on a hunch; in round 5 (hold 5/38/38, declared 38) the break-even was 5.7 and my smallest was 5, so night was marginally correct and I leaked points by playing main out of laziness. Never say "I don't know my smallest" — I drew those crates; read them off the hold. Compute the comparison exactly, and at close boundaries (smallest within a point or so of 0.15 × declared) prefer the arithmetically better line — there is no hidden uncertainty here at all, since the confiscation hits the smallest crate, whose value I know.

With the declaration pinned to my heaviest crate, night is right mainly for lopsided holds (smallest well under ~15% of heaviest, or a heavy mid-crate with a tiny one — e.g. 5/38/38 type shapes). Flat holds go main. But don't pattern-match "this looks flat"; run the numbers.

Read the other seats' declarations for information, not imitation. Opponents mostly cluster near their heaviest crate too, which tells me the field is playing the same safe line — no exploitable tells emerged, and no reason to deviate from the safe line myself. A seat that flags (-40 swing) loses a round; that's the only large swing in the game besides my own flag risk, which the declare rule eliminates.

Endgame: the flag-avoidance rule holds even with a lead — a -40 can flip a close scoreboard. If I'm narrowly ahead on the last rounds, prefer main for certainty even if night is arithmetically a point or two better. If I'm narrowly behind, take the arithmetically optimal line exactly; the game is tight enough that sub-point route errors accumulate — I finished +299 in second-ish position in a field where every seat was within ~40, so those small leaks matter.

One-round summary:
1. Declare = max crate value. Deviate only in true desperation, and almost never even then.
2. Route: night iff smallest crate < 0.15 × declared; else main. My smallest crate is always known to me at route time — read it off my hold and compute; don't guess or default.
3. Track opponents' declarations for patterns, but the safe line stays optimal until someone proves otherwise.
4. Never reason about the route from the size of the declaration alone — the formula is the whole story.
5. Close boundary cases (smallest ≈ 0.15 × declared): take whichever the arithmetic says, unless protecting a narrow late-round lead, in which case take main.