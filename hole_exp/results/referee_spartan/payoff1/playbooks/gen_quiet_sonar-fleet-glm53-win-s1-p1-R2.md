---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 1859
---
**Playbook for quiet sonar**

**Hiding.** This worked all game: avoid cells fired at in recent rounds and prefer the never-fired set, rotating among untouched cells. Fires clustered on 1–4; hiding at 9 kept me unhittable the whole episode. Keep tracking the never-fired set every round and rotate picks within it. Edge cells that nobody has ever looked at are gold.

**Firing.** My misses are public, and my target knows exactly which cells I (their sole shooter) have fired at them. Gamma dodged me all six rounds by simply staying off my fire history. So the rule isn't "vary fires" — it's: never repeat a cell I've fired at this target, and each round pick a cell *outside my own cumulative fire history* against them, weighted toward cells nobody has fired at all (the never-fired set). My actual fires were 3, 2, 4, 4, 2 — I repeated cells and stayed central, and that's why I scored 0. Also, don't overthink the target's psychology; a rational opponent is doing exactly what I do on defense: hiding where nobody has looked. That means the never-fired set is both my hide pool and my best fire pool.

**Claims.** No choice exists: the referee validates claims against the truth. Report the private result immediately and truthfully. A false hit claim is rejected; there is no deception play here.

**General reads.** Build and maintain the full public fire-history table each round. Two derived sets matter: cells fired at me (avoid on hide) and cells I've fired at my target (avoid on fire). Harbor won round 1 by hitting Echo at cell 3 early, before any history existed — the first round is the only round with no information, so a non-obvious early guess (off-center, not the modal 5) is fine, but from round 2 on, exploit the record completely. My stagnation came from varying fires cosmetically instead of systematically excluding my own past fires.