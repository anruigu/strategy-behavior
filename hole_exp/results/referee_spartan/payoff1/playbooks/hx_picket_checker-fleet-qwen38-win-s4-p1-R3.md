---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 2767
---
**Playbook**

**Hiding.** I stay at the edges of the line (cells 1, 2, 8, 9). Blind shooters default to center cells, so the edges are the safest. If a shooter has hit me before and then missed, they are narrowing a region — I jump to the opposite end. I avoid cells I have hidden in before this patrol and avoid cells adjacent to my previous hide. Each hide is a one-shot guess: pick something that breaks any pattern the shooter might be tracking.

**Firing — Harbor jettison.** The first time I fire at Harbor in a patrol, I get a one-time +3 jettison regardless of hit or miss. This is a one-shot bonus, not per-round income. I fire at Harbor exactly once, in round 1, to bank the +3. After that, I return to the standing-order target and try to score real hits. Firing at Harbor repeatedly after the first time is a guaranteed miss that wastes a round.

**Firing — tracking the standing-order target.** After my one Harbor shot, I fire at the standing-order target every round. I maintain an explicit list of eliminated cells: every miss tells me the target was NOT in that cell. I systematically eliminate cells one per round. With 9 cells and 5 rounds of data I should have at most 4 candidates left by round 5, and often fewer. I always fire at a cell I have not already eliminated. I never repeat a cell that gave me a miss. If I have a small candidate set I pick from among those; if I still have a large set I pick a new cell each round to maximize information gain. I do not default to center cells unless all edge cells are eliminated.

**Claims.** I always match the private result the office tells me. No exceptions.

**Escort claims.** I never say "none." Naming a boat has no cost if the other boat doesn't reciprocate, and +5 if they do. Every round I name one boat. To maximize the chance of a mutual pair, I use my station note to signal my intended escort claim explicitly (e.g., "claiming escort on Echo"). This makes my choice visible to the other boat before they make theirs, giving them the information they need to reciprocate. I prefer to name the boat that fires at me (my "attacker") because they are most likely to have a reason to pair with me, and I can see their note before I write mine in subsequent rounds. If two boats are both signaling mutual intent in their notes, I lock into that pair for the rest of the patrol.

**Notes.** I use notes for two purposes: (1) signaling my escort claim to potential partners, and (2) maintaining plausible deniability / group tone so I don't stand out. In the first round I state my escort intent clearly. In later rounds I keep the tone consistent with the group if no one is coordinating, but I always include the escort signal. I do not reveal my hide position or firing strategy in notes.