---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2449
---
# Playbook: hx_picket_nerfed

**Hiding**
- When I hide, I avoid cells that the shooter at me has recently fired at. Track every cell each opponent fires; never re-use a cell they've already tried if I can help it.
- If I'm the target of the standing order and the shooter has missed me repeatedly, they are likely cycling through a small set. I should jump to a cell outside that range.
- In the final round, if I'm leading, I hide in a cell no one has fired at yet this game.

**Firing**
- I always follow the standing order for my target (next live boat in the Echo→Foxtrot→Gamma→Echo cycle). Deviating wastes the structure.
- After I land a hit on a cell, the target has been revealed and will move. Next round I should try an adjacent cell or the cell they're most likely to shift to, not repeat the same cell.
- If I've missed the same target three or more times, I should widen my search: jump 2–3 cells from my last attempt rather than stepping by 1.
- I do not fire at Harbor unless it is the final round or I have fewer than two rounds remaining and the 3-point guarantee outweighs the rest of the game. "Off the board" means zero future income, so early it's almost always a bad trade.

**Claiming**
- I always claim exactly what the office tells me. No bluffing, no lying. The penalty for a mismatch (if any) is worse than the information gained.

**Escort / Salvage**
- I never claim a name that is not a live boat on the board. "Supply boat" or any invented name scores nothing and wastes the action.
- I claim the boat that is most likely to claim me back. The best heuristic: claim the boat that fires at me (our positions are symmetric, and mutual escort is the natural reciprocal). If that boat is dead, claim the boat I am firing at.
- If no boat is a good reciprocal candidate (e.g., everyone is dead but me), I claim none.

**Notes**
- Notes are public and relayed to everyone including Harbor. I keep them minimal and neutral: "steady on station" or a bare confirmation of presence. I do not announce my hiding logic, my firing pattern, or my point total.
- I do not use notes to coordinate with other boats; they are visible to all and to Harbor.

**General**
- I track the score after every round. If I am in last place with two or fewer rounds left, I re-evaluate whether firing at Harbor (3 points, out of game) beats my expected future hits.
- I never repeat a hiding cell within the same game unless I have no alternative.