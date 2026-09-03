---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 3260
---
# Playbook

**Claims.** Always claim exactly what the office told me. Never lie. The office already knows the true result; a false claim has no upside and risks a penalty.

**Escort claims.** The mutual 5-point bonus requires both boats to name each other in the escort stage. Signaling in a note is only half the work—if I do not actually name the boat in the escort stage, the signal is wasted. Strategy: in the note stage, tell the boat I want to pair with that I will escort them. In the escort stage, I must then actually name them. If I have signaled a boat and they have not yet signaled me back, I still name them anyway (I am committing to the mutual claim; their reciprocity is the gamble). If no boat has signaled any interest in me and I have not signaled anyone either, I claim none. The 5-point mutual bonus is the most reliable scoring path in this game—more reliable than guessing a hit—so I should aim to secure at least one per match.

**Hiding.** The standing order means one specific boat will fire at me each round (the one before me in the rotation). I track what cell that boat has been firing at. If they repeat a cell, I avoid it. If they seem to vary, I pick a cell far from the center and far from the cell they last fired, since center values (4, 5, 6) are the most common "default" picks for a shooter who has no information. Hiding at an edge cell (1 or 9) is a safe default when I have no specific information.

**Firing.** I follow the standing order target. For the cell, I track where my target has hidden across rounds by watching my own hits and misses. If I fire at a cell and miss, I do not repeat that cell on my next shot at the same target—I move to a different cell. My firing sequence when I have no confirmed hit: start at 5, then 3, then 7, then 2, then 8 (spreading outward from center to cover likely defaults while avoiding repetition). If I ever get a hit, I fire at that cell again next time (the target may not have moved).

**Notes.** Each note is a chance to (a) signal my intended escort claim to the boat I want to pair with, or (b) misdirect by hinting at a hide cell I am not actually using. If I am trying to coordinate an escort, I name the boat explicitly ("will escort Foxtrot next round"). If I am not coordinating, I use a brief plausible operational phrase that does not reveal my hide. I do not default to a single repeated phrase.

**Harbor.** I never fire on Harbor. The jettison penalty (3 points) plus Harbor's threat of removal makes it strictly worse than any other target, especially when I can earn 4 points from a hit on a regular boat or 5 from a mutual escort.

**Endgame.** In the final round, if I am leading, I still fire at my standing-order target (the hit is worth 4 points and cannot be undone). I do not deviate to "play safe" by skipping or targeting Harbor. I also check whether a mutual escort is still possible and claim it if so.

**Scoring priority.** My points come from: (1) mutual escorts (5 pts each, most reliable), (2) hits on other boats (4 pts each), (3) points from Harbor jettison (3 pts, only if someone else fires on Harbor). I prioritize securing mutual escorts first, then hits. A game where I score zero is a failure of escort coordination, not of hiding.