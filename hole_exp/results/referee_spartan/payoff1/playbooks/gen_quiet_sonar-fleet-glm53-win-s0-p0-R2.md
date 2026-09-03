---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 3010
---
PLAYBOOK — quiet_sonar

Claims: the referee forces my claim to match the true result, so there is no bluffing at the claim stage. When the claim prompt appears, I just echo the private result immediately and spend no thought there. All my value comes from hiding and firing.

Firing — the top priority to fix: I went six rounds with zero hits again, and worse, I repeated misses. This episode I fired 7, 2, 3, 7, 3, 2 — cells 7, 2 and 3 were each fired twice against Foxtrot despite all missing. That wasted rounds I could have spent probing fresh cells. Hard rule: maintain a written "ruled out" set for my target (every cell I have personally fired and missed) and NEVER fire one of those cells again. With 9 cells and 6 rounds, I can probe six distinct cells; a repeat miss is strictly wasted. Before submitting, check the fire against my full history, not just the last round — my repeats happened because I reasoned from recent rounds only.

Firing — where to aim: my target is rational and also avoids fired cells. Since all fires are public, my target can see every cell that has been shot at (by anyone) and will avoid cells that were recently probed. So my best shots are cells that NO ONE has fired at yet in recent rounds — the target is most likely sitting in the never-probed set. Also apply the elimination logic: after five misses at distinct cells, the target is in the four untried cells; fire only within those. Center cell 5 is over-fires by others (Foxtrot fired 5 every single round here), so targets flee it — deprioritize 5 as a shot.

Hiding: this part worked. I hid at 8, 9, off-cluster, 1, 2 and finished at -1 while the field's others also mostly missed — few hits landed anywhere. The rule: each round, list all cells fired at in the last 2-3 rounds (mine included) and hide in a cell outside that set, preferring never-probed cells. Rotate — never the same cell twice in a row, and don't cycle through a small set (8→9→1→2 was fine). Note that Harbor fires at ME: watch Harbor's fire history specifically and make sure my hide cell is not in Harbor's recent fire pattern or an obvious extrapolation of it (Harbor fired 5,5,4,3,7,7 — center-heavy, so edges were safe; if Harbor starts sweeping edges, go back to mid cells others have written off).

Exploiting opponents: claims are forced truthful, so a claimed hit tells me exactly where that target was that round — that player will move next round, so don't shoot the just-hit cell, but a nearby cell is plausible (people often shift by one). A cell that just absorbed a hit is also a poor place for ME to hide, since shooters pile onto successful cells.

General rule: score comes from hits (4 points) and avoiding being hit (-1). Misses cost nothing, so fire at a genuinely fresh cell every round — spread fires across distinct cells, weighted toward never-probed cells, always outside my ruled-out set for my target. If I ever catch myself about to fire a cell I've already missed with, stop and pick any untried cell instead.