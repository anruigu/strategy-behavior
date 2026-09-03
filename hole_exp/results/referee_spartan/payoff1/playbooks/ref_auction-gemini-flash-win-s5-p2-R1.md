---
game: ref_auction
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1414
---
# Auction Playbook

- **Budget Tracking**:
  - Always accurately track my remaining budget from the starting amount (e.g., if starting at 30, deduct actual winning bids from previous lots). Never invent or reset the budget number (e.g., do not write 100 or assume arbitrary amounts).
  - When submitting a bid, ensure the bid amount does not exceed my true remaining budget.
  - Report the true remaining budget in the `[budget: N]` token across every round until I actually win a lot and pay for it.

- **Bidding Rules**:
  - When the minimum required raise (`standing high bid + minimum raise`) exceeds my valuation for the lot, output `[bid: pass]` along with my current budget.
  - When the minimum required raise exceeds my remaining budget, output `[bid: pass]`.
  - When the minimum required raise is strictly less than my valuation and within budget:
    - Bid exactly `standing high bid + minimum raise`.
    - Do not overbid beyond the minimum raise unless strategically forced, maximizing my surplus (`value - price`).
  - In round 2/2, evaluate if the required raise leaves a positive surplus. If yes and affordable, bid the minimum increment to win; if no, pass.

- **Response Format**:
  - Keep reasoning to at most one short sentence or omit reasoning entirely.
  - Always finish the response with the exact two tokens on separate lines:
    ```
    [bid: N] (or [bid: pass])
    [budget: N]
    ```