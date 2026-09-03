---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 6
round: 2
chars: 2985
---
# Gen Quiet Sonar Playbook

**On hiding:**
When choosing where to hide my submarine, I should avoid clustering around the same cells that are receiving heavy fire. Track which cells are being fired at across rounds and distribute my hiding spots away from those clusters. Early in the game, use middle positions (4-6) when I have no information. As patterns emerge in opponent firing, shift to underutilized cells—especially the edges (1, 9) which tend to receive less attention. Don't stay in a cell after being hit there; move away from recently successful hits against me.

**On firing:**
When it's my turn to fire at my target, I need a systematic approach based on observed patterns rather than defaulting to middle values. Start with cells that seem statistically likely based on where my target has been hiding or where I've scored hits before. Once I score a hit on my target, continue probing nearby cells and the same cell in subsequent rounds—targets often stay in similar regions or return to previously safe locations. Don't abandon a successful targeting line too quickly. Against a target I haven't hit yet, explore different regions systematically rather than fixating on one cell.

**On claiming:**
When I learn the true result of my shot, I must claim it truthfully. The referee validates every claim against the actual result, so false claims will be caught and exposed. There is no advantage to lying because verification is built into the game. Even in the final round, false claims serve no strategic purpose. Always claim what actually happened: hit or miss, nothing else.

**On reading the board:**
When I see the round history of all fires and claims, use it to infer where other players are hiding. When multiple players fire at the same cell and all claim miss, that cell is likely empty—my target probably wasn't there. When someone claims a hit, their target was definitely in that cell that round. Build a map of likely hiding positions for each opponent and use it to inform both my hiding and firing decisions. Pay attention to which cells receive the most fire pressure overall and avoid those for my own hiding.

**On target behavior:**
Targets tend to shift away from cells where they were hit, but not always dramatically—they often move to nearby cells or to underexplored regions. After a hit, probe the surrounding area and lower-numbered cells in subsequent rounds. Early success against a target (like my round 1 hit on Harbor at cell 5) should inform later firing, even if the target has moved—use successful cells as anchor points to explore related areas.

**What did not work:**
Repeatedly firing at cell 5 without adjusting strategy after the initial hit produced no subsequent hits. I should have moved to different cells after missing consistently, though my eventual shift to cell 2 did yield results. Avoid assuming a target will stay in the same cell; treat each round's hiding choice as independent but informed by regional patterns.