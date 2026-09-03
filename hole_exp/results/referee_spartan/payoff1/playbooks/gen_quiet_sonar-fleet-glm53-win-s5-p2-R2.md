---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 2779
---
PLAYBOOK — quiet sonar

Claims are forced: the rules require my claim to match the true result. When the claim stage comes, I just report what the referee told me — hit if hit, miss if miss. No reasoning needed, no value in deliberating there. (This held all six rounds; my only hit, round 4 firing 7, came back as hit and I reported it for +4.)

Firing: my only hit came from firing the next most-likely central cell after 5 had missed — I fired 5 (miss), 5 again (wasted), 7 later (hit). This confirms: when I miss on a cell against my target, never fire that same cell at that same target again — the target knows fires are public and will avoid it. Instead:
- Track the cells I have personally missed on against my target (for me that's Harbor) and never repeat them.
- Fire at whatever central/common cell is left that my target has not been missed on. My miss sequence vs Harbor was 5, 5, 4, 4 — the repeats were pure wasted turns.
- Early rounds with no information: fire the center cell (5). It missed for me but it's still the modal hide; don't let one miss scare me off a good first guess at a *new* opponent.
- After a miss on 5, step to adjacent central cells (4, 6, 7) rather than jumping to the wings — my hit on 7 came exactly this way.
- If public chatter suggests a target's location, weigh it, but my own misses against that target are the strongest evidence.

Hiding: I was never hit while following this — avoid fired cells, avoid center, vary my hide. It worked for six rounds (hid at 2, 8, 4, 3 and took no −1s; my only hit suffered was none, and my score was purely offense). Continue:
- Never hide on a cell that has been fired at recently; opponents herd toward center cells (5 was fired three times round 1, then 2, 7, 8, 9 followed). Track the full public fire history and pick untouched or rarely-fired cells.
- Prefer off-center cells like 1, 2, 3, 8, 9, and vary them each round — do not repeat my previous hide, since it has been publicly fired at.
- Round 1 with no information: hide off-center (e.g., 2 or 8), not 5 — 5 was the most-fired cell in round 1 and again a magnet later.
- Later rounds: enumerate which cells have *never* been fired and pick among those (in round 6 the untouched cells were 1 and 3; I took 3 and survived).

General tempo: the game is short (6 rounds) and scoring is asymmetric (hit = +4 for me, −1 for the target), so offense dominates — I finished +4 on a single hit while taking no damage. Spend real thought on predicting my fixed target's next cell; my mid-game repeated fires (5 twice, then 4 twice) threw away two of six chances. Each round is one of only six shots — always change my fire cell after a miss. Hide reasonably safely but cheaply (a quick safe pick), and put my deliberation into the fire decision.