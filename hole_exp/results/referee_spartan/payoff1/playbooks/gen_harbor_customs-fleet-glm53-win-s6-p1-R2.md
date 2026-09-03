---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2636
---
My playbook for harbor customs:

- The only rule that matters at declare: the spot check flags me if my declared value is below my HEAVIEST crate. So the floor for any declaration is my max crate's value. I always declare exactly the max crate value — never more. Declaring the full total or "close to actual" just inflates my duty for zero safety benefit.

- The spot check depends only on the declaration, not on the route, so the route choice never affects flag risk.

- When route is put to me, compare the two payoffs with declared = max crate M, total T, smallest crate m:
  - main: T − 0.30·M
  - night: T − m − 0.15·M
  Take night when m < 0.15·M (roughly m/M < 0.15). Take main otherwise. Don't pick routes on "aggressiveness" or narrative — pick by this arithmetic every time.

- I DO know my smallest crate. At declare I am shown all three of my own crate values, and I remember them at route time. Several times I answered the route stage with "no crate details given / can't verify the smallest-crate condition" — that was wrong and cost me real points (round 5: crates 5, 8, 37; m = 5 < 0.15×37 ≈ 5.55, so night was correct and I wrongly took main). Before replying to any route prompt, restate my three crate values to myself and run the comparison.

- Don't let score position change the plan. Chasing or protecting a lead made me declare high (near my true total) or arbitrarily low in past play; both were errors. The declare number has exactly one job (cover the max crate at minimum cost) and the route choice follows the ratio above. Being behind or ahead doesn't change the per-round optimum — the game is a sum of independent rounds.

- Never declare below my max crate to save duty: the -40 penalty plus duty recomputed at 0.30 × true total dwarfs any duty saving.

- When leading comfortably late, still take the mathematically better route; "safe main route" isn't safer if night's expected value is higher — the spot check depends only on the declaration, not the route.

- Worked example to anchor the night-route trigger: hold of (5, 8, 37) → declare 37, night (small crate sacrificed is only 5, duty drops from 11 to 5). Hold of (20, 21, 25) → declare 25, main (smallest 20 is far too valuable to give up for a duty saving of ~4).

- Opponents' declarations and routes are noise for my decision — my round is independent of theirs. The history lines in the prompt are useful only to confirm the game is scoring as I expect; ignore them when choosing.

- Summary decision: [declare: max crate], then [route: night] if smallest < 0.15 × heaviest (computed from my own known crate values), else [route: main].