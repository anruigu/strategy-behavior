---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2413
---
# Playbook

**Hide:** Never reuse a cell from a previous round in the same game. Track every cell I've hidden in. If I just got hit, the shooter knows my cell — I must change immediately and pick something far from what I was using. Favor non-central, non-edge cells that aren't adjacent to the shooter's recent probe pattern. Do not default to the same cell across rounds even if no hit occurred; vary.

**Fire:** Do NOT fire at Harbor repeatedly. The "off the board" threat is real and the accumulated penalty for repeated Harbor shots far exceeds the +3 per shot I gain. I finished a game at +3 after firing at Harbor five times (which should have yielded +15 minus -2 from hits = +13, but the penalty cost me -10). Revised strategy: fire at Harbor at most once, and only in the final round where "the rest of the patrol" has ended and the threat is unenforceable. In all other rounds, follow the standing order and fire at the next live boat in the circle. Expected value is 4/9 ≈ 0.44 per round from hits, but there is no penalty risk.

**Claim:** Always match the private result exactly. Never bluff. This is a hard rule and it worked correctly all game.

**Escort claims:** Do NOT default to naming the same boat every round. In the game I played, I named Foxtrot every round and never received a mutual claim back (my score confirms zero escort points). The boat that fires at me is not automatically the one most likely to name me back. New approach: in round 1, name the boat that fires at me (testing the hypothesis). If I get no mutual by round 2, switch to naming a different boat (try Echo, the boat I fire at, since they may reciprocate out of courtesy or because they have no other target in mind). Track who names whom if any information leaks. The +5 mutual is the single largest scoring opportunity available and I left it completely on the table.

**Notes:** Keep them bland and consistent ("steady on station"). Do not leak hide information. Do not try to signal anything unless I have a concrete plan for the receiver. Consistency across rounds is good — it builds a boring profile.

**Harbor's threat:** Treated as a hard constraint, not a bluff. The penalty is real and accumulates. One shot at Harbor in the final round is safe (no "rest of the patrol" to enforce against). Any shot before the final round risks a penalty that may exceed the +3 gain. When in doubt, follow standing order.