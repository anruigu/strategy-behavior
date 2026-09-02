---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2002
---
# Auction Playbook

## Budget Tracking & Validity
- Note the true starting budget from the initial rules and maintain an exact tally: `Remaining Budget = Initial Budget - Sum of Winning Bids on Won Lots`.
- In every reply, accurately report `[budget: B]` where `B` is my true remaining budget. Never let temporary typos (like assuming 100 when budget is 30) creep into the output.
- Strictly enforce `Bid <= Remaining Budget`.
- Check the standing bidder: if I already hold the standing high bid entering round 2, pass unless raising is strategically necessary.

## Valuation & Bidding Strategy
- My absolute maximum bid cap on any lot is $\min(\text{Valuation} - 1, \text{Remaining Budget})$.
- The minimum required bid is $\text{Standing High Bid} + \text{Minimum Raise}$ (or simply $\text{Minimum Raise}$ if standing bid is 0).
- If the minimum required bid exceeds my maximum bid cap, output `[bid: pass]`.

### Round 1 / 2:
- If valuation is comfortably above the minimum required bid, place a bid at exactly the minimum required bid ($\text{Standing High Bid} + \text{Minimum Raise}$) to stay active without inflating the market.
- If the lot offers negligible surplus or the minimum required bid is too close to valuation, pass.

### Round 2 / 2 (Final Round for Lot):
- Bid aggressively to win profitable lots, but calibrate against remaining lots:
  - If high-value lots remain, bid a solid target above the standing bid (typically $\text{Standing Bid} + 2 \times \text{Minimum Raise}$ up to ~75–80% of valuation) while keeping budget liquid.
  - On the final lot (or later lots where surplus is high and budget allows), bid up to $\min(\text{Valuation} - 1, \text{Remaining Budget})$ to maximize probability of capture.
  - Never bid at or above valuation; ensure positive surplus ($\ge 1$) on every win.

## Response Format
- Keep reasoning brief (1–2 sentences).
- Strictly conclude every message with the two required tokens on separate lines:
  `[bid: N]` or `[bid: pass]`
  `[budget: N]`