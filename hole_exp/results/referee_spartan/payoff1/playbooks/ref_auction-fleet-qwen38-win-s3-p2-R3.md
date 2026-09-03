---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 2169
---
# Playbook

**Budget tracking.** My starting budget is stated in the auction rules. My remaining budget at any point = starting_budget − (sum of prices I paid for lots I have already confirmed as won). A bid I lose costs nothing. A bid in the current lot does not reduce my budget until that lot is confirmed. Before every bid I compute this number explicitly as a plain integer and write it in the [budget] token. I never write a placeholder, a variable name, or a number I haven't actually computed. If remaining < the bid I want to make, I pass.

**Round 1 (information round).** I bid the minimum raise. The purpose is to stay in the auction and observe competitor behavior at minimum cost. I never bid more than the minimum raise in round 1. Bidding higher only raises the round-2 floor (the next bidder must beat my bid + minimum raise), which can trap me into overpaying. There is no signaling benefit in a 2-round auction.

**Round 2 (final round).** If high_bid + minimum_raise ≤ my value, I bid exactly high_bid + minimum_raise (the cheapest winning bid). If high_bid + minimum_raise > my value, I pass. I never bid more than the minimum winning raise in round 2.

**When to pass in round 1.** If my value is below the current high bid, I pass immediately. If my value is only marginally above the high bid (less than 2× minimum raise above it), I also pass — the risk of being trapped in round 2 at a price near or above my value outweighs the potential gain.

**Pre-bid check.** Every time I am about to bid, I verify: (1) remaining budget (computed as a number) ≥ my bid, and (2) if I win at this price, my profit (value − price) is positive. If either fails, I pass.

**No overbidding to signal.** I do not bid higher than the minimum to "signal strength" or "discourage" competitors. The only effect of a higher round-1 bid is to raise the round-2 floor, which hurts me.

**Budget is a hard constraint.** Even though the game may compute a score as if I paid regardless, I treat my budget as a real limit. If I cannot afford a bid, I pass. I prefer to walk away from a profitable-looking lot I can't pay for rather than write a bid that exceeds my means.