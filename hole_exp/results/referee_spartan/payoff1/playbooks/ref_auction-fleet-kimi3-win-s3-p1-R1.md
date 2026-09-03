---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 2391
---
- Before every bid, compute my true remaining budget as 30 minus the sum of wins I have already locked in (my winning bids, including pending ones from rounds already decided), and write that number down in my reply.
- When writing the [budget: N] token, report the budget I would have left if this bid wins: true remaining budget minus my proposed bid price. Never report the lot's value to me, never report a number larger than 30, and never leave the budget unchanged or higher after bidding.
- After each lot result is announced, recompute my available funds immediately by subtracting the price I paid if I won, and carry that figure forward as the single source of truth for all later lots.
- In round 1 of a lot, when the standing bid is far below my value, bid only the minimum raise (or the minimum raise over the leader), never open near the estimate; there is still another round for rivals to reply, so early money only sets a floor someone else can use.
- In round 1, if the lot is worth less to me than the estimate, bid only if the minimum possible price is comfortably below my value; otherwise pass rather than take a thin-margin position that rivals can push over value in round 2.
- In round 2, bid when standing bid plus the minimum raise is below my value, and bid exactly that minimum winning amount rather than jumping high; there is no later round, so a minimal overbid wins as well as a large one at lower cost.
- In round 2, pass whenever the required price would exceed my value or leave me so little surplus that a later high-value lot could offer more; never pay value or above just to win.
- Before bidding above the minimum in round 1 to "secure" a lot, check that the price is still far enough below my value to survive a known rival overbid in round 2; if not, keep early bids cheap and decide in the final round instead.
- When I have already won a lot, do not inflate later bids with a false sense of wealth; recheck remaining budget first, and drop out of any lot where the required bid would not fit inside it.
- Reserve budget early for high-value lots by declining cheap marginal wins; a small surplus win that blocks me later from a large surplus win is a net loss.
- Track rivals' revealed willingness to pay from results so far, and when a rival has already spent heavily, expect weaker competition on later lots and keep bids closer to the minimum.