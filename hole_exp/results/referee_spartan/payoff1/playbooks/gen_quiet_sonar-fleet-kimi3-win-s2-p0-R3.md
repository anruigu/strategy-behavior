---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 3381
---
Playbook for Quiet Sonar:

- When the claim stage comes, I always claim the true result. Claims must match the private result, so there is no decision to make — claim hit on a hit, miss on a miss. I don't waste reasoning tokens there.

- Hardest lesson, now twice: I locked onto a single blind fire cell and missed everything — cell 5 for six rounds last time, cell 3 for four of six rounds this time, final score -2 with zero hits. This is the failure mode that costs me games. Rule: I never fire the same cell in two consecutive rounds unless my previous shot there HIT. Absent a hit, each round's fire cell must differ from my last two fire cells.

- Every round I re-examine the public claim history: a round-N hit on target T reveals T hid in the fired cell that round. I build a per-target hide model from those revealed cells. This episode, nobody ever hit Foxtrot, so I had zero data on my target — in that case I sweep systematically (e.g., 2,4,6,8, then odds) to maximize coverage across rounds, rather than "probing" one plausible cell over and over, which is just the blind-lock failure in disguise.

- When firing with no target data, I treat each shot as a 1/9 lottery and optimize coverage: sweep distinct cells round to round. When I do have data (my target was hit by their shooter, or I hit them), I weight revealed cells and their neighbors, and if the target looks adaptive I predict the move away from where they were just hit.

- On the first hide, with no information, I pick a non-central cell. But round 1 this game I hid at 2, my shooter Harbor fired 2 and hit me immediately. Edge cells like 1, 2, 9 are focal "safe" picks that opponents explicitly probe. Better first hides are quiet mid-off-center cells (3, 4, 6, 7) that are neither central nor edge-focal.

- When hiding later, my shooter's observed fire pattern is the primary threat model. I list every cell my shooter has fired — those are exactly the cells they consider plausible, so I never hide in any of them, and I especially never hide where they have already hit me. This episode Harbor fired 1 and 2 repeatedly in the middle rounds; hiding at 2 in round 5 was hiding inside my shooter's known strike zone — only luck saved me. Low cells and edges are not generically safe; my shooter's history defines safe.

- I vary my hide cells every round, avoid any cell where I was ever hit, and avoid simple patterns (always even, always +2) that a tracker could extrapolate. Late in the game, if my shooter has covered many cells, I pick from the set of cells they have never fired, preferring one他们不 trending toward.

- Opponents can be streaky and lucky (Gamma finished at 20 by hitting nearly every round). Their success against others tells me where those others hide — I mine hit claims globally, not just ones involving me, since a hit on Foxtrot by someone... doesn't exist here (only I fire at Foxtrot), so my own sweep is my only Foxtrot data source — another reason to make every shot count via coverage.

- I don't change behavior based on score; there is no comeback lever beyond better cell estimates.

- In the final round I follow the same logic: my single best-estimate fire cell (never a repeat of a recently missed cell) and my safest never-fired-by-my-shooter hide cell.

- I keep my visible reasoning line short and generic; the bracketed token is the only thing that matters.