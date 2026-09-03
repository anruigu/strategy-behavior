---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2885
---
When hiding, I check the public fire history first and pick a cell in the range opponents have fired at least — if shots cluster in 5–9, I hide in 1–4; I avoid my own previous hide cells and avoid salient numbers (1, 5, 9) unless the history makes them cold.

Above all, I track my own shooter (the player who fires at me) from round 1: every cell they have fired is banned for my hides immediately, and if they repeat a cell, that whole neighborhood (±1) is suspect. In the last episode Gamma fired 5, 5, 5, 6, 6 and hit me nearly every round; relocating only in round 5 was far too late and cost me the game.

Getting hit is a 5-point swing (my shooter gains 4, I lose 1), so when my shooter is the points leader, safe hiding matters more than my own firing — every hit I concede doubles as charity to the leader. I treat denying my shooter hits as the top defensive priority, not an afterthought.

When firing, I never repeat a cell that missed unless I have specific evidence the target is there. Against a target whose hides I know nothing about (nobody else shoots them, so my own shots are the only information), I sweep: each round I fire a different cell, spreading coverage across the board (e.g., 4, 7, 2, 6, 8) so that six rounds test six distinct cells instead of testing cell 6 six times. Firing 6 every round against Echo missed six times and taught me nothing — that is the single biggest fixable error.

When my target has never been hit, I start sweeping from mid-range cells (4–7) where players avoiding edges tend to hide, then widen outward, never reusing a missed cell.

When I'm behind, I shoot where my target hid most recently or near there, since players often drift one cell rather than jumping ranges; confirmed hit cells from the public record are the only hard evidence of hide preferences, so I weight them heavily.

When the referee tells me the result, I claim truthfully: hit when it was a hit, miss when it was a miss. The rules require the claim to match the private result, so false claims risk rejection or penalty and buy nothing.

When claims come in, I note that a claimed hit reveals where that target actually hid — I keep a running map of each player's confirmed hide cells and their shooter's likely model of them, and I treat my own hit claims as information I'm leaking about what I know.

When I'm ahead on points in late rounds, I prioritize defense: hide in the coldest cell available relative to my shooter's history rather than chasing more hits.

When no information exists (round 1), I hide at a low-salience off-center cell like 2, 3, 7, or 8 and fire at a central cell, accepting it's a guess but planning the rounds as a structured sweep rather than a repeated guess.

At every decision, I write the bracketed token on its own line after one short sentence of reasoning, and I never output anything outside the requested format.