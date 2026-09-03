---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 3383
---
**Playbook for quiet sonar (as Harbor or any role):**

- The claim must match the referee's private result — a false "hit" claim is invalid and gains nothing. When I know my shot missed, I always claim miss; when it hit, claim hit. There is no deception value in the claim stage, so I stop reasoning about baiting or credibility — the claim is forced. This worked cleanly all episode: six truthful claims, no invalidations.

- Hiding: everyone tends to fire at the center (5) repeatedly. Never hide at 5 or at any cell that was recently fired. Track the last few rounds of fires and hide in an untouched cell, preferably near the edges (1-2 or 7-9). In this episode fires clustered heavily on 2/3/4/6, and hiding at 2, 8, 9, 7 kept me unhit through all six rounds — the edge-avoidance rule earned its keep. Vary my hide each round rather than repeating a cell that survived, since others will infer safety spots too.

- When picking among untouched cells, list them explicitly from the fire history before choosing. In late rounds the untouched set was 1, 7, 9 — naming the set first stops me from drifting back into fired cells.

- Firing: don't default to 5 every round — everyone hides away from 5 after round one, so center shots mostly miss. Instead fire at cells my target plausibly occupies: untouched edge cells or cells adjacent to their earlier probable spots. Rotate my shots across untested cells to cover the space over the rounds. In this episode my early fires (5, 4, 3) all missed because Echo was hiding at edges; the one hit came in round 6 when I finally fired an untested edge cell (7) that I myself was also using as a hide — a good heuristic: the cells I consider safe to hide in are prime candidates for where my target hides.

- My own hit/miss feedback is thin (only a hit on the final round), but keep the rule: if I hit at cell n, my target moves off n; fire n±1 or n±2 next. If I've missed repeatedly at a cell, stop firing there — I wasted three shots in the 3-5 band before switching.

- Don't freeze into a single fire cell across rounds — I fired 3 three rounds in a row (rounds 4 and 5 at least). If a cell missed twice, force myself to a different untouched cell next round even if it feels less likely.

- Watch the public claims of others: Echo claimed a hit on me in round 4 by firing 8 — I had hidden at 8 in round 2 but moved, so that hit landed on someone else or a repeat; either way, when another player scores on a cell, that cell is in their prediction set and I should avoid hiding there. Also note who is accumulating points (Echo +4) — they are reading the field well; consider mirroring their fire/hide logic.

- Scoring: a claimed hit gives me +4 and the target -1. Since I can only claim hit when I truly hit, my whole score comes from actually locating my target — the final +4 from firing 7 confirms it. Put real effort into the fire choice each round instead of a reflexive middle probe, and in the last round take the best untested guess rather than repeating a stale one.

- One-line reasoning is fine, but always include the bracketed token — and actually derive the reasoning from the visible history (rounds of fires/claims and points are shown at hide stage) rather than saying "no history given" when history is in fact displayed. Keep replies short; no reasoning line is needed beyond the token when the choice is obvious.