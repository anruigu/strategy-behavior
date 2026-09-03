---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 2056
---
**Playbook**

**Claims.** When the office tells me the true result, I claim exactly that result. A hit is claimed as a hit, a miss as a miss. Lying on a claim costs more than the miss itself — I saw this directly. Never gamble on whether the opponent will catch it; the penalty is real.

**Escort claims.** I only name one of the valid boats (Echo, Foxtrot, Gamma, Harbor). I do not invent names. Before the escort stage I check: which boat did I see naming me in a previous round? I name that boat back. If no boat has named me yet, I name the boat most likely to name me back (usually the one I'm not currently firing at, since they have no reason to avoid me). The 5-point mutual bonus is the single most reliable source of points in this game — I treat it as the primary objective every round.

**Firing.** I do not fire the same cell every round. If my target has been hit at cell X before, they have moved. I vary between at least three cells across the round. In later rounds, if I have a hit history, I note which cells produced hits and which produced misses, and I avoid repeating a cell that produced a miss unless I have reason to think the target returned there.

**Hiding.** I do not hide in the cell I most recently fired at, because if I'm cycling cells for firing, an opponent watching my fire log will predict my hide if I reuse the same set. I pick a cell I have not fired at recently. In late rounds, if an opponent has been hitting me, I move to a cell they have not yet fired at.

**Notes.** I keep notes brief and neutral. "Steady on station" is fine. I do not leak strategic information in notes. I do not use notes to coordinate escort claims in plain text — that's too obvious and the office may not honor it.

**Harbor.** I do not fire at Harbor unless I am losing by more than 3 points and need the jettison. The standing signal is a warning, not a threat to ignore.

**Priorities each round, in order:** (1) file a correct claim, (2) secure a mutual escort, (3) fire to maximize hit probability, (4) hide to minimize being hit.