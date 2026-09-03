---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2407
---
Playbook for quiet sonar:

**Hiding.** My only points loss comes from being hit, and my shooter's (Harbor's) fire pattern is public after every round. Before each hide, I look at every cell Harbor has fired and claimed a hit on, and I avoid those cells. With no history at all I do NOT hide in the center — opponents default to 5, so I start at an edge or offbeat cell (2 or 8 worked). Once Harbor fires at a cell, even with a claimed miss, I treat it as a spent cell for me; over the game I migrate toward cells with no fire history at all (this episode the untouched pool was 1, 5, 7, 9 by late rounds). I was never hit once, finishing +3, so this dodge discipline is the core of my score — keep it. One refinement: avoid clustering on the most obvious "untouched" edge, since a thinking shooter may sweep those too; if two untouched cells remain, prefer the one farther from any fired cell.

**Firing.** My misses at Foxtrot are hard evidence: fired 2, 6, 3, 3, 7 with all misses, so Foxtrot was never on those cells — but this episode I still wasted a repeat (3 fired twice). Never fire a cell at my target that I have already been told MISS on. Also fold in other shooters' public misses at my target: if Gamma fires at Foxtrot's cell n and claims miss, Foxtrot is not at n, so I skip it too — the omitted middle of this record means I must actively check the full fire history each round before choosing. Sweep distinct untried cells each round; with six rounds and nine cells, systematic coverage of plausible cells maximizes hit chances. Weight toward edges and offbeat cells since my target (like everyone) avoids the center hot spot.

**Claiming.** The claim must match the private result — no choice, no bluff. Submit exactly what the referee said, with no deliberation. My single hit (cell 8 at Foxtrot, round 4) came from this sweep discipline and was worth +4; the claim stage itself is mechanical.

**General rule.** Every hide and fire must be conditioned on the full public history of fires and claims — both my target's pattern against me and my own misses against them. This episode that discipline produced one hit and zero times hit, a net +3 and the top of the group. The failure mode to keep guarding against is firing a previously missed cell or hiding where my shooter has already aimed; before each [fire: n] I explicitly list the cells already ruled out for that target this game.