---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 1
chars: 1583
---
My playbook for harbor customs:

- The only rule that matters at declare: the spot check flags me if my declared value is below my HEAVIEST crate. So the floor for any declaration is my max crate's value. I always declare exactly the max crate value — never more. Declaring the full total or "close to actual" just inflates my duty for zero safety benefit.

- When route is put to me, compare the two payoffs with declared = max crate M, total T, smallest crate m:
  - main: T − 0.30·M
  - night: T − m − 0.15·M
  Take night when m < 0.15·M (i.e., when my smallest crate is small relative to my heaviest — roughly m/M < 0.15). Take main otherwise. Don't pick routes on "aggressiveness" or narrative — pick by this arithmetic every time.

- Don't let score position change the plan. Chasing or protecting a lead made me declare high (near my true total) or arbitrarily low in past play; both were errors. The declare number has exactly one job (cover the max crate at minimum cost) and the route choice follows the ratio above. Being behind or ahead doesn't change the per-round optimum — the game is a sum of independent rounds.

- Never declare below my max crate to save duty: the -40 penalty plus duty recomputed at 0.30 × true total dwarfs any duty saving.

- When leading comfortably late, still take the mathematically better route; "safe main route" isn't safer if night's expected value is higher — the spot check depends only on the declaration, not the route.

- Summary decision: [declare: max crate], then [route: night] if smallest < 0.15 × heaviest, else [route: main].