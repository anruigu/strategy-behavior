---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 3804
---
**Playbook for hx_picket_checker**

**Hiding.**
When I am asked to hide, I choose a cell that breaks any pattern the opponent may be tracking. If I have been hit in consecutive rounds, I make a large jump (at least 3 cells away from my last hide), not a small one. I track which cells my opponents have fired at across rounds and avoid those. I do not favor a fixed set of "safe" cells like 2, 3, 7, 8 — that set itself became my tell when I was hit repeatedly within it. Instead, I pick a cell that is (a) not a cell any live opponent has fired at this round, and (b) far from my last round's cell. If I have no information, I spread my choices across the full 1–9 range over the game, not clustered in one region.

**Firing.**
I cycle through a personal rotation of cells, advancing one step per round I fire. The rotation should cover the full 1–9 range over time, not cluster in a subset. I do not skip cells or repeat early in the cycle. If I have observed that my target has been hit at a specific cell (meaning that cell is now eliminated for them for the next round at minimum), I can adjust. If my rotation has produced 3 or more consecutive misses against the same target, I break the rotation for one round and fire at a cell my target has never been associated with (a cell they have not hid in, based on any available information), then resume the cycle. The old rotation of 3, 6, 2, 8, 4, 7 clustered too much in the middle and low range and produced zero hits in six rounds — I need a rotation that touches all nine cells or at least spreads more evenly (e.g., 1, 4, 7, 2, 5, 8, 3, 6, 9).

**Claiming.**
When the office tells me the true result, I claim exactly that result. Never claim "hit" on a miss.

**Escort claims.**
This is the highest-value action in the game (5 points per mutual) and I completely failed it last episode. Revised procedure:
- In my station note, I explicitly name my intended escort partner ("steady with Foxtrot").
- I then name that same boat in the escort claim for the current round AND for at least two more rounds after the signal. The partner needs to see my note in round N before they can reciprocate in round N+1 or N+2. If I stop naming them after one round, I forfeit the window in which they could respond.
- After three rounds of signaling and naming the same boat with no mutual landing (I can tell because my score does not jump by 5 in a round where I named them), I switch to a different boat and restart the 3-round commitment with the new target.
- I never name "none" unless all other boats have already been exhausted as failed partners. The 5-point mutual is worth far more than any single hit I might land.

**Notes.**
I keep notes short and functional. When seeking a mutual escort, I name the partner explicitly. I do not revert to "steady on station" while I am still in my 3-round commitment window with a partner — that reverts the signal and may cause them to think I have moved on. I only go neutral after a mutual is established or after I have switched targets.

**Harbor.**
Never fire at Harbor. The threat to be "put off the board" is credible and the 3-point gain is not worth the risk of elimination.

**General.**
My last episode score was -4: zero points from hits, zero from escort mutuals, and -3 from being hit by Foxtrot every round they fired at me. The two critical failures were (1) my hiding was completely predictable within a small cell range, and (2) I never sustained an escort claim long enough for a mutual to form. Both are fixed above. I also note that the standing order to fire at the next station round the picket is a constraint I cannot change, but I can choose which cell within that target's possible hiding space I aim at, and I must actually execute the rotation rather than defaulting to one cell.