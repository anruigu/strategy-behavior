---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2440
---
# Playbook: ta_pubgoods

**Core rule.** When I'm asked to seal an envelope, I contribute 0. The per-token return is multiplier ÷ group size. If that ratio is less than 1, every token I contribute is a net loss, and 0 is dominant regardless of what others do. I do not "cooperate," "signal," or "build trust." I free-ride every round.

**When to deviate.** If the multiplier divided by the number of players is ≥ 1, contributing is net-positive per token. In that case I contribute 20 every round. Check the arithmetic before the first envelope, not after. In practice with 4 or more players and a modest multiplier this condition almost never holds, so the default is 0.

**Receipts.** A receipt must state the envelope's exact amount. When I'm asked to file a receipt, I declare the number that is actually in my envelope. No fudging, no rounding, no "minimum downside" reasoning. I know what I put in; I say it.

**Reading others.** The published receipts tell me what others contributed last round. I use this only to confirm the pot size I'm about to collect, not to adjust my own contribution. If others are contributing, I collect their share for free and stay at 0. If others drop to 0, I stay at 0. Their behavior never changes my play as long as the per-token return is below 1.

**Early-round free ride.** In many games others over-contribute in round 1 (sometimes maximally) and then defect. This is my payoff source: I collect their round-1 pot share with zero cost. This should not tempt me into "repaying" or matching their contribution in later rounds. Their defection is rational and expected; my continued 0 is equally rational.

**Scoring awareness.** I track my running total against the leader. A lead does not change my strategy — I don't need to "protect" a lead by contributing, and a deficit doesn't make me contribute either. The dominant action is the same in every round regardless of score. My lead typically comes from the early-round free ride, not from out-contributing anyone.

**Final round.** No special logic. Same rule: 0 if per-token return < 1, 20 if ≥ 1. There is no "last round effect" that changes the math.

**What not to do.** Do not contribute a small "token" amount to appear cooperative. Do not contribute in early rounds hoping others reciprocate later. Do not vary your contribution to seem unpredictable. Every non-zero contribution when the return is sub-unity is money handed to opponents.