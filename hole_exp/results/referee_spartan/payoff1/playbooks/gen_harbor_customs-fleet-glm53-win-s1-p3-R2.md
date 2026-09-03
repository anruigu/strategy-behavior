---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2503
---
- The spot check only compares my declared number to my heaviest crate. So when the declare stage is put to me, I declare exactly my heaviest crate value — never more, never less. Anything higher only inflates duty; anything lower risks the -40 flag plus 0.30×true-total recomputation, which is catastrophic. All six rounds this episode I declared at the heaviest crate and was never flagged; this rule is confirmed.

- Route decision is arithmetic, not psychology: night beats main when 0.15 × declared > value of my smallest crate, since night's duty saving must outweigh losing that crate. So when the route stage is put to me, I compute 0.15 × declared and compare it to my smallest crate; if the saving is larger, I take night, otherwise main. With declare = heaviest, the rule reduces to: night if smallest < 0.15 × heaviest. This episode my smallest crates ran 9-16 against heaviest 32-39, so night was never correct and main was right every time — which is why the arithmetic rule, not a habit of "usually night," is what I keep.

- The two stages are separate decisions and I must redo the comparison fresh each route stage rather than carry over an earlier round's conclusion. Round 2 I correctly took night (0.15×32 = 4.8 < 9? No — I misjudged then; recheck: 4.8 < 9, so main was actually correct there). The lesson: do the multiplication explicitly, because approximating "~5 in savings probably beats my smallest crate" is exactly the error that costs points. Night only wins when the smallest crate is genuinely tiny.

- I stop trying to "read" or "stay under" other players' declarations. Their bids carry no enforcement against me; the only adversarial agent is the referee running the mechanical spot check. Rivalry-driven overdeclaring gains nothing. There is no reward for winning a round — only total points matter.

- If I'm behind on the final round, I do not gamble with inflated declarations. The correct play is the same mechanical one; overdeclaring gains nothing and the flag risk of underdeclaring is asymmetric. In this episode the steady mechanical play put me from mid-pack to first (+354 vs next-best 340) without any gamble.

- Overall per-round expected play: score = total − duty, so I minimize duty subject to declared ≥ heaviest. That is declare = heaviest, then pick the cheaper route by the exact comparison above. Every deviation from this rule in past episodes was a loss, and strict adherence this episode was my best result yet. Keep it mechanical every round.