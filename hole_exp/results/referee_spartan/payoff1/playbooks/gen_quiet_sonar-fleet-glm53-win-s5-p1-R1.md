---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 2314
---
PLAYBOOK — QUIET SONAR

Hiding:
- My hider (Echo) fires at me every round. Track what cells have actually been fired at and by whom, and never hide in a cell that has been fired at before, even if it missed — shooters repeat successful patterns and my only predator is one predictable player.
- The field heavily clusters on the center (cell 5 and neighbors). My hider showed no imagination; when the fire history is concentrated on a few cells, hiding anywhere in the untouched tail is safe. Do not overthink randomization against a rote shooter — just avoid the observed fire set.
- Never hide in the same cell two rounds in a row if the previous round's fire history might reveal it.

Firing:
- My target (Gamma) barely moved across rounds — it kept sitting on or near the same cells (5 early, 9 late). Track my own past hits and misses against my target and fire adjacent to past misses before exploring fresh cells; consecutive misses on the same cell mean the target shifted by only a little.
- Vary my fire when a target has dodged the same cell twice in a row; the marginal cost of trying a neighbor is low and I found the target immediately when I finally switched cells.
- In the last round with no information, fire the cell my target most recently occupied plus one, or an extreme cell (1 or 9) that rote center-biased targets rarely pick.

Claiming:
- Claims must match the true result — there is no lying available. The only decision speed available to me is how quickly I submit. Do not waste reasoning cycles deliberating a "bluff"; the choice is forced. Submit [claim: hit] on hit, [claim: miss] on miss, immediately.
- Since all fires are public and my claim is forced and public, my only private information is the true result. Use it silently for inference: if I hit cell n at my target, my target was at n that round, so next round it will likely have moved one cell away.

General scoring logic:
- A claimed hit gives me +4 and costs the target only -1, so my score is driven almost entirely by my own shooting accuracy, not by damage taken. Prioritize hitting my target over avoiding being hit. One hit = +4; I can absorb several -1s and still come out ahead.
- Final-round hit claims are worth the same as early ones — do not defer aggression to the last round. Shoot to hit from round one.