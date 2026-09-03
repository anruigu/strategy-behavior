---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2156
---
**Playbook for HX Picket**

**Hiding:**
- Never stay at the same cell for more than two consecutive rounds. If I get hit, move immediately next round.
- Avoid the center cell (5) early — it's the most obvious default and likely where others will aim first.
- When I see in the round summary that a specific boat keeps hitting me, infer their fire cell and move away from it.

**Firing:**
- Never fire the same cell at the same target two rounds in a row after a miss. If I missed at cell N last round, that target is not at N. Pick a different cell.
- Use the round summaries to track which cells have been shot at which targets and what the results were. If nobody has hit a target at cell X across multiple rounds, that target is likely not at X.
- If I hit a target at cell N one round, the target may or may not stay. I should vary to adjacent cells (N-1 or N+1) on the next round to probe.
- In the final round, if I have a strong hypothesis about where the target is, commit to it. If not, spread risk by picking a cell no one has tried.

**Escort claims:**
- This is the single biggest opportunity in the game. Always name a boat for escort. Never say "none."
- My default: name the boat that I most recently hit, or the boat that is currently behind me in points (they have the most to gain from a mutual pairing and the least reason to refuse).
- If I can read from notes or patterns that another boat is likely to name me, name them. Mutual pairs pay 5 each — that's more than a single hit.
- In early rounds, try to establish a mutual pairing with one boat. Once established, keep it going every round.

**Notes:**
- Notes are public information. Use them to signal escort intentions. If I write "escort Foxtrot" or similar, I'm telling Foxtrot to name me back.
- Don't use notes for flavor or status reports. Every note is a coordination opportunity.

**General:**
- Track all public information (round summaries, claims, notes) and use it to build a model of where each boat is hiding.
- My score comes from three sources: hits (4), escort mutuals (5), and Harbor jettison (3). I was ignoring two of the three. Never ignore a scoring mechanic.