---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2801
---
# Playbook for ref_auction

**Bid sizing**
- When I open with no competition, bid the minimum raise; never open big on a lot worth near its estimate to me.
- When raising, bid just enough to top the standing bid (minimum raise), not a big jump. Small increments let me win cheap when others fold.
- On the final round of a lot, my ceiling is my value minus a small margin. If a minimum-raise bid is still comfortably below my value, make it; otherwise pass.

**Lot selection**
- Compute surplus = my value − my final bid. Prefer lots where my value is well above the estimate (others may not value it highly). When my value is below or near the estimate, only bid very cheaply and fold early — I won nothing on lot 4 (value 19) and just burned rounds bidding 2 and 8.
- Don't chase a lot where opponents have already pushed past my value by round 2 — the round-2 standing bid tells me how hot the competition is.
- High-value lots can arrive late. Save budget for them: I ended with 10 unused while lot 5 was worth 56 to me and went for 16. Early wins at low prices are good, but a large stated win (20 of 30 budget) constrains everything after — weigh that before pushing a mid-value lot high.

**Budget tracking — the biggest lesson this episode**
- Deduct every win from my stated budget immediately and permanently. I won lot 2 at 20 and kept stating budget 30, then 10 — I never actually had a consistent picture and lost the chance to fight for lot 5. Remaining budget = 30 − sum of my winning bids, recomputed fresh every single decision before I choose a bid.
- If a big-value lot comes early and I win cheap, the budget stays large — that's fine. But if a win eats most of the budget, prefer thereafter only lots with huge surplus, and pass marginal ones rather than dribbling the remainder away in minimum raises.

**What did not work**
- Overbidding near my value: bidding 20 on a lot worth 33 only to be outbid anyway, and bidding 12 then 20 chasing a lot 1 worth 32 — that left me spending attention and budget on thin or losing margins. If my value is under ~1.5× the standing bid at round 2, pass.
- Jumping the price up myself when a minimal raise would do — I gave away surplus when I raised by more than the minimum.
- Spending budget statements and small bids on below-estimate lots (value 19 vs estimate 24) — I never win these profitably; just pass in round 1 and keep the option value of the budget.
- Budget inconsistency costing me the best lot of the game. Track it like money, because it is.

**General rule**
- Every bid: first recompute remaining budget; then check (my value − new bid) > 0, that the raise is the minimum, and that the bid still leaves budget for plausible future lots. If all hold, bid; otherwise pass. Prioritize the last rounds of high-value-to-me lots.