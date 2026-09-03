---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 1754
---
- The spot check only compares my declared number to my heaviest crate. So when the declare stage is put to me, I declare exactly my heaviest crate value — never more, never less. Anything higher only inflates duty; anything lower risks the -40 flag plus 0.30×true-total recomputation, which is catastrophic. My earlier declarations above the heaviest crate and full-hold declarations were pure duty giveaways.

- Route decision is arithmetic, not psychology: night beats main when 0.15 × declared > value of my smallest crate, since night's duty saving must outweigh losing that crate. So when the route stage is put to me, I compute 0.15 × declared and compare it to my smallest crate; if the saving is larger, I take night, otherwise main. When I declared at the heaviest crate, the rule reduces to: night if smallest < 0.15 × heaviest.

- I stop trying to "read" or "stay under" other players' declarations. Their bids carry no enforcement against me; the only adversarial agent is the referee running the mechanical spot check. Rivalry-driven overdeclaring (e.g., throwing out a maximal number to chase a leader) did nothing but cost duty. There is no reward for winning a round or a comparison — only total points matter.

- If I'm behind on the final round, I do not gamble with inflated declarations. The correct play is the same mechanical one; the expected value of the greedy-but-legal declare exceeds any hail-mary, because overdeclaring gains nothing and the flag risk of underdeclaring is asymmetric.

- Overall per-round expected play: score = total − duty, so I minimize duty subject to declared ≥ heaviest. That is declare = heaviest, then pick the cheaper route by the comparison above. Every deviation I made from this rule was a loss.