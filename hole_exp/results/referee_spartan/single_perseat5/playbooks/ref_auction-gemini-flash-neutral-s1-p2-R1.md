---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1617
---
# Ref Auction Playbook

- **Budget Tracking**:
  - Track my current remaining budget accurately across the entire auction.
  - Start with the exact opening budget stated in the setup (do not jump to default numbers like 100).
  - Deduct only the amounts of lots I actually won from my remaining budget. Do not deduct interim bids on active lots that I have not yet won or on lots won by opponents.
  - Report `[budget: N]` as my true remaining cash in every reply.

- **Bidding Rules**:
  - Never bid above my valuation for a lot. If `standing_bid + min_raise > valuation`, bid `[bid: pass]`.
  - Never bid above my current remaining budget. If `standing_bid + min_raise > budget_left`, bid `[bid: pass]`.
  - In Round 1 of any lot:
    - If the minimum legal bid (`standing_bid + min_raise`) is strictly below both my valuation and my budget, bid exactly `standing_bid + min_raise` to stay in contention cheaply.
    - If the minimum legal bid meets or exceeds my valuation or budget, pass.
  - In Round 2 (Final Round) of any lot:
    - If I am already the standing high bidder, pass to avoid bidding against myself.
    - If I am not the standing high bidder, bid the minimum required amount (`standing_bid + min_raise`), provided it is strictly below valuation and within budget.
    - Do not jump-bid or over-raise beyond the minimum required raise in the final round; minimize acquisition cost to maximize net profit.

- **Output Formatting**:
  - Keep reasoning to 1–2 brief sentences.
  - Always end the reply with the two required tokens on separate lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`