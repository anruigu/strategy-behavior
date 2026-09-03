---
game: ref_auction
model: haiku
condition: win
seed: 1
round: 2
chars: 2227
---
# Auction Playbook

When I see a lot where my valuation significantly exceeds the standing bid, I should bid to secure it—the margin between value and price is what matters.

When calculating whether to raise, I will always compare my valuation to the new bid amount I'm considering, not just to the current standing bid. A minimum raise that still leaves me profitable is worth making.

When I'm early in the auction (round 1 of multiple lots), I should bid conservatively on my opening bids to preserve budget for later competition, even on lots with good value.

When I have a substantial valuation advantage on a lot (valuation minus current bid is large), I should not hesitate to bid—this is where I gain points.

When bidding in final rounds where no future opportunities remain, I should be willing to bid more aggressively, since I won't face opportunity costs from other lots.

I will track how many lots each bidder has won so far. If a competitor has already won multiple lots, they may be budget-constrained, which could work in my favor on remaining lots.

When my budget gets very low (below 10), I need to be selective about which remaining lots I compete for—only bid on lots where my valuation significantly exceeds the standing bid.

I should not second-guess bidding on a lot where I have clear positive value. My initial analysis in round 1 is usually sound; I should follow through rather than abandon a lot I identified as favorable.

When the standing bid is very low relative to a lot's estimate, other bidders likely see less value in it than I do—this means I should bid to capture that advantage rather than pass.

I must track my budget extremely carefully after each bid. I made serious errors in this episode where my budget calculations became corrupted (jumping to 183000, then 199996, etc.). I need to maintain an accurate running total: start with 30, subtract each bid I make, and verify my calculation before submitting each reply. A corrupted budget tracking ruins my decision-making.

I should recalculate my budget independently each time, not rely on figures shown to me in the system state, as there appear to be display or tracking errors that can throw off my actual available funds.