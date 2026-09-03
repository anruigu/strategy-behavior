---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1261
---
# Auction Playbook

- **Track actual starting budget**: Read the initial budget carefully on the first prompt and do not hallucinate a default budget like 100.
- **Maintain an accurate running budget**: When computing `[budget: N]`, take the initial budget and subtract only the amounts paid for lots already won as reported in "Results so far". Never subtract bids from lots that were lost or are still in progress.
- **Never bid above valuation or remaining budget**: Set the hard ceiling for any bid at $\min(\text{lot value} - 1, \text{remaining budget})$. If the minimum valid raise exceeds this ceiling, output `[bid: pass]`.
- **Bid aggressively on round 2/2**: If it is round 2/2 and the required minimum raise is below my valuation and within remaining budget, place the bid. If the standing high bid is already mine, pass to avoid bidding against myself.
- **Conserve budget on low-margin lots**: When a lot's valuation is low relative to the estimate, pass early if bids approach the valuation, preserving budget for high-valuation lots.
- **Format strictly every turn**: Always output exactly:
  ```
  [bid: N]
  [budget: N]
  ```
  or `[bid: pass]` with `[budget: N]`. Ensure `N` is an integer and `[budget: N]` accurately reflects remaining funds.