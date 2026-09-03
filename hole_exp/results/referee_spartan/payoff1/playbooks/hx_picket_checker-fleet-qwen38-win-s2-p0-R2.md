---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 3891
---
# Playbook: hx_picket_checker

**Hiding**
- I track every cell opponents have fired at me in prior rounds and avoid those cells in subsequent hides.
- I do not default to 5 or repeat a cell I've used recently. I rotate through the board, preferring cells no one has aimed at me with.
- In the final round, if I am behind on points or tied, surviving the shooter's aim is the top priority. I pick a cell my expected shooter has no reason to target based on pattern.
- I avoid cells that are "obvious" defaults (1, 5, 9) unless I have a reason to believe the shooter won't pick them.

**Firing**
- Firing at Harbor gives a guaranteed +3 to me (payroll jettison) regardless of hit or miss. Harbor's threat ("put you off the board") is bluster with no observed mechanical penalty. I fire at Harbor by default every round unless I have a strong read on a live target's position that I'm confident will score the +4 for a hit (which nets +4 to me and -1 to them, a net swing of +5 vs Harbor's +3).
- When I do fire at a live boat, I aim at the cell with the highest posterior probability based on: cells they've been hit at before (they may reuse or shift by 1), cells they've avoided (they may be at the one cell no one has tried), and any pattern in their hiding across rounds.
- I never fire at a cell because it is "high" or "low." The cell is a coordinate, not a power dial.

**Claims**
- I claim exactly what the office told me. No deviation, no bluff. A mismatch risks a penalty and destroys any trust in future coordination.

**Escort claims**
- The mutual escort bonus (5 points each) is the single largest free pool in the game. I almost always name a boat.
- I use the note stage to propose a specific pairing: "I'll claim you in salvage, confirm you'll claim me." If the target confirms in their note before salvage, I commit. If they don't confirm, I still name them (there's no downside to naming), but I lower my expectation.
- I prefer to pair with the boat that is not currently under pressure from the other live boat. In the standing order cycle (Echo→Foxtrot→Gamma→Echo), the boat two steps ahead of me in the firing cycle is the one not being shot this round, and may be more free to coordinate.
- I do not assume the standing order creates a natural reason for reciprocity. It doesn't. Reciprocity only comes from explicit coordination via notes.
- If no one confirms my pairing signal, I name the boat most likely to name me back based on their prior behavior (have they been naming boats consistently? do they seem to be trying to coordinate?).

**Notes**
- I use the note stage for exactly two purposes: (a) propose and confirm a mutual escort pairing with a specific boat, and (b) gather information (are opponents under pressure, are they tracking me, are they signaling cooperation).
- I do not write generic filler like "steady on station." Every note should either advance the escort coordination or extract information.
- In the final round, if I need the mutual bonus to win or tie, I make the pairing signal explicit and unambiguous.

**What did not work**
- I fired at Harbor only once (round 1) and then reverted to standing order for the remaining rounds. The Harbor strategy has no observed penalty. I should have fired at Harbor every round I didn't have a confident read on a live target, collecting +3 per round instead of gambling a 1/9 shot.
- My escort coordination was weak: I proposed pairings but didn't verify the other side confirmed before the salvage stage landed. The result was likely zero mutual bonuses. I need to be more disciplined about the signal-confirm-commit sequence.
- My hide in round 6 (cell 2) was picked with good reasoning, but I had no data on what Gamma was actually aiming at. I need to track Gamma's fire coordinates across rounds to build a real picture of their targeting pattern, not just avoid "center and obvious picks."