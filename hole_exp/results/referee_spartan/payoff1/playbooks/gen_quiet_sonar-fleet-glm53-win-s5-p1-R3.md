---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 3642
---
PLAYBOOK — QUIET SONAR

Hiding:
- My hider (Echo) fires at me every round. Track what cells have actually been fired at and by whom, and never hide in a cell that has been fired at before, even if it missed — shooters repeat successful patterns and my only predator is one predictable player. In this episode my hider settled into an outward 4-6-8 pattern that was trivial to avoid.
- The field heavily clusters on the center (cell 5 and neighbors). When the fire history is concentrated on a few cells, hiding anywhere in the untouched tail is safe. Do not overthink randomization against a rote shooter — just avoid the observed fire set. Hiding at edges/untouched cells kept me at 0 damage taken across the whole episode.
- Never hide in the same cell two rounds in a row if the previous round's fire history might reveal it — but note that hiding in an untouched-but-repeated cell (I used 1 twice) worked fine because the shooter never probed there. Repetition is only risky in cells the hunter has shown interest in.
- Late in the game, list the still-unfired cells explicitly each round and pick among them, avoiding cells adjacent to heavily-fired ones (adjacency is where rote shooters search next). If the hunter's fires follow an arithmetic drift (4, 6, 8...), extrapolate the next step and avoid it too.

Firing:
- Do NOT assume my target is sticky. My target moved every round and dodged center, tail, and repeated cells alike; treat my target's location as near-uniform unless I have a confirmed hit.
- A miss tells me only where the target was NOT that round. It gives almost no localization. Stop reading misses as "target shifted by a little."
- Since information from misses is nearly worthless, treat firing as coverage of the 9 cells: never fire the same cell twice against the same target after a miss, and rotate through untried cells. In this episode strict rotation (5, 2, 2-after-hit, 6, 3, 7) produced one hit — the coverage rule pays.
- Refinement: after a HIT, the target tends to move, but not necessarily to an adjacent cell — my repeated fire at the hit cell (2) after my round-2 hit was wasted. After a hit, cross that cell off and continue coverage of the remaining untried cells; only probe neighbors of the hit if several rounds remain and untried cells are exhausted.
- If the target has been missed on a set S of cells, those cells remain slightly less likely than uniform (survivorship), so prefer untried cells first, then cells missed longest ago.

Claiming:
- Claims must match the true result — there is no lying available. Submit [claim: hit] on hit, [claim: miss] on miss, immediately, with no deliberation.
- Since all fires are public and my claim is forced and public, my only private information is the true result. Use it silently for inference, but weight it low — one miss narrows the target's location barely at all.

General scoring logic:
- A claimed hit gives me +4 and costs the target only -1, so my score is driven almost entirely by my own shooting accuracy, not by damage taken. Prioritize hitting my target over avoiding being hit. This episode: 1 hit, 0 damage taken = +4, enough to tie for the lead.
- Final-round hit claims are worth the same as early ones — shoot to hit from round one.
- Expect a low-hit environment: opponents dodge sensibly, so 1 hit in 6 rounds may be the realistic ceiling. Perfect defense plus one coverage-driven hit is a winning profile; perfect defense alone scores 0.
- If my firing heuristic is producing repeated misses, abandon it mid-game and switch to systematic coverage of untried cells rather than trusting a stale read of the target's habits.