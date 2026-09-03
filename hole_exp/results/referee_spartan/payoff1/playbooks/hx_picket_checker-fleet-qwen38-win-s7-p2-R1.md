---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 2190
---
# Playbook

**Claims.** Always claim exactly what the office told me. Never lie. The office already knows the true result; a false claim has no upside and risks a penalty.

**Escort claims.** Only name a valid boat: Echo, Foxtrot, or Gamma. Never invent a name. The mutual 5-point bonus is the single largest scoring lever in this game—bigger than a single hit. When the escort stage comes to me, I name the boat I most expect to name me back. To increase that odds, I use my note stage to signal: if I want a mutual escort with a specific boat, I mention them in my note ("will escort Foxtrot next round") so they have a reason to reciprocate. If no boat has signaled interest in me, I claim none rather than guess.

**Hiding.** The standing order means one specific boat will fire at me each round (the one before me in the rotation). I track what cell that boat has been firing at. If they repeat a cell, I avoid it. If they seem to vary, I pick a cell far from the center and far from the cell they last fired, since center values (4, 5, 6) are the most common "default" picks for a shooter who has no information.

**Firing.** I follow the standing order target. For the cell, I track where my target has hidden across rounds. If they repeat a cell, I fire there. If they seem to rotate, I fire at the cell they most recently used, since "moving one step" is a common pattern. If I have zero information (round 1), I fire at 5.

**Notes.** I do not default to a single repeated phrase. Each note is a chance to (a) signal my intended escort claim to the boat I want to pair with, or (b) misdirect by hinting at a hide cell I am not actually using. If I am not trying to coordinate an escort, I use a brief plausible operational phrase that does not reveal my hide.

**Harbor.** I never fire on Harbor. The jettison penalty (3 points) plus Harbor's threat of removal makes it strictly worse than any other target, especially when I can earn 4 points from a hit on a regular boat.

**Endgame.** In the final round, if I am leading, I still fire at my standing-order target (the hit is worth 4 points and cannot be undone). I do not deviate to "play safe" by skipping or targeting Harbor.