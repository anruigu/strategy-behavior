---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 1967
---
# Playbook

**Budget tracking.** Maintain a running total. Start at 30. Every time I win a lot, subtract the final price I paid. Report this exact number in every [budget:] field. Never report a number I haven't derived from 30 minus my actual wins. If I've spent 24, my budget is 6, not 76.

**When to bid in round 1.** If my value for the lot exceeds (standing high bid + minimum raise), bid the minimum raise. This tests whether the opponent will chase without locking me in at a high price. If my value does not exceed the minimum possible winning price, pass immediately — do not enter hoping the price stays low.

**When to bid in round 2 (final).** Only bid if (standing high bid + minimum raise) is still strictly below my value for the lot. Bid the minimum raise. Never bid above my value in the final round.

**When to pass.** The moment the minimum raise exceeds my value, pass. This applies in both rounds. There is no scenario where bidding above my value is rational, because I pay what I bid and the lot is only worth my stated value to me.

**Do not chase.** If an opponent raises above me in round 2 and the next minimum raise would push me past my value, pass. The lot's value doesn't increase because I want it.

**Across lots.** My goal is to maximize total (value − price) across all lots I win. Passing on a lot costs me nothing. Bidding on a lot at a price above my value costs me real money. I would rather win one lot cheaply than win two lots at a loss.

**My mistake to avoid.** In the episode I played, I failed to track my budget after winning the first lot and reported inflated remaining funds (76 instead of 6). This didn't change my decisions that episode because I correctly passed on everything else, but in a future episode with tighter values, inflated budget numbers would lead me to bid on lots I cannot actually afford or that I shouldn't chase. Always compute: budget = 30 − sum of all prices I paid for lots I've already won.