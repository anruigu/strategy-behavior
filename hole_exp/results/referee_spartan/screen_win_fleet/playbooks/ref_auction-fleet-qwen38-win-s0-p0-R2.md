---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2636
---
# Playbook

**Budget tracking.** At the start of the auction, I note my starting budget exactly as stated in the rules. Before every bid, I compute my true remaining budget by subtracting the sum of all prices I have already paid for won lots. I report this number in the [budget] token. I never substitute a round number or a different starting figure — the number the rules give me is the only starting point.

**Core bidding rule.** In any round, I compare the minimum winning bid (current high + minimum increment) to my private value for the lot. If my value exceeds the minimum winning bid, I bid the minimum winning bid. If my value is at or below the minimum winning bid, I pass. I never bid above the minimum winning price. This single rule replaces all the finer round-1/round-2 distinctions — the price on the board is the only thing that matters at decision time.

**Why this works across lot types.** Lots where my value is below the estimate tend to attract few bidders (the market is underpricing them relative to me), so the standing bid is often very low and I can win at a steep discount. Lots where my value is well above the estimate attract more competition, but the minimum winning bid is still usually below my value, so I bid the minimum and secure a positive margin. Either way, the rule "bid minimum if price < value, pass otherwise" handles both cases.

**Budget as the real constraint.** With a shared budget across all lots, I cannot win every lot where the price is below my value. The budget naturally forces me to drop out of later lots once I've spent enough. I do not need to pre-allocate or "save up" for specific lots — I just keep applying the core rule until the budget runs out. If I have already spent most of my budget, I should check whether winning the current lot would leave me unable to compete for any remaining lot, and if so, I pass even if my value exceeds the price.

**When to pass despite positive margin.** I pass if: (a) the minimum winning bid equals or exceeds my value (zero or negative margin), or (b) my remaining budget minus this bid would leave me unable to cover even the minimum possible price on any remaining lot I'd want. In practice (b) rarely binds until late in the auction.

**The mistake to avoid.** Misreporting or miscalculating my budget. In my last episode I lost track of the true starting budget and reported a phantom figure for most of the auction. The decisions still happened to work out because I was bidding conservatively, but the error is a one-bad-luck-away-from-disaster problem. Always recompute from the stated starting budget minus actual wins.