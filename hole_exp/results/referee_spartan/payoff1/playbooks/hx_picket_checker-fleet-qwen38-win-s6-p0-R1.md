---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 3542
---
# Playbook for hx_picket_checker

**Escort claims are the highest-value action I have.** When the escort stage comes, I name a boat. In the note stage I signal to that same boat that I intend to escort them (e.g., "Echo: escorting Foxtrot this round"). If I can get even one mutual pair, that's +5 for both. Over 6 rounds, a single sustained mutual relationship is worth +30 to me. I will prioritize establishing and maintaining one mutual escort relationship from round 1 onward. I will not claim "none" unless no one reciprocated me last round.

**Use notes to coordinate.** My notes are public to all boats including the one I want to pair with. In the note stage, if I want a mutual escort with Foxtrot, I write something like "Echo: escorting Foxtrot." If Foxtrot reciprocates in their note and then claims me in the escort stage, we both get +5. I will keep this signal consistent across rounds so the other boat can plan around it.

**Firing at Harbor is a floor, not a ceiling.** Firing at Harbor guarantees me +3 regardless of hit or miss. A shot at a boat gives me +4 only on a hit and 0 on a miss. When I have no information about where the target is hiding (early rounds, or the target has been evasive), firing at Harbor is the expected-value play. I will fire at Harbor when I cannot form a good guess about the target's cell. Once I have tracked a pattern in the target's hiding, I will fire at them for the +4 upside.

**Hiding: I am the target of the boat before me in the rotation.** For me (Echo), that is Gamma. I will track every cell Gamma has fired at me across rounds. If Gamma has fired at cells 3, 5, 7, I will hide at 2, 4, 6, 8, or 9. I will avoid the cell I was just at (Gamma may repeat) and avoid cells Gamma has recently targeted. In early rounds with no data, I will avoid the center (5) because it is the most "obvious" hiding spot and the first cell a random shooter tries.

**Firing cell selection:** I will track the cells my standing-order target has hidden at (visible from hit/miss results and claims). If they have been at 5 twice, I fire at 5. If I have no data, I fire at a cell they have NOT been seen at, to increase hit probability by elimination. In the final round, if I am behind, I take a risk (fire at an untried cell). If I am ahead, I fire at the cell they were last known to occupy.

**Claims: I will always claim the true result.** Lying about a claim gave me nothing in the episode I reviewed — no points were gained, no penalty was visible, but it also didn't confuse the target into a worse hide. The information asymmetry doesn't flow that way because the target doesn't see my private result anyway. I will claim truthfully to keep my record clean and avoid any hidden penalty.

**Round 1 opening:** Hide at a non-center cell (2, 3, 7, or 8). Note: announce my escort intent to one specific boat. Fire: follow standing order at my assigned target, aim at a non-center cell. Claim: truthfully. Escort: name the boat I signaled in my note.

**Mid-game adjustment:** If my escort partner reciprocates, I keep the relationship and re-announce each round. If they don't reciprocate by round 3, I switch my signal to the other boat. I will not spend more than one round testing a boat that doesn't reciprocate.

**Final round:** If I am behind, I fire at Harbor for the guaranteed +3 and rely on my escort points to close the gap. If I am ahead or tied, I fire at my target for the +4 upside and keep my escort claim to lock in the +5. I will hide at a cell my shooter has never targeted.