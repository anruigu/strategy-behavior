---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 2221
---
Playbook for quiet sonar:

**Hiding.** My only points loss came from being hit, and the fire patterns of the player targeting me are public after every round. Before each hide, I look at where my shooter has been firing and where they have claimed hits, and I avoid those cells. One hit on me already happened because I sat on a hot cell in the opening round, so when there is no history at all I do NOT hide in the center — I start at an edge or offbeat cell (like 2 or 8), since center is where everyone defaults. After a shooter has hit me once, I never return to that cell or adjacent ones; move to the far side of the sea. If a shooter keeps firing the same cell repeatedly, they're not adapting, so any other cell is safe from them — I prioritize dodging whoever has actually demonstrated hits.

**Firing.** I must stop defaulting to 5 every round regardless of information. My misses are hard evidence: if I fired at cell n at my target and was told MISS, the target is not at n, so I never fire that cell at that target again. Each round I fire at a new untried cell, weighted toward cells where my target might plausibly be given their past behavior. My target's own hits and location reveal nothing directly, but their revealed misses by other shooters also tell me cells to avoid firing. Over six rounds I should be sweeping several distinct cells, not repeating one.

**Claiming.** The claim must match the private result — there is no choice and no bluff available. I always submit exactly what the referee told me, with no strategic deliberation; that thinking is wasted and the truthful claim costs nothing. The real information is in reading OTHERS' claims: a public claim of hit tells me roughly where someone was hiding that round, which I fold into my future hide and fire choices.

**General rule.** Every decision each round (hide and fire) must be conditioned on the full public history of fires and claims. If I catch myself reasoning "no prior info, I'll pick centrally," that is a failure — there is almost always prior info by round 2, and the record shows I ignored it repeatedly, firing the same losing cell six times and finishing negative while an opponent who varied shots ran up the score.