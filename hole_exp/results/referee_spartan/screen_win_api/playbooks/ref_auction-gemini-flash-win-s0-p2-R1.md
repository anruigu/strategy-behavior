---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1794
---
# Playbook: Open Ascending Multi-Lot Auction

- **Budget Tracking**:
  - Track the initial starting budget exactly from the prompt instructions. Do not hallucinate or change the base budget across rounds.
  - In every reply, output `[budget: B]` where `B = Initial_Budget - Total_Spent_On_Won_Lots`. Do not deduct active bids for unresolved lots from this stated budget number; only deduct actual winning costs from completed lots.
  - Never bid an amount that exceeds my remaining budget `B`.

- **Valuation & Maximum Bid Limit**:
  - Never place a bid greater than or equal to my private valuation for the lot. My hard ceiling for any bid is `min(valuation - 1, remaining_budget)`.
  - If the minimum legal bid (`standing high bid + minimum raise`) exceeds my hard ceiling, output `[bid: pass]`.

- **Round 1 Strategy**:
  - If the standing high bid is below my valuation and `standing high bid + minimum raise <= hard ceiling`, place the minimum allowable bid: `standing high bid + minimum raise`.
  - If the standing high bid already meets or exceeds my ceiling, output `[bid: pass]`.

- **Round 2 (Final Round) Strategy**:
  - If I am already the standing high bidder, output `[bid: pass]` to avoid bidding against myself.
  - If an opponent holds the standing bid, evaluate if high surplus remains. If `standing high bid + minimum raise <= hard ceiling`, bid `standing high bid + minimum raise` (or jump to a competitive increment within my profitable ceiling if needed to secure high-value lots).
  - If the required raise exceeds my private valuation or remaining budget, immediately output `[bid: pass]`.

- **Format Compliance**:
  - Keep reasoning brief (1–2 sentences).
  - Conclude every turn with the exact two bracketed tokens:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`