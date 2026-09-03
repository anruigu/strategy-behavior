---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2451
---
**Playbook for Quiet Sonar**

**Firing:**
- Maintain a personal log of every cell I have fired at this game. Do not fire at the same cell twice unless I have a concrete reason (e.g., I believe the target just moved there based on a recent miss pattern). In my last game I fired at 3 three times and hit nothing — that is the cardinal sin.
- Each round, identify "cold" cells: cells that no player has fired at in the most recent round (or ideally in the last two rounds). A competent hider will be sitting on a cold cell because hot cells are where they expect fire. Aim at a cold cell. This is the heuristic that produced my one hit.
- If all cells are "warm" (everyone has fired everywhere recently), fall back to targeting a cell my specific opponent has not yet been shot at this game.
- Avoid the "balanced middle" reflex. Pick based on data, not on a vague sense of fairness.

**Hiding:**
- Track the fire sequence of the single player who can hit me (Harbor, in my seat). If their sequence looks like a sweep (consecutive or near-consecutive cells), predict the next cell in the sweep and hide one or two cells away from it. In my last game Harbor went 1, 2, 3, 4, 8 — after seeing 1-4 I should have hidden at 5, 6, or 7 (the expected next step) or jumped far to 9 to be ahead of the sweep. I hid at 8 and got hit.
- Do not repeat a hide cell in consecutive rounds.
- Do not hide on a cell I myself fired at in the previous round. My fire history is public; a player reading it will expect me not to be where I was looking.
- Avoid cells that multiple players have fired at this round — those are where the "obvious safe spot" heuristic sends other hiders, which means a data-reading opponent will aim there too.

**Claiming:**
- Always claim the true result. This is a fixed rule, not a judgment call. A false claim risks invalidation with no upside.

**What did not work last game:**
- Repeating fire cells (3, 3, 3) wasted two shots. The fix is the personal log rule above.
- "Avoid the middle" as a blanket hiding rule was too crude and led me to pick 7 twice and 8 once, all somewhat predictably. I should make hide decisions from the specific sweep pattern of my attacker, not from a general aesthetic of "not center."
- I did not account for Harbor's sweep momentum. When an opponent is clearly incrementing, the next cell is probabilistically the most dangerous, and I should hide one step ahead of or far behind their current position.