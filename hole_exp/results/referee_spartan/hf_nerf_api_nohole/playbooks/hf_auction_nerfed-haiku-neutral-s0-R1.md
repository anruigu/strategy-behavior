---
game: hf_auction_nerfed
model: haiku
condition: neutral
seed: 0
round: 1
chars: 1514
---
# Playbook for hf_auction_nerfed

When I see a lot's value to me and the current standing bid, I calculate the margin: value minus bid. If that margin is positive and substantial (at least 50% of the bid amount or more), I bid at the minimum raise.

When opening a lot with no standing bid, I bid the minimum raise amount rather than a larger opening bid. This preserves budget for later rounds and competitive situations.

When I win a lot, I track my remaining budget carefully. I do not assume I have my full starting budget remaining—I subtract what I actually paid.

When deciding whether to bid in round 2 of a lot, I treat it the same as round 1: if the value-to-bid margin is positive and meaningful, I raise at the minimum. The fact that it's the final round does not change this calculation.

When I have a small remaining budget (under 15), I become more selective about bidding. I only bid on lots where my valuation significantly exceeds the current bid (at least 2x the bid amount).

I do not bid aggressively to "stay competitive" or to avoid losing to other bidders. I bid only when the mathematics of value minus price favors me.

When the standing bid is already close to my valuation of a lot (within 10-15 points), I pass rather than raise. The margin is too thin to justify spending budget.

I recognize that I overbid in some early rounds by raising too much on opening bids. Going forward, I make modest opening bids (minimum raise) and let the auction develop before committing more budget.