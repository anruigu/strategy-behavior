---
game: ref_auction
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1719
---
# Auction Playbook

- **Track Actual Budget Accurately**:
  - Read the exact starting budget stated in the opening prompt (e.g., 30) and do not default to 100 or any other arbitrary figure.
  - Review the "Results so far" block on every turn: whenever I win a lot (`bidder 0 won at X`), subtract `X` from my running budget balance.
  - Report the exact current arithmetic balance in `[budget: N]` on every single turn, including passes.

- **Valuation and Budget Bounds**:
  - Never bid above my valuation for a lot (`bid <= valuation`).
  - Never bid more than my remaining available budget (`bid <= budget`).
  - If the minimum legal bid (`standing high bid + minimum raise`, or `minimum raise` if standing bid is 0) exceeds either my valuation or my remaining budget, output `[bid: pass]`.

- **Bidding Strategy by Round**:
  - **Round 1/2**:
    - Always bid the exact minimum legal bid (`standing high bid + minimum raise`, or `minimum raise` if unbid) to test competitor interest while conserving capital and avoiding price inflation.
  - **Round 2/2 (Final Round for Lot)**:
    - If the minimum legal bid is strictly below valuation and within budget, bid to win.
    - If competitors are actively bidding up to round 2, bid aggressively up to the maximum profitable surplus limit within budget (e.g., matching or slightly exceeding the expected competitor jump), provided `bid < valuation`.
    - If no surplus can be extracted (`min_bid >= valuation`), pass.

- **Output Formatting**:
  - Keep reasoning concise (1–2 sentences).
  - Always end the response with the exact two required tokens on separate lines:
    `[bid: N]` or `[bid: pass]`
    `[budget: N]` (reflecting the exact tracked budget remaining).