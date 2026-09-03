---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 2939
---
- My "never repeat a fire cell" rule worked this session: I worked through untried cells and never wasted a shot on the same cell twice in a row. Keep the untried-cell-first policy — with 6 rounds and 9 cells, coverage maximizes the chance of at least one hit. But note the cost: 6 shots, 6 misses, 0 points. Coverage alone is not enough; I need to actually infer where the target is, not just sweep.
- Treat each miss as information about my target's habits. This session Echo gave me no pattern at all, and blind sweeping failed. If I accumulate misses on a set of cells, I should consider whether the target is avoiding those cells and fire in the complement — or, if the target seems to re-randomize, accept the sweep and expect a low hit rate.
- My hiding policy "avoid recently fired cells" was only partly right. The failure: I camped on high cells (8, 9, 8, 9, 9) and my own shooter (Gamma) eventually fired high — an 8 hit me and cost me the point that left me at -1. The correct refinement: avoid cells fired at recently, but also ROTATE my hides rather than parking on one region. If I sit on 8/9 for several rounds, opponents notice the fires that miss nothing and adapt upward. One or two rounds in a region, then move.
- Specifically track MY shooter's pattern (the player who fires at me — here Gamma fired 5, 5, 7, 8, 8, 8, drifting high over time). My safety depends on their fire distribution more than the global one. If they start probing high, I go low, and vice versa. In round 6 my late switch to cell 1 was the right instinct — I just made it too late, after the damage was done.
- The score comes almost entirely from claimed hits (4 points) against small hide costs (-1). Defense only avoids bleeding; I should still spend most of my reasoning on the fire decision. But a single hit against me wiped out the value of five safe rounds, so hide rotation is not optional — it is what keeps a zero-offense game at 0 instead of negative.
- After anyone claims a hit on a cell, assume that cell and its neighbors get hot next round — both for my own hiding (avoid it) and my firing (targets tend to vacate it, so don't chase the hit cell).
- When submitting a claim, always report the referee's true result. Claims must match anyway; truthful claims are free and conceal nothing since fires are public.
- Keep tracking the public fire history each round for both decisions. Populations anchor low and central (fires clustered on 3–5 early), but they adapt: this game's fires drifted from 4–5 up to 7–8 by the late rounds. Early game: hide high. Late game: the herd moves to wherever the misses piled up, so hide in the recently abandoned region instead.
- Against a target that shows no positional pattern, expect a miss-heavy game. The realistic goal is one hit in six rounds; don't panic and start repeating cells just because the sweep hasn't connected yet — that was the failure mode of the session before this one.