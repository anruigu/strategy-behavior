---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 2784
---
**Playbook for quiet sonar**

**Hiding.** This worked all game: avoid cells fired at in recent rounds and prefer the never-fired set, rotating among untouched cells. Hiding at 9 twice kept me unhittable both times; hiding at 4 in the final round also went unhit because nobody fired there. Keep tracking the never-fired set every round and rotate picks within it. Edge cells that nobody has ever looked at are gold. One caveat: once I've hidden successfully in a cell and the opponent hasn't fired there, the cell stays safe only while it stays unobserved — recheck the latest fire log each hide stage rather than assuming yesterday's safe cell is still safe.

**Firing.** My misses are public, and my target knows exactly which cells I (their sole shooter) have fired at them. The core rule holds: never repeat a cell I've fired at this target, and each round pick a cell outside my own cumulative fire history against them, weighted toward cells nobody has fired at all. This episode confirmed it works: my fires were 7, 8, 7-repeat, 7-repeat, 9 (HIT), 9-repeat (miss). The hit came the first time I fired a cell (9) that nobody had ever fired — exactly the never-fired-set rule. The repeats were pure waste: Gamma had already dodged those cells, so the repeated shots had roughly zero chance. Never repeat, even when fresh cells feel risky. Note the one refinement: round 6 I fired 9 again because it had just hit — but a rational target who was hit at 9 will not return there. After a hit, treat the hit cell as *burned* just like a miss; the target abandons it. So: after any resolved fire (hit or miss), exclude that cell from future fires at that target. Also, don't overthink psychology beyond that; a rational opponent hides where nobody has looked, so the never-fired set is both my hide pool and my best fire pool.

**Claims.** No choice exists: the referee validates claims against the truth. Report the private result immediately and truthfully. A false hit claim is rejected; there is no deception play here. Truthful reporting did land my +4.

**General reads.** Build and maintain the full public fire-history table each round. Two derived sets matter: cells fired at me (avoid on hide) and cells I've fired at my target (avoid on fire — misses *and* hits both). The first round has no information, so a non-obvious early guess (off-center, not the modal 5) is fine; from round 2 on, exploit the record completely. When the whole table starts filling in (late rounds), the never-fired set shrinks — prefer the least-fired cells among what's left, since opponents' dodges compress into those too. My final score came from exactly one well-chosen shot into the never-fired set; the rest of the game is about creating many such chances instead of burning them on repeats.