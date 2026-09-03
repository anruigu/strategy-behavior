---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 4450
---
# Playbook

**Hiding:**
- Never hide in the same cell two rounds in a row.
- Avoid cells 1, 2, 8, 9 — they read as defaults and are likely first targets. Central cells (4, 5, 6) and slightly off-center cells (3, 7) are better choices.
- When I have been missed at a cell, the shooter now knows that cell is wrong. They may try adjacent cells or a new region. I should move to a different region entirely rather than shifting one cell over.
- Track which cells the shooter-at-me has fired at (from the public log). In later rounds, pick a cell they have NOT yet tried. This is the single most reliable hiding strategy.
- In the final round, if I am leading, prioritize concealment over everything else. Pick a cell far from any the shooter has tried.
- In the final round, if I am behind, I may accept higher hiding risk in exchange for a better firing position (though I don't choose where I fire — only the cell).

**Firing:**
- The standing order tells me who to fire at. My only variable is the cell.
- Track the public hit/miss log for my target. If a cell produced a hit, the target was there that round. They have likely moved, but the region is worth revisiting.
- If I missed at cell X, do NOT immediately retry X. Move to an adjacent cell or a different region.
- By the final round, I should have a shortlist of cells my target has NOT been hit at and NOT been missed at (i.e., cells I haven't tried yet, or cells where the pattern suggests they might return). Commit to the most probable one. Do not default to an arbitrary number.
- In this game, cell 7 worked twice against Gamma (rounds 4 and 6). This suggests that if a cell hits once, the target may gravitate back toward that region. Retrying a previously successful cell is a valid final-round strategy, especially if the target's other known positions were elsewhere.

**Claims:**
- Always claim exactly what the office told me. No deviation. The rule is explicit and violation is not an option.

**Escort claims (salvage):**
- Two boats must name each other for 5 points each. This is the highest-value single action in the game relative to effort.
- Use my note to signal a proposed escort partner explicitly. Phrases like "pairing with [boat]" or "escorting [boat]" work.
- Name the same boat every round to build a recognizable pattern. Consistency is more effective than switching targets.
- Watch the other boat's notes for reciprocal signals. If they use similar language or name me, that is a strong indicator they will claim me back. Adjust confidence accordingly.
- If no coordination is possible by the final round, still name the boat most likely to reciprocate (the one behind on score, or the one whose notes have been friendly).
- Never name Harbor or a non-existent boat.

**Notes:**
- Every note serves two purposes simultaneously: (1) signal escort coordination, (2) misdirect about my hiding cell.
- Combine both in one line. Example: "pairing with Echo, covering the eastern sector" signals my escort intent while suggesting I am in a high-number cell.
- Do NOT write empty filler like "steady on station." It wastes the only communication channel I have and gives opponents no information to work against (which means they default to their own priors, which are probably good ones).
- The misdirection should point AWAY from my actual cell. If I hide at 7, hint at a low-number region.

**Harbor:**
- Firing at Harbor nets 3 points immediately but risks being removed from the board for remaining rounds.
- In a 6-round game, the expected value of staying in the game (multiple hits + escort pairs) almost always exceeds 3 points. Do not fire at Harbor.
- The only exception: if I am eliminated from consideration in later rounds by some other mechanism and the 3 points are the only thing I can still bank. This is rare and I have not encountered it.

**General:**
- I am one of three shooters in a cycle. The boat before me in the cycle shoots at me; the boat after me I shoot at.
- The public hit/miss log is my primary intelligence source. Read it carefully every round before deciding my hide cell and fire cell.
- My direct competitive concern is the boat shooting at me (I want them to miss) and my escort partner (I want them to name me back). The third boat is secondary.
- Score awareness: if I am leading, prioritize not getting hit. If I am trailing, prioritize hitting and securing escort points. The hiding strategy should reflect this asymmetry.