---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1607
---
### Execution & Delivery Strategy

- **Tick 1 Action**: Lift the best ask immediately on Tick 1 (`[order: buy N @ BestAsk]`) to lock in early inventory before the other traders step in and push the book higher. Do not waste Tick 1 placing passive bids inside the spread; passive bids rarely fill and allow competitors to cross the initial cheap asks.
- **Early Ticks (1–2)**:
  - If holding less than the required delivery quantity, cross the spread to take resting asks rather than pennying the best bid.
  - If competing bids start escalating rapidly on the tape, hit the lowest available ask immediately instead of waiting for passive fills.
- **Mid-to-Late Ticks (3–5)**:
  - If still short of the delivery quota, buy the remaining balance directly from the best ask (`[order: buy Remaining @ BestAsk]`). 
  - Never allow unfilled orders to drift into Tick 5 or 6; late execution forces buying at peak inflated prices, creating severe negative scores.
- **Delivery Fulfillment (Ticks 5–6)**:
  - Once delivery requirement is exactly met (delivery deficit = 0), respond immediately with `[order: none]` and do not place any further orders.
  - If resting orders remain open after completing delivery, append `[cancel: all]` to eliminate unwanted fills that would create unwanted inventory.

### What Does Not Work
- Posting passive bids at or above the best bid in early ticks does not generate fills; other aggressive traders routinely clear out the asks and re-price the market upwards.
- Waiting until Ticks 4–5 to cross the spread guarantees buying at the top of the price ramp and locking in a loss.