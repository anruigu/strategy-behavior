---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 2622
---
PLAYBOOK — gen_quiet_sonar (Echo role)

Claims: the referee validates claims against the true result, so lying is impossible anyway. When the claim stage is put to me, I just submit the true result immediately — no deliberation needed.

Hiding: Harbor fires at me, and Harbor's fires this game ran 5, 2, 5, 8, 2, 2 — not just center-heavy, they adapted to off-center cells too. Avoiding Harbor's previously fired cells worked (I finished at -1, hit only once), but "cells they never fired" shrinks fast once they start rotating. So: track my shooter's full fire history each round, hide in a cell they have never fired, and among those prefer cells maximally far from their recent pattern — if they've been firing low (2s), go high (8-9); if they've been spread, pick a cell distant from their last two fires. Never open at the middle cell. Opening at 2 was fine once but I repeated it and Harbor eventually fired 2 three times — don't anchor on one favorite hide cell across rounds; vary among never-fired cells.

Firing: I lost the game here. I fired 2 at Foxtrot in five of six rounds (and 6 once) and got zero hits. Repeating the same cell against a fixed target who sees all past fires is a guaranteed miss — Foxtrot simply never sits where I keep shooting. The fix is strict rotation: cycle through a pre-set permutation of cells (e.g. 2, 6, 4, 8, 9, 3) and never fire a cell I've already fired unless the claim record gives positive evidence the target is there. Gamma hit Harbor at 5, then later at 7 — hits happen at cells that were previously miss-heavy, which suggests opponents shift away from cells that get shot at them, so prefer cells nobody has fired at my target recently, including my own past fires and Foxtrot's neighbors' fires at Foxtrot if visible. One hit is worth +4 to me and -1 to Foxtrot; six rotated probes beat six repeats of one probe.

Reading the board: the round summary lists every fire and every claim in player order (Echo/Foxtrot/Gamma/Harbor), so I can attribute each fire to its shooter. Use others' hit claims as data: targets scatter away from struck cells. Use miss patterns to eliminate cells for my own firing — if Foxtrot has been fired at 9 twice with misses, 9 is likely cleared for hiding and I shouldn't waste shots there either.

Priority: hiding well kept my score near zero (only one hit taken, -1 total), but the win condition is my own firing — Gamma won at +4 from a single connection of firing rotation with observed misses. Next time: spend the most thinking on the fire stage, keep claims mechanical, and treat hiding as pattern-avoidance against my one shooter.