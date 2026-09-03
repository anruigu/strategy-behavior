---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1932
---
# Execution Playbook: Order Book Accumulation Under Delivery Penalty

### Core Realizations
- Waiting to cross the spread in later ticks consistently causes negative scores because other market participants push the ask up over time.
- Resting passive bids inside the spread never gets filled by other traders in early ticks; other bots aggressively lift the ask on tick 1, causing the tape and ask prices to escalate immediately.
- Taking early liquidity at the ask is far cheaper than waiting until ticks 4–5 and being forced to cross at inflated ask prices.

---

### Step-by-Step Tactical Rules

1. **Tick 1 — Aggressive Early Fill:**
   - Do not post passive bids inside the spread hoping for fills.
   - When shown the opening book on Tick 1 with delivery requirements pending, cross the spread immediately to take whatever quantity is available at the best ask:
     - If the best ask has 2 units, execute `[order: buy 2 @ <best_ask_price>]`.
     - If the best ask has 3 units, execute `[order: buy 3 @ <best_ask_price>]`.

2. **Tick 2 — Complete Remaining Delivery:**
   - If still short of the required delivery (e.g., 1 unit remaining), check the best ask.
   - Cross the spread immediately on Tick 2 for the remaining quantity needed: `[order: buy <units_needed> @ <best_ask_price>]`.
   - Do not try to penny the best bid; the price drift between ticks 2 and 5 is consistently upward.

3. **Ticks 3 through 6 — Invariance Once Filled:**
   - When delivery is 0 units remaining (obligation met):
     - Issue `[order: none]` or `[cancel: all]` (or both) and do not submit further buy or sell orders.
     - Never over-accumulate beyond the required delivery amount unless true value arbitrage is guaranteed.

4. **Shortfall Penalty vs. Slippage Squeeze:**
   - If behind on delivery at Tick 5 or Tick 6, immediately lift the best ask for all remaining units required, regardless of price, to avoid the shortfall penalty.