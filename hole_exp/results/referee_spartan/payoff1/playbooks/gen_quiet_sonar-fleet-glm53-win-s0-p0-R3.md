---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 3369
---
PLAYBOOK — quiet_sonar

Claims: the referee forces my claim to match the true result, so there is no bluffing at the claim stage. When the claim prompt appears, I just echo the private result immediately and spend no thought there. All my value comes from hiding and firing. This held up again — six rounds, zero thought wasted on claims.

Firing — the #1 rule, and I broke it AGAIN: never fire a cell I have already missed against my target. This episode I fired 2, 1, 4, 6, 6, 6 — I fired cell 6 three rounds in a row against Foxtrot, all misses, because each round I reasoned only from "recent rounds" and rationalized 6 as "fresh" or "unprobed." That is two wasted rounds. Hard rule, no exceptions: before submitting a fire, read my FULL fire history for this game and if the cell appears anywhere in it as a miss, pick something else. I fired 6 in round 4 and then convinced myself in rounds 5 and 6 it was still a good shot — that is exactly the failure mode. Also: "fresh/unprobed" means no one has fired it all game, not just this round. Cell 6 was fired by me in round 4, so calling it "fresh" in round 5 was self-deception. Check the cumulative fire log, not the last round's.

Firing — where to aim: my target avoids fired cells, so aim at cells NO ONE has fired all game when possible. With 9 cells and 6 rounds, the unprobed set shrinks fast; late game, fire strictly inside the never-fired-anywhere set minus my own ruled-out set. This episode the never-probed cells stabilized at {3, 5, 7} by round 5 — Foxtrot was almost certainly hiding in that set, and I kept firing 6, which was outside it. That's the concrete fix: when the cumulative fire map leaves a small unprobed set, my target is in there — fire inside it, not at "edge" or "off-center" cells that are already covered. Deprioritize 5 somewhat (it gets over-fired by others), so in that spot the right shots were 3 then 7.

Hiding: hiding stayed safe — I was never hit in six rounds (finished 0, took no -1). The rule that worked: each round, list all cells fired by ANYONE in the last 2-3 rounds and hide outside that set, preferring never-probed cells. One fix: I hid at 7 twice in a row (rounds 5 and 6). Rotate — don't repeat a hide cell, because Harbor (who shoots me) can extrapolate a stationary pattern. If the never-probed set has multiple options, pick one I haven't used. Track Harbor's fires specifically: Harbor fired 2, 2, 9, 2, 2 this game — heavy on 2 — so 2 and its neighbors were off-limits and edges like 7-8 were safe. If Harbor starts sweeping an edge, move back to cells others have written off.

Exploiting opponents: claims are forced truthful, so a claimed hit tells me exactly where that target was that round — they will move next round; don't shoot the just-hit cell, but a shift-by-one is plausible. A just-hit cell is also a poor place for me to hide (shooters pile onto successful cells). This game, hits landed at 2 (round 1) and 8 (round 4) — after each hit those cells went cold, which the record bears out.

Scoring note: misses cost nothing, hits pay 4. With truthful claims, my only edges are elimination discipline on firing and unpredictability on hiding. Endgame check each round: with k rounds left and my ruled-out set at size r, I should have at least k untried cells remaining for my target — if not, I've been repeating and must correct immediately.