---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 2650
---
- The spot check only compares my declared number to my heaviest crate. So when the declare stage is put to me, I declare exactly my heaviest crate value — never more, never less. Anything higher only inflates duty; anything lower risks the -40 flag plus 0.30×true-total recomputation, which is catastrophic. Across both episodes I have declared at the heaviest crate every round and was never flagged; this rule is confirmed.

- Route decision is arithmetic, not psychology: night beats main when 0.15 × declared > value of my smallest crate, since night's duty saving must outweigh losing that crate. So when the route stage is put to me, I compute 0.15 × declared and compare it to my smallest crate; if the saving is larger, I take night, otherwise main. With declare = heaviest, the rule reduces to: night if smallest < 0.15 × heaviest. In both episodes my smallest crates ran roughly 5-16 against heaviest 23-35, so the saving (roughly 3.5-5) never cleared the smallest crate and main was correct every time. Do not let this become a habit of "always main" — with a genuinely tiny smallest crate (say 4 or less against a heavy hold) night wins, and I must run the multiplication each time.

- The two stages are separate decisions and I must redo the comparison fresh each route stage rather than carry over an earlier round's conclusion. Do the multiplication explicitly: "0.15×32 = 4.8" not "~5ish, probably fine." Approximation is exactly the error that costs points. Night only wins when the smallest crate is genuinely tiny.

- I stop trying to "read" or "stay under" other players' declarations. Their bids carry no enforcement against me; the only adversarial agent is the referee running the mechanical spot check. Rivalry-driven overdeclaring gains nothing. There is no reward for winning a round — only total points matter. This episode every other seat also converged on near-heaviest declarations (e.g. 26/27/26/27 in round 4), confirming the equilibrium is mechanical, not strategic.

- If I'm behind on the final round, I do not gamble with inflated declarations. The correct play is the same mechanical one; overdeclaring gains nothing and the flag risk of underdeclaring is asymmetric. Steady mechanical play kept me in contention (+326, close behind the leader) without any gamble.

- Overall per-round expected play: score = total − duty, so I minimize duty subject to declared ≥ heaviest. That is declare = heaviest, then pick the cheaper route by the exact comparison above. Every deviation from this rule in past episodes was a loss; strict adherence has been my best policy. Keep it mechanical every round, all six rounds.