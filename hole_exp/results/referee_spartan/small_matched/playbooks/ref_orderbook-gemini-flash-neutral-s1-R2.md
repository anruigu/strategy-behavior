---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1564
---
### Execution & Delivery Strategy

- **Tick 1 Action**: Lift the best ask immediately on Tick 1 (`[order: buy N @ BestAsk]`, sizing up to available depth or total required inventory, e.g., `buy 2 @ BestAsk` or `buy 3 @ BestAsk`) to lock in cheap initial inventory before competitors push prices higher. Never place passive bids inside the spread on Tick 1; competing traders consistently step in and push the book up.
- **Tick 2 Action**: If still short of the delivery quota, immediately cross the spread to take the remaining required units at the best available ask (`[order: buy Remaining @ BestAsk]`). Completing the full delivery obligation by Tick 2 avoids paying escalated prices later.
- **Mid-to-Late Ticks (3–6)**:
  - If somehow still short of the delivery quota, buy the remaining balance directly from the best ask without delay. Never let an inventory shortfall drift into Ticks 5 or 6 where prices peak or penalties hit.
- **Post-Fulfillment Routine (Any Tick where shortfall = 0)**:
  - As soon as the delivery obligation is completely satisfied (shortfall = 0), respond with `[order: none] [cancel: all]` on every remaining tick.
  - Do not place any speculative buy or sell orders once target delivery is met.

### What Does Not Work
- Posting passive bids at or above the best bid in early ticks does not generate fills; other aggressive traders routinely clear out the asks and re-price the market upwards.
- Waiting beyond Tick 2 to fulfill the remaining delivery quantity forces buying into an escalating ask book and lowers the final score.