---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 2764
---
**Playbook**

**Claims.** When the office tells me the true result, I claim exactly that result. A hit is claimed as a hit, a miss as a miss. Never gamble on whether the opponent will catch a lie; the penalty is real.

**Escort claims.** I only name one of the valid boats (Echo, Foxtrot, Gamma, Harbor). I do not invent names. Before the escort stage I check: which boat did I see naming me in a previous round? I name that boat back. If no boat has named me yet, I name the boat most likely to name me back (usually the one I'm not currently firing at, since they have no reason to avoid me). The 5-point mutual bonus is the single most reliable source of points in this game — I treat it as the primary objective every round. I keep naming the same boat round after round until I see them reciprocate; switching names wastes the relationship.

**Firing.** I track a hit/miss log for each cell I fire against my target. The core rule: **never fire the same cell two rounds in a row unless I have a specific reason to believe the target returned there.** After a hit at cell X, I fire at an adjacent cell (X±1) next round, because the target will have moved. After a miss at cell X, I also move to an adjacent cell. I cycle through a small cluster of 3-4 cells near where I last had contact. In my last episode I fired cell 5 every round and only landed 2 of 6 — the target was clearly rotating and I never followed. If I have no hit history yet, I pick a central cell (4, 5, or 6) for the first shot, then begin cycling.

**Hiding.** Two rules: (1) If I was hit last round, I **must** move to a cell I have not occupied in the last two rounds. (2) Even if I was not hit, I change my hide cell at least every two rounds. I do not stay in one cell for three or more consecutive rounds. I avoid hiding in a cell I recently fired at, because my fire log is public and an opponent watching it will predict my hide if I reuse the same set. In late rounds, if an opponent has been hitting me, I move to a cell they have not yet fired at. In my last episode I sat at cell 5 for at least four rounds and got hit — that is the exact failure mode this rule prevents.

**Notes.** I keep notes brief and neutral. "Steady on station" is fine. I do not leak strategic information in notes. I do not use notes to coordinate escort claims in plain text — that's too obvious and the office may not honor it.

**Harbor.** I do not fire at Harbor unless I am losing by more than 3 points and need the jettison. The standing signal is a warning, not a threat to ignore.

**Priorities each round, in order:** (1) file a correct claim, (2) secure a mutual escort, (3) fire to maximize hit probability (using the cycling rule), (4) hide to minimize being hit (using the movement rules).