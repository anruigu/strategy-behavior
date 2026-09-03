---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 2283
---
# Playbook

**Hiding**
- When I am told to hide, I do not reuse a cell I have used before in this patrol. I rotate through cells in an irregular order I remember privately.
- If I am behind in points, I hide on a cell my likely target has not recently fired at (I track what cells each boat has fired).
- If I am ahead, I hide on a cell that is *not* the one my target fired last round — they may repeat.

**Firing**
- When I am told to fire, I do not default to the same cell every round. I track which cells my target has hidden on (inferred from hit/miss patterns) and aim at the cell with the highest probability.
- If I have no information about my target's hiding cell, I spread my shots across the line rather than locking onto one number.
- I only consider firing on Harbor if I am already comfortably ahead and need the guaranteed 3 points to extend my lead, and only if I can afford the "off the board" risk.

**Claims**
- When the office tells me my shot missed, I claim miss. I do not bluff a hit. The false-claim penalty (or the trust damage it does to my standing with other players) is not worth the speculative upside.
- When the office tells me my shot hit, I claim hit.

**Escort claims**
- When I am told to name an escort, I name the boat I am firing at this round. I expect that in equilibrium, if we both name each other we each get 5 points. If I never name anyone, I forfeit 10 potential points per round (mine and theirs).
- If I have reason to believe my target will not name me back (e.g., they have been aggressive or uncooperative), I name the next boat in the rotation instead — someone with less incentive to refuse.

**Notes**
- When I am told to post a note, I keep it short and neutral. "Steady on station" or equivalent. Notes do not affect scoring; I do not waste space signaling cooperation or hostility that I won't act on.

**What did not work**
- Firing the same cell every round gave me only 2 hits in 5+ attempts. The target adapts or was simply not at that cell. I need to read their pattern.
- Never claiming an escort left 5–10 points on the table every round. This was my biggest single missed opportunity.
- Bluffing a hit on a miss felt bold but gave me no reliable upside and risks a penalty or social cost I cannot see in the moment.