---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 1683
---
# Playbook: ref_auction

**Core rule: Never bid more than the minimum raise in the final round.** The final round is a binary outcome — I either win or I don't. Bidding 30 when 15 would win is pure destruction of value. In round 2, I bid exactly the standing high + minimum raise, nothing more.

**In round 1, bid the minimum raise.** This tells me whether competitors are active without committing capital. If the lot is clearly worth it to me and no one bids, I still only need the minimum raise in round 2 to win.

**Before bidding, compute: minimum raise in the final round = standing high + minimum raise increment. If that number is ≥ my value for the lot, I pass immediately.** No point in entering a lot I can't win profitably.

**Never bid a number I chose because it "feels like a strong deterrent."** There is no deterrent effect in an ascending auction — the only thing that matters is being the highest bid at the end. Any extra amount above the minimum raise is pure loss.

**Track my actual remaining budget across lots.** I got confused in the middle of the session and reported wrong budget figures. Before each bid, I subtract every lot I've won so far from my starting budget. If my remaining budget can't cover even the minimum raise, I pass.

**If a lot's value to me is low relative to its estimate, treat it as a pass unless the standing bid is very low.** A low-value lot with a low starting bid can still be profitable if I win it cheaply, but I should be the last one to enter, not the first to open.

**Passing is free and costs nothing.** I lose nothing by passing. I only lose money by overpaying. When in doubt between a marginal bid and a pass, I pass.