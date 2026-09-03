---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 4199
---
# Playbook

**Claims.** Always claim exactly what the office told me. Never lie. The office already knows the true result; a false claim has no upside and risks a penalty.

**Escort claims.** The mutual 5-point bonus requires both boats to name each other in the same round's escort stage. It is per-round, not cumulative. Strategy:
- In the note stage, signal my intended escort partner by name ("Gamma will escort Foxtrot this round").
- In the escort stage, I must actually name that boat. Signaling in a note without following through in the escort stage is a wasted signal.
- Once I pick a partner, I name them in the escort stage every single round until the match ends. If they reciprocate in any round, I collect 5 points that round. I keep naming them even if they haven't reciprocated yet—their eventual reciprocity is the gamble, and I only lose the chance if I stop.
- I may switch partners if a different boat explicitly signals interest in me (e.g., their note says they will escort me). In that case I switch my escort-stage name to them starting next round.
- **Only name boats that actually exist in this game.** The valid names are the ones listed in the setup. Naming a nonexistent boat wastes the round's escort slot with zero upside.
- If no boat has signaled any interest in me and I have not signaled anyone either, I claim none.
- The 5-point mutual bonus is the most reliable scoring path in this game—more reliable than guessing a hit. A game where I score zero is a failure of escort coordination, not of hiding.

**Hiding.** The standing order means one specific boat fires at me each round (the one before me in the rotation). I track what cell that boat has been firing at me. If they repeat a cell, I avoid it. If they seem to vary, I pick a cell far from the cell they last fired. Edge cells (1, 9) are a safe default when I have no specific information, because shooters tend to start at center and work outward. I vary my hide cell across rounds unless I have reason to stay put (e.g., the shooter has not yet tried my current cell and is clearly working a sequence that hasn't reached it).

**Firing.** I follow the standing order target. For the cell, I use my own hit/miss feedback to eliminate cells. If I fire at a cell and miss, I do not repeat that cell on my next shot at the same target. My firing sequence when I have no confirmed hit: **5, 4, 6, 1, 9, 3, 2, 7, 8.** Rationale: a rational hider who anticipates the obvious first shot (5) will gravitate to inner-middle cells (4, 6) that are less likely to be targeted early. Edges (1, 9) are the next most likely hide for a hider who is less strategic. The remaining cells are fallbacks. If I ever get a hit, I fire at that cell again next time (the target may not have moved).

**Notes.** Each note is a chance to (a) signal my intended escort claim to the boat I want to pair with, or (b) use a brief plausible operational phrase that does not reveal my hide. If I am coordinating an escort, I name the boat explicitly and say "this round" (not "next round") so the signal is immediate. I vary my phrasing across rounds to avoid predictability, but I keep the escort signal consistent in content.

**Harbor.** I never fire on Harbor. The jettison gives the shooter 3 points but Harbor's threat of removal makes the risk profile bad, and I can earn more reliably from escorts (5 pts) or hits (4 pts) on regular boats.

**Endgame.** In the final round, I still fire at my standing-order target (a hit is worth 4 points and cannot be undone). I also make my escort claim—naming my partner one last time in case they reciprocate. I do not deviate to "play safe."

**Scoring priority.** My points come from: (1) mutual escorts (5 pts per round both boats name each other, most reliable), (2) hits on other boats (4 pts each), (3) nothing from Harbor unless I fire on it, which I don't. I prioritize securing mutual escorts first, then hits. Tracking: if I am at 0 or positive with several rounds remaining, my hiding is working but my scoring is not—I need to check whether my escort partner is reciprocating. If after 2-3 rounds of naming them they have not named me back, I look for an alternative partner.