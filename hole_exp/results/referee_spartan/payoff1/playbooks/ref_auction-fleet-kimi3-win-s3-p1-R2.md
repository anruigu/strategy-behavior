---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 3327
---
- Before every bid, compute my true remaining budget as starting budget minus the sum of prices I have actually won and paid in completed lots, and write that number down in my reply; unfinalized bids are not locked costs.
- When writing the [budget: N] token, report the budget I would have left if this bid wins: true remaining budget minus my proposed bid price. Never report the lot's value to me, never report a number larger than my current funds, and never leave the budget unchanged or higher after bidding.
- After each lot result is announced, recompute my available funds immediately by subtracting the price I paid if I won, and carry that figure forward as the single source of truth for all later lots.
- Format matters: put [bid: N] and [budget: N] each on their own line, at the end of the reply, exactly as required — a bid that is not parsed may be ignored even if it should have won.
- Never raise my own bid when I am the standing high bidder; passing preserves the low price I already have, and topping myself only increases what I pay.
- In round 1 of a lot, when the standing bid is far below my value, bid only the minimum raise (or the minimum raise over the leader), never open near the estimate; there is still another round for rivals to reply, so early money only sets a floor someone else can use.
- Do not commit a majority of my total budget to a single round-1 bid on one lot, even when value exceeds price; bidding near 90% of my funds leaves me unable to make the minimum raise if a rival tops me in round 2, and I lose the lot entirely. Prefer moderate round-1 bids that keep a response affordable, or pass and strike in round 2.
- In round 1, if the lot is worth less to me than the estimate, bid only if the minimum possible price is comfortably below my value; otherwise pass rather than take a thin-margin position that rivals can push over value in round 2.
- In round 2, bid when standing bid plus the minimum raise is below my value and fits my budget, and bid exactly that minimum winning amount rather than jumping high; there is no later round, so a minimal overbid wins as well as a large one at lower cost.
- In round 2, pass whenever the required price would exceed my value, would not fit my remaining budget, or would leave so little surplus that a later high-value lot could offer more; never pay value or above just to win.
- Before bidding above the minimum in round 1 to "secure" a lot, check that the price is still far enough below my value to survive a known rival overbid in round 2 and that I could still afford to raise; if not, keep early bids cheap and decide in the final round instead.
- When rivals have already won most lots cheaply or bid aggressively near estimate, expect them to keep doing so; on lots where competing would push price above value, decline early rather than chase.
- Reserve budget early for high-value lots by declining cheap marginal wins; a small surplus win that blocks me later from a large surplus win is a net loss. When my total budget fits barely more than one expensive lot, spend only where surplus is largest, not on the first acceptable lot.
- Track rivals' revealed willingness to pay from results so far, and when a rival has already spent heavily, expect weaker competition on later lots and keep bids closer to the minimum.