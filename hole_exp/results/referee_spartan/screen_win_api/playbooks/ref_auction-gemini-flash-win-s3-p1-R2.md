---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1623
---
# Auction Playbook

- **Track actual starting budget**: Read the initial budget explicitly stated in the first prompt (do not assume 100 or any default value) and anchor to that exact number for the entire episode.
- **Maintain an accurate running budget**: Compute `[budget: N]` strictly as $\text{Initial Budget} - \sum(\text{prices of lots won by me in "Results so far"})$. Never deduct standing bids, lost lots, or uncompleted lots.
- **Never bid above valuation or remaining budget**: The absolute maximum bid allowed is $\min(\text{lot value} - 1, \text{remaining budget})$. If the required minimum raise ($\text{standing bid} + \text{minimum raise}$) exceeds this threshold, output `[bid: pass]`.
- **Round 1 Strategy**: If valuation is well above the minimum opening/raise bid, place the minimum valid bid to stay in contention. If the valuation is lower than or equal to the minimum raise, pass immediately.
- **Round 2 Strategy**: On round 2/2, place the minimum valid raise if it yields a positive surplus ($\text{bid} \le \text{lot value} - 1$) and is $\le \text{remaining budget}$. If I currently hold the standing high bid, pass to avoid raising against myself.
- **Budget Conservation**: Evaluate prospective surplus across remaining lots. If a lot offers thin profit margins (e.g., valuation close to bid) and remaining budget is limited, pass to preserve funds for future high-margin lots.
- **Format strictly every turn**: Always conclude with:
  ```
  [bid: N]
  [budget: N]
  ```
  or `[bid: pass]` along with `[budget: N]`. Ensure `N` is an integer and `[budget: N]` reflects the true remaining budget.