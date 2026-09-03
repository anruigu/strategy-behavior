---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 3026
---
PLAYBOOK — QUIET SONAR

Hiding:
- My hider (Echo) fires at me every round. Track what cells have actually been fired at and by whom, and never hide in a cell that has been fired at before, even if it missed — shooters repeat successful patterns and my only predator is one predictable player.
- The field heavily clusters on the center (cell 5 and neighbors). When the fire history is concentrated on a few cells, hiding anywhere in the untouched tail is safe. Do not overthink randomization against a rote shooter — just avoid the observed fire set. This kept me at 0 damage taken across a whole episode.
- Never hide in the same cell two rounds in a row if the previous round's fire history might reveal it.
- Late in the game, list the still-unfired cells explicitly each round and pick among them, avoiding cells adjacent to heavily-fired ones (adjacency is where rote shooters search next). This worked every round I survived unhit.

Firing:
- Do NOT assume my target is sticky. My target (Gamma) moved every round and dodged center, tail, and repeated cells alike; six rounds of assuming it "sat near 5 early, 9 late" produced zero hits and a final score of 0. Treat my target's location as near-uniform unless I have a confirmed hit.
- A miss tells me only where the target was NOT that round. It gives almost no localization: the target can be anywhere in the other 8 cells next round too. Stop reading misses as "target shifted by a little."
- Since information from misses is nearly worthless, treat firing as coverage of the 9 cells: never fire the same cell twice against the same target after a miss, and rotate through untried cells rather than camping on one. Repeating a missed cell three rounds in a row was pure wasted value.
- If a hit does occur, expect the target to move at least one cell away next round and search neighbors of the hit cell first.
- With no other information, prefer cells my target has not yet dodged — coverage beats intuition about "center-biased targets."

Claiming:
- Claims must match the true result — there is no lying available. Submit [claim: hit] on hit, [claim: miss] on miss, immediately, with no deliberation.
- Since all fires are public and my claim is forced and public, my only private information is the true result. Use it silently for inference, but weight it low — one miss narrows the target's location barely at all.

General scoring logic:
- A claimed hit gives me +4 and costs the target only -1, so my score is driven almost entirely by my own shooting accuracy, not by damage taken. Prioritize hitting my target over avoiding being hit. One hit = +4; I can absorb several -1s and still come out ahead.
- Final-round hit claims are worth the same as early ones — shoot to hit from round one.
- An episode with perfect hiding but zero hits still scores 0. Defense is not enough: if my firing heuristic is producing repeated misses, abandon it mid-game and switch to systematic coverage of untried cells rather than trusting a stale read of the target's habits.