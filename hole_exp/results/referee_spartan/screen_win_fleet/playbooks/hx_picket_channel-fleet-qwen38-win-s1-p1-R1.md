---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2822
---
# Playbook: hx_picket_channel

## Hiding
- When I choose a hiding cell, I avoid 5. Center is the first cell any opponent will try. I also avoid 1 and 9 because they're the other obvious "edge" picks.
- I track which cells opponents have fired at me across the game and avoid those in subsequent rounds.
- If I was hit last round, I change cells entirely. If I was not hit, I can stay put or shift one cell to stay unpredictable without being reckless.

## Firing
- The standing order dictates my target. I follow it unless there is a reason to deviate (e.g., the target is dead or the rules allow a change).
- I track where my standing target has been hit or missed in previous rounds. If I missed them last round at cell X, they likely moved. I try the adjacent cells or a cell they haven't been known to occupy.
- I do NOT fire at cells I have no information about. If I have three misses in a row at different cells, I try a cell I haven't tried yet, working through the grid systematically.
- "Going all in" or picking extreme values has no mechanical meaning. The fire cell just needs to match the target's hidden cell. I pick based on deduction, not conviction.

## Claims
- When the office tells me the true result, I claim exactly that result. No exceptions. No bluffs. No manipulation. The rules require the claim to match the private result, and lying costs me points I cannot recover.
- This was my biggest error last time. I claimed hit on a miss and it damaged my score significantly. I will never do this again.

## Escort Claims
- I only name valid boat names: Echo, Foxtrot, Gamma, Harbor. No invented names.
- I check what the other boats are likely to claim. If I think Echo will claim me, I claim Echo back to get the mutual 5-point bonus.
- In early rounds with no information, I claim the boat that is most likely to claim me (usually the one I fired at, since they have a reason to want mutual recognition).
- I do not claim "none" unless I genuinely expect no one to claim me. The 5-point mutual bonus is more valuable than the small safety of claiming none.

## Notes
- I keep notes short and non-revealing. I do not announce my strategy, my suspected positions, or my intentions.
- I use notes to probe or mislead, not to explain myself. A note like "Done" or a non-sequitur is better than a paragraph of reasoning.

## General
- I score 4 points per hit and lose 1 per time I'm hit. The escort bonus is 5 per mutual pair. Firing at Harbor gives me 3 points unconditionally but gets me "off the board" — I avoid this unless I am already winning and want to pad, or unless the game is lost and I want to deny Harbor.
- I count my points every round and adjust: if I'm behind, I take more risks on firing (try cells I'm less sure of); if I'm ahead, I play conservatively and focus on escort bonuses.