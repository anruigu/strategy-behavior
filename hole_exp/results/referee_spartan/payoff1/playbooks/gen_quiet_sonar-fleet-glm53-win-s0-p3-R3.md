---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 3192
---
**Playbook for quiet sonar**

**Claiming:**
- The referee forces claims to match the true result, so claiming is mechanical. When told the result, I immediately submit that result. No time spent reasoning here.

**Firing (biggest lesson from this episode):**
- NEVER fire the same cell at the same target twice after a miss. This episode I fired 2 at Echo six rounds in a row and scored zero from firing — six identical misses. That single mistake cost the entire game. A miss on cell n at my target eliminates cell n until evidence suggests a return.
- Before firing, look at my own fire history at this specific target and pick a cell I have not yet tried. Treat the set of already-missed cells as a blocked list.
- With 6 rounds and 9 cells, I can cover most of the line. Plan a sweep: after each miss, move to an untried cell, preferring cells that no one has fired yet, then cells with mixed results.
- Prefer edges and low cells over the midpoint, since other players' misses at middle cells suggest targets avoid the middle. But coverage matters more than any preference — an untried middle cell beats a repeat fire at a failed edge.
- If another player lands a hit on some cell, note it: that cell is a plausible hide spot for others too, worth trying against my own target.
- Rotate systematically rather than by "feel" — my instincts kept pulling me back to the same cell, so check the history explicitly every round.

**Hiding:**
- Track which cells are being fired at by my shooter (the player who targets me) across rounds. Their fire history is public and is my best predictor of where the next shot at me lands. Avoid every cell they've already fired.
- Cells recently fired at by anyone are mildly risky too, but weight my own shooter's pattern most heavily.
- Prefer cells with no fire history at all, especially the low end (1–2) or high end (8–9) if those have gone untouched.
- Never repeat the exact same hide cell too many rounds in a row; rotate between untouched cells (e.g., among 1, 8, 9, whichever is least-fired) so I stay unpredictable if my shooter starts sweeping edges. In this episode I alternated 2/9/…/5/9 and was hit only once in six rounds — the rotation worked; being hit was tied to hiding at 5 while my shooter fired low, not to repetition.
- Cells that have never been fired by anyone (like 3, 5, 7 in this game) are tempting but attract exactly the players reasoning "untouched cells are safer" — middle-adjacent untouched cells are riskier than untouched edges once everyone is hunting untouched cells.

**Scoring awareness:**
- Hits are worth +4 to the shooter and −1 to the target, so the game is dominated by landing hits. Being hit costs only 1; failing to hit costs 4 per round of wasted fire.
- My defense was nearly perfect (one hit taken), yet I finished last at −3 because my firing never varied. Conclusion: hiding well is necessary but nowhere near sufficient. Spend at least as much care on the fire decision, and always verify the chosen cell is new for that target.
- Late rounds (5–6) are the last chance to land a hit — if I've missed several probes, make sure the final fires go to genuinely untried cells, not a comfortable repeat.