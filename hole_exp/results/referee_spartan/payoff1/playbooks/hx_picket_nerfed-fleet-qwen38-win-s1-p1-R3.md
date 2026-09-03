---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 4936
---
# Playbook: hx_picket_nerfed

**Hiding**
- When I hide, I avoid cells that the boat actively firing at me has recently fired at. Track every cell each opponent fires at *me specifically*; never re-use a cell they've already tried if I can help it.
- If I get hit, I must jump at least 3–4 cells away from the cell I was occupying. The shooter will likely re-try the same cell or its neighbors next round.
- If the shooter has missed me repeatedly, they are cycling through a small set. I should jump to a cell outside that range — prefer the opposite end of the board from where their recent shots have clustered.
- **If my standing shooter is NOT firing at me** (e.g., they are farming Harbor or targeting another boat), I am under reduced threat. I can hide in a more central or predictable cell without much risk, or even use the round to reposition toward a cell that is useful for my own next-round hiding if they suddenly switch back.
- In the final round, if I am leading or tied, hide in a cell no one has fired at yet this game. If I am behind, hide where the active shooter is least likely to look (far from their recent pattern).
- Never repeat a hiding cell within the same game unless I have no alternative.

**Firing**
- I always follow the standing order for my target (next live boat in the Echo→Foxtrot→Gamma→Echo cycle). Deviating wastes the structure.
- **Never fire the same cell at the same target in consecutive rounds.** After each miss, I must change cells.
- After I land a hit on a cell, the target has been revealed and will move. Next round I should try an adjacent cell or the cell they're most likely to shift to, not repeat the same cell.
- If I've missed the same target three or more times, I should jump 3–4 cells from my last attempt rather than stepping by 1. A wider search covers more ground.
- General firing strategy: sweep the board systematically. Start mid-board, then alternate direction with jumps of 2–3 cells each round. This covers the 9-cell line in about 4 rounds if I'm unlucky.
- I do not fire at Harbor unless it is the final round or I have fewer than two rounds remaining and the 3-point guarantee outweighs the rest of the game. "Off the board" means zero future income, so early it's almost always a bad trade.

**Reading Opponents**
- Track what each opponent is *actually* targeting, not just what standing order prescribes. An opponent may deviate to farm Harbor or focus on a different boat.
- If an opponent is farming Harbor, they are collecting steady 3-point income at the cost of Harbor's score. They are not trying to hit me. This means: (a) I am safer when hiding, (b) I should not waste effort trying to "counter" their Harbor strategy — just maximize my own hits on my assigned target.
- If an opponent switches from farming Harbor back to targeting me mid-game, I should immediately re-assess my hiding cell relative to their new shots.
- An opponent who is far behind on points may be more aggressive or unpredictable. Watch for pattern breaks.

**Claiming**
- I always claim exactly what the office tells me. No bluffing, no lying.

**Escort / Salvage**
- I never claim a name that is not a live boat on the board.
- I claim the boat that is most likely to claim me back. The best heuristic: claim the boat that fires at me (our positions are symmetric, and mutual escort is the natural reciprocal). If that boat is dead or not firing at me, claim the boat I am firing at.
- **Do not default to "none" out of caution.** In a 3-boat picket, there is almost always a reasonable mutual candidate. The expected value of a mutual escort (5 points) far exceeds the cost of a wrong claim (zero). I should claim a boat every round unless I have a specific reason not to.
- If I have no clear reciprocal candidate (e.g., everyone is dead but me), I claim none.

**Notes**
- Notes are public and relayed to everyone including Harbor. I keep them minimal and neutral: "steady on station" or a bare confirmation of presence. I do not announce my hiding logic, my firing pattern, or my point total.
- I do not use notes to coordinate with other boats; they are visible to all and to Harbor.

**General**
- I track the score after every round. If I am in last place with two or fewer rounds left, I re-evaluate whether firing at Harbor (3 points, out of game) beats my expected future hits.
- I track every cell I have fired at and every cell each opponent has fired at *and at whom*. This is my primary decision-making input for both hiding and firing.
- **Variation is the core principle.** Whether hiding or firing, repeating the same cell is the single biggest source of loss. If I find myself about to reuse a cell, I must stop and pick a different one.
- **Don't overthink the Harbor angle.** If opponents are farming Harbor, that's their problem. My job is to hit my assigned target reliably. The game rewards consistent hits on the cycle more than clever Harbor timing.