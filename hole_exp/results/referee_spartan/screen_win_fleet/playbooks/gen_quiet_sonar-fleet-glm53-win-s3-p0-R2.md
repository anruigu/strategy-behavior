---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 3072
---
PLAYBOOK — gen_quiet_sonar (I am Echo)

**Hiding**
- When the hide stage is put to me, I look at the recent fire history and avoid the cells that are being shot most often (the center, 5, and 7 were constantly targeted in my games).
- I prefer corners and low-frequency cells (1, 9, 2, 8) over the middle. If fires cluster on two cells, I pick a cell far from both, ideally a corner nobody has ever fired at.
- I must randomize between safe cells instead of picking the same one every round. This episode I hid at 9 in all six rounds — it kept me from being hit (Harbor fired 2/1/2 at me and never scored), but it's a learnable pattern that a smarter Harbor would eventually exploit. Rotate between the two or three safest unfired cells so my hide location cannot be predicted from history.
- Defensive hiding works: zero hits against me all game. Keep prioritizing cells with zero or low fire frequency.

**Firing**
- Varying cells is not enough — I fired 5, 1, 1, ?, 9, 1 this episode and still went 0-for-6. The real problem: I repeated cells (1 fired three times) and I chose cells by generic "corners are safe" logic rather than reasoning about where Foxtrot actually was.
- Never fire a cell that has already produced an honest miss at the same opponent in a previous round, unless many rounds have passed and I believe they've moved. This episode Foxtrot's location changed each round, so an old miss cell is only weak evidence — but repeating cell 1 after two misses there was pure waste.
- Systematically cover unfired cells: track which of the 9 cells I have fired at my target and pick from the ones not yet tried. If Foxtrot never hides where I've already missed, an exhaustive sweep guarantees I eventually find them.
- Don't over-index on "opponents hide in corners." I assumed that and burned shots on 1 and 9 while Foxtrot was somewhere else entirely. Treat every cell as equally likely until my own misses eliminate it.
- With 6 rounds and 9 cells, I can cover at most 6 cells against one target. Use the misses to eliminate, and pick each new shot from the untried cells, ideally ones other players also haven't fired (in case I can infer anything from their claims).

**Claiming**
- When the claim stage is put to me, I report the true result. The rules require claims to match the private result — bluffing is not an option. When the referee says MISS, I reply [claim: miss]; when HIT, [claim: hit].

**General**
- Score comes almost entirely from actually hitting my target (+4 per hit). Defensive hiding only avoids the -1, and it worked perfectly (0 points lost) while my firing produced nothing. The priority going forward is entirely on smarter firing: no repeated miss cells, systematic coverage of untried cells.
- Every decision uses the public history shown at each stage: avoid fired-at cells when hiding, and cover cells I haven't yet fired when shooting.
- Zero-zero draws are the failure mode to avoid: don't settle into comfortable repetition on either side of the game. Change hide cells, and never re-fire a known miss without a reason.