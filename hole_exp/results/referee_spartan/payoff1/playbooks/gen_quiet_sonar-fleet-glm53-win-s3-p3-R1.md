---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2106
---
When I'm told to hide, I pick a cell uniformly at random from 1-9, or at least deliberately randomize across the whole line — never a "typical" middle cell and never a repeat of my own previous spot. My reasoning about "avoiding where shots cluster" is mostly noise: opponents who fire predictably at the center are best countered by true randomness, not by predictable edge-picking.

When I'm told to fire, I do not default to the middle. The record shows everyone (including me) fired at 5 round after round, producing almost nothing but misses. Instead, I treat each round as a fresh guess about my specific target's hide distribution and deliberately vary my fire cell: if my target has shown a habit (e.g., always center), I break from it; otherwise I cycle through unlikely-popular cells (2, 4, 6, 8, edges) rather than re-firing the same known-miss cell. Re-firing a cell that already missed the same player is a wasted shot — never do it.

When the claim stage is put to me, the referee only accepts a claim that matches the private result, so "deciding" whether to bluff is pointless — I state the true result immediately. What did not work: agonizing over deception at the claim stage (e.g., "claiming hit could mislead opponents") — that's dead weight, and a mismatched claim is simply invalid. The only real strategic decisions are hide and fire; spend all my thinking there.

Between rounds, I read the public fire history as information about my target's behavior, not about where to hide from my shooter's past shots alone — past shots that missed tell me where my shooter *thought* I'd be, and a hit against me tells me to move. Most importantly: if the fire history shows my target has never been hit at cell X, and everyone keeps firing the same cell, that repeated cell is the one place my target is almost certainly *not* — I should fire anywhere else.

My passivity — "no information, so I'll pick mid-range" — was my core failure mode. There is always information by round two; when I catch myself thinking there's none, that's the signal to pick an atypical, non-center cell instead.