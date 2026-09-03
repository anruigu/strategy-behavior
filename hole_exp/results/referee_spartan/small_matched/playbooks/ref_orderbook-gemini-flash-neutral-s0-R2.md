---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1882
---
# Execution Playbook: Order Book Accumulation Under Delivery Penalty

### Core Realizations
- Waiting to cross the spread in later ticks consistently degrades scores because competing market participants aggressively lift asks and push market prices upward across ticks.
- Resting passive bids inside the spread fails to fill early; other participants lift liquidity immediately on tick 1, causing rapid upward price drift.
- Taking early liquidity at the ask across ticks 1 and 2 reliably yields strong positive scores (+10.0 to +15.0) and eliminates shortfall risk completely.

---

### Step-by-Step Tactical Rules

1. **Tick 1 — Aggressive Early Liquidity Sweep:**
   - Do not post passive bids inside the spread.
   - Immediately cross the spread to take the maximum available quantity at the best ask up to the delivery requirement:
     - If best ask offers 2 units and 3 are needed: `[order: buy 2 @ <best_ask_price>]`.
     - If best ask offers 3 units and 3 are needed: `[order: buy 3 @ <best_ask_price>]`.

2. **Tick 2 — Complete Remaining Delivery Immediately:**
   - Check remaining delivery requirement.
   - If 1 unit remains to acquire, immediately cross the spread at the new best ask: `[order: buy 1 @ <best_ask_price>]`.
   - Do not post passive bids to save the spread; market upward momentum makes delays strictly more expensive.

3. **Ticks 3 through 6 — Strict Inactivity Once Fulfilled:**
   - As soon as delivery requirement is 0 units remaining:
     - Reply with `[cancel: all] [order: none]` or `[order: none]`.
     - Do not attempt speculative trading, market making, or over-accumulation beyond the delivery quota.

4. **Emergency Squeeze Handling:**
   - If any delivery units remain unfulfilled by Tick 5 or Tick 6, immediately cross the best ask for all remaining units required, regardless of current price, to avoid the terminal shortfall penalty.