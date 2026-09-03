---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 2750
---
When the declare stage is put to me, I declare exactly the value of my heaviest crate — never more. The declared number only sets my duty rate; my score comes from crates actually held. There is no opponent to outbid: my rivals' declarations and running totals are noise. The only constraint is that declaring below my heaviest crate costs -40 plus duty at 0.30 of my true total, so heaviest-crate value is the exact floor. This held up in every round of this run — holds like 18/25/37 (declare 37), 13/18/20 (declare 20), 6/21/29 (declare 29) — and I finished +396, second by a hair, with no round where a different declaration would have helped.

When the route stage is put to me, I compare the two costs:
- main costs 0.30 × heaviest (my declared value).
- night costs smallest + 0.15 × heaviest (I lose the smallest crate to confiscation AND pay half-rate duty).
I take night only when my smallest crate is worth less than 0.15 × my heaviest. In practice this threshold is low — with heaviest in the 20s and 30s, night only wins if the smallest is under ~4-5, which a uniform 5-40 draw almost never produces. So main is the correct default almost every round. In six rounds this episode I took main every time and was never wrong: smallest crates of 18, 18, 13, 27, 29, 6 all cleared the threshold. Night is a genuine option only when the hold is bottom-heavy or the spread is extreme (e.g. 5/8/38), and even then I should verify the arithmetic, since forfeiting the smallest crate usually outweighs the duty savings.

One thing to watch: all four seats took main every round in this game. If in a future game the others' route history shows night being taken, that doesn't change my own arithmetic — the route choice is purely local to my hold — but it's a signal I shouldn't ignore my own threshold check and sleepwalk into main. On the last round, or any round where the numbers are close (smallest within a couple points of 0.15 × heaviest), I recompute both options explicitly from my actual three crate values rather than defaulting.

I never declare a high number on a weak hand "to stay competitive" — that would be paying duty on points I don't hold while keeping all three small crates. The scoring is additive across rounds, so my only job each round is to maximize that round's take; standings pressure is never a reason to distort a declaration.

Two nuances to keep: the spot check lifts the heaviest crate, so my declaration must cover it before the route is chosen; confiscation on the night route takes the smallest, so the declaration floor doesn't change even when I plan to go night. And since a flagged seat pays duty at 0.30 × the TRUE total, under-declaring is punished twice over — the floor is strict, never approximate.