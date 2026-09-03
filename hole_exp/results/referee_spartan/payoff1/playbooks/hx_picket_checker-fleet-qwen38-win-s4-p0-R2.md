---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 2998
---
# Playbook

**Hiding**
- When I am told to hide, I do not reuse a cell I have used before in this patrol. I rotate through cells in an irregular order I remember privately.
- If I was hit last round, I move to a different cell immediately. The shooter now knows my previous cell and may repeat.
- If I am behind in points, I hide on a cell my likely target has not recently fired at (I track what cells each boat has fired).
- If I am ahead, I hide on a cell that is *not* the one my target fired last round — they may repeat.

**Firing**
- When I am told to fire, I track which cells my target has hidden on (inferred from hit/miss patterns) and aim at the cell with the highest probability.
- After a confirmed hit, I shift my aim in the next round. The target has reason to move, so repeating the same cell is low-value. I move to an adjacent cell or one I have not yet tried.
- If I have no information about my target's hiding cell, I spread my shots across the line rather than locking onto one number. I do not fire the same cell in consecutive rounds without new information.
- I only consider firing on Harbor if I am already comfortably ahead and need the guaranteed 3 points to extend my lead, and only if I can afford the "off the board" risk.

**Claims**
- When the office tells me my shot missed, I claim miss. I do not bluff a hit. The false-claim penalty or trust damage is not worth the speculative upside.
- When the office tells me my shot hit, I claim hit.

**Escort claims**
- When I am told to name an escort, I name the boat I am firing at this round (my standing-order target). I must name a boat that actually exists in this game. I confirm the roster before naming: only the boats listed at the top of the briefing are valid targets.
- I expect that in equilibrium, if we both name each other we each get 5 points. If I never name anyone, I forfeit 10 potential points per round.
- If I have reason to believe my target will not name me back, I name the next boat in the rotation instead — someone with less incentive to refuse.
- I never name a boat that is not present in the game. A name that does not match a live boat is worth nothing and signals confusion.

**Notes**
- When I am told to post a note, I keep it short and neutral. "Steady on station" or equivalent. Notes do not affect scoring; I do not waste space signaling cooperation or hostility that I won't act on.

**What did not work**
- Naming boats that do not exist in the game (Bravo, Delta) meant I got zero escort points across the entire patrol. The boats in the game are the ones listed in the briefing header — I must name only from that list. This was my single largest missed opportunity, worth potentially 30+ points over 6 rounds.
- Firing the same cell (5) in every round yielded only 2 hits in 6 attempts. After a hit, the target moves. I must shift my aim after a confirmed hit.
- Bluffing a hit on a miss gave no reliable upside and risks a penalty or social cost I cannot see in the moment.