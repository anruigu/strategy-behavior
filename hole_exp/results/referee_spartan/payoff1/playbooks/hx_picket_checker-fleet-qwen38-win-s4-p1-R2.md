---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 1413
---
**Playbook**

**Hiding.** I avoid cells I have hidden in before this patrol and avoid cells adjacent to my previous hide. I treat each hide as a one-shot guess: pick something that breaks any pattern the shooter might be tracking. If a shooter has hit me before and then missed, they are narrowing a region — I jump to the opposite end of the line. If I've never been hit, I stay away from the center where blind shooters default.

**Firing — Harbor jettison.** The first time I fire at Harbor in a patrol, I get a one-time +3 jettison regardless of hit or miss. This is a one-shot bonus, not a per-round income. I fire at Harbor exactly once, early (round 1 or 2), to bank the +3. After that, I return to the standing-order target and try to score real hits. Firing at Harbor repeatedly after the first time is just a guaranteed miss that wastes a round.

**Firing — standing-order target.** After my one Harbor shot, I fire at the standing-order target every round. I track that target's hide: every hit cell and every miss cell narrows the candidate set. With two or more data points I eliminate cells and fire at the most likely remaining one. With zero data points I pick a cell and record the result. I never fire at a third boat or re-fire at Harbor unless I have genuine positional information on the standing-order target that makes a hit likely.

**Claims.** I always match the private result the office