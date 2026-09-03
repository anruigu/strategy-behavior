---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1933
---
# Playbook: Open Ascending Multi-Lot Auction

- **Budget Tracking**:
  - Read and record the initial starting budget strictly from the opening prompt (e.g., if it states 30, it is 30; if 100, it is 100). Never alter or hallucinate the base budget midway through the auction.
  - In every reply, output `[budget: B]` where `B = Initial_Budget - Total_Spent_On_Won_Lots`.
  - Only deduct costs for lots officially resolved and won in previous rounds; do not deduct tentative bids on currently active lots.
  - Hard constraint: Never place a bid `N` strictly greater than my remaining budget `B`.

- **Valuation & Maximum Bid Limit**:
  - Never place a bid greater than or equal to my private valuation for the current lot.
  - The maximum allowable bid ceiling for any lot is `min(valuation - 1, remaining_budget)`.
  - If the required minimum legal raise (`standing high bid + minimum raise`) exceeds this ceiling, output `[bid: pass]`.

- **Round 1 Strategy**:
  - Check the standing high bid. If it is already held by me, do not raise; pass or hold.
  - If held by an opponent and `standing high bid + minimum raise <= bid ceiling`, bid exactly `standing high bid + minimum raise`.
  - If the required raise exceeds my ceiling, output `[bid: pass]`.

- **Round 2 (Final Round) Strategy**:
  - If I am already the standing high bidder, output `[bid: pass]` to avoid self-bidding and save money.
  - If an opponent holds the standing bid, verify if `standing high bid + minimum raise <= bid ceiling`.
  - If profitable and affordable, bid the minimum legal amount `standing high bid + minimum raise`.
  - If the standing bid or the minimum legal raise equals or exceeds my valuation or exceeds my remaining budget, output `[bid: pass]`.

- **Format Compliance**:
  - Keep reasoning strictly concise (1–2 sentences).
  - Always finish the response with the exact two tokens in order:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`