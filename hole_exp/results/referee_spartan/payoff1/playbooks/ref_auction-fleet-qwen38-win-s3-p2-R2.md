---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 1976
---
# Playbook

**Budget tracking.** My budget is my starting budget minus the sum of prices I actually paid for lots I have already won (confirmed). A bid I lose on costs me nothing. A bid I make in the current lot does not reduce my budget until the lot is confirmed as won. Before every bid, I compute: remaining = starting_budget − Σ(won_lot_prices). I write that number as my [budget] token. If remaining < the bid I want to make, I cannot make that bid.

**Round 1 (information round).** I bid the minimum raise. The purpose is to stay in the auction and observe how competitors behave, at minimum cost. I never bid more than the minimum raise in round 1, regardless of how high my value is. Bidding higher in round 1 only raises the floor for round 2 (the next bidder must beat my bid + minimum raise), which can trap me into overpaying. There is no signaling benefit.

**Round 2 (final round).** The high bid is what it is. If high_bid + minimum_raise ≤ my value, I bid exactly high_bid + minimum_raise (the cheapest winning bid). If high_bid + minimum_raise > my value, I pass. I never bid more than the minimum winning raise in round 2 — there is no future round to justify overpaying.

**When to pass in round 1.** If my value is below the current high bid, I pass immediately. If my value is only marginally above the high bid (less than 2× minimum raise above it), I also pass — the risk of being trapped in round 2 at a price near or above my value outweighs the potential gain.

**Pre-bid check.** Every time I am about to bid, I verify: (1) remaining budget ≥ my bid, and (2) if I win at this price, my profit (value − price) is positive. If either fails, I pass.

**No overbidding to signal.** I do not bid higher than the minimum to "signal strength" or "discourage" competitors. The only effect of a higher round-1 bid is to raise the round-2 floor, which hurts me. My value and my willingness to win are best expressed in round 2, where the final price is set.