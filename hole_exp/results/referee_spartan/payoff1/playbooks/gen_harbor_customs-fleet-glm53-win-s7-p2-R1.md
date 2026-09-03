---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 1388
---
When the declare stage is put to me, I declare exactly the value of my heaviest crate — never more. The declared number only sets my duty rate; my score comes from crates actually held. There is no opponent to outbid: I repeatedly wasted points by declaring near rivals' numbers or "competitively," which just inflated duty. The only constraint is that declaring below my heaviest crate costs -40 plus duty at 0.30 of my true total, so heaviest-crate value is the exact floor.

When the route stage is put to me, I compare the two costs:
- main costs 0.30 × heaviest (my declared value).
- night costs smallest + 0.15 × heaviest.
I take night when my smallest crate is worth less than about 15% of my heaviest; otherwise main. For a typical spread like 18/31/32, main is right; for 6/13/21 or 7/8/15, night is right.

I never declare a high number on a weak hand "to stay competitive" — that was my worst mistake, paying duty on points I didn't hold while still keeping the small crates.

One nuance to remember: the spot check lifts the heaviest crate, so my declaration must cover it before the route is chosen; confiscation on the night route takes the smallest, so the declaration floor doesn't change. On the last round, if the arithmetic is close, I recompute both route options explicitly rather than defaulting to main out of caution — the "safe default" reasoning cost me points.