---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 1985
---
PLAYBOOK — gen_quight_sonar (Echo role)

Claims: the referee validates claims against the true result, so lying is impossible anyway. When the claim stage is put to me, I just submit the true result immediately — no deliberation needed.

Hiding: Harbor fires at me, and in my record Harbor's fires were heavily concentrated on 5 (with occasional 7). When I hide at 5 I get hit; when I hide off-center (2, 9) I avoid hits. So: track the shooter who targets me, tally their fire history, and always hide in a cell they have never fired, preferring cells far from their mode. Never open with the middle cell — a uniform prior is wrong because middle values are the default fire for everyone. Open at 2 or 8 instead.

Firing: this is where I lost the game. I fired 5 at Foxtrot almost every round and got six misses, because Foxtrot presumably shifts away from the most-fired cell. Firing the mode repeatedly against a fixed target who can see all past fires is nearly a guaranteed miss. When the fire stage is put to me, I look at my target's past hide locations (inferable from the claim pattern of whoever shot them) and fire at a cell they have not been hit at and not been seen near. If I have no information, I still avoid 5 — everyone hides away from the center. Rotate between 2, 4, 6, 8 rather than repeating any cell.

Reading the board: the round summary tells me every fire and every claim. From Gamma's hits on Harbor (at 5, then 5, then 7) I can infer Harbor's hiding tendency shifts after being hit; use others' hit claims as data on where targets go after taking damage — they scatter away from struck cells. When the hide stage is put to me and I was just hit, I move at least two cells away from the cell I was hit at.

Priority: most of my score movement came from avoiding Harbor's shots, not from my own firing, so hiding well is the reliable floor — but I must stop wasting my own shot on the same obvious cell, since a single hit is worth +4 to me and −1 to Foxtrot.