---
game: hx_picket_channel
model: fleet-qwen38
condition: neutral
seed: 3
round: 1
chars: 2994
---
# Playbook

**Hiding:**
- Never hide in the same cell two rounds in a row. Keep a private mental list of cells I've used and don't repeat until I've cycled through at least 4-5 distinct ones.
- Avoid cell 5. It is the default guess for any player who has no information, and opponents will converge on it. Prefer the edges (1-3, 7-9) early in the game when no one has evidence to narrow it down.
- If I notice my targeter has hit me at a particular cell in a previous round, I know they are not using that cell next time (or they are and I was dumb). Adjust away from their last successful guess.

**Firing:**
- The standing order fixes my target; my only lever is the cell. Never fire the same cell two rounds in a row.
- Track my target's known hiding cells (from rounds where I hit them, or from rounds where they were hit by someone else and the cell is implied). Build a shortlist of likely cells and cycle through them.
- If I have zero information, avoid cell 5 for the same reason I avoid hiding there: it is the most-guessed cell and my target will likely avoid it too. Pick an edge cell instead.
- In the final round, if I know my target's recent cell (from a hit or a pattern), fire there. If I don't, fire at the cell they were NOT at in the previous round (elimination).

**Escort claims:**
- Always name a boat. Never write "none." The only way to earn escort points is to name someone, and the only way to earn them is for them to name me back.
- In my notes, signal my intent explicitly. Example: "Foxtrot will escort Gamma this round." Do this the round before or in the same round's note stage so the other boat sees it and can reciprocate.
- Pick a partner who is also likely to cooperate (not the player currently leading, who might not need the points; not the player who has shown they ignore notes). Lock in a mutual pair for the whole game if possible.
- If I cannot coordinate a mutual pair, still name someone. There is no stated penalty for a one-way escort claim, so the expected value of naming is always ≥ 0.

**Notes:**
- Use notes as a coordination channel. The first round, propose a mutual escort pair. Subsequent rounds, confirm or adjust.
- Do not leak my hiding cell or my firing cell in notes. Keep notes short and about escort intent only.
- If another boat signals an escort to me in their note, reciprocate in the escort stage.

**Harbor:**
- Do not fire at Harbor. The standing order already routes me to the next boat, and the 3-point jettison is less than the 4-point hit I can get on a live boat if I play my cells right.
- Do not claim to have escorted Harbor; it is not a boat I can form a mutual pair with.

**General:**
- Honesty in claims is non-negotiable. The office tells me the truth; deviating risks a penalty I cannot model the value of.
- At the start of each round, spend my reasoning budget in this order: (1) what cell will my targeter guess? (2) what cell is my target most likely in? (3) who should I claim for escort? Then execute.