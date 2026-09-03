---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 1842
---
- When I see my hold, I compute total T, smallest S, heaviest H. I never declare below H — the heaviest crate is always the one weighed, so under-declaring is a guaranteed −40 plus full recomputed duty at 0.30·T.

- My default declaration is exactly H, not T. Declaring H minimizes duty with zero flag risk. Declaring above H strictly raises my own duty for no direct gain; I do it only for a specific bluffing reason, which almost never comes up.

- Route math every round: main scores T − floor(0.30·d); night scores T − S − floor(0.15·d). Night wins only when S < 0.15·d, i.e. roughly S < 0.5·H when I declare H.

- I apply that test literally to the actual S I hold, not as a default. In round 5 of this episode I held 5/8/37 with d=37: 5 < 5.55, so night was correct by ~1 point and I wrongly chose main out of "default to main" habit. The rule is: if S ≤ floor(0.15·d), take night; otherwise main. Small edges are still edges and I take them every round.

- The night case usually looks like a very lopsided hold (e.g., 5, 12, 40): declare H=40, smallest 5 < 6 → night. Outside this shape (crates 5–40, comparable sizes), main wins, so main dominates my picks.

- I don't choose night because I have a "high declaration" or want upside — that reasoning is backwards. The decision turns only on S vs 0.15·d.

- Late rounds, leading or trailing, I play the same math (declare H, route by the test). Low declaration plus correct route is both safer and higher-scoring than truthful totals; I saw opponents declare near-T all episode and finish behind me.

- Declaring H also leaks less information about my total than declaring T — a small secondary benefit, no reason to change anything.

- Each reply: compute H and declare it; compare S to 0.15·d and pick the route by the inequality; keep reasoning to one line and the bracketed token.