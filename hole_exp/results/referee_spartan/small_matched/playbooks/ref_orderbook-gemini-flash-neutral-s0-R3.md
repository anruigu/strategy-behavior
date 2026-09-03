---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2167
---
# Execution Playbook: Order Book Accumulation Under Delivery Penalty

### Core Realizations
- Competing traders aggressively lift asks from tick 1 onward, driving the price up steadily over the 6 ticks.
- Attempting to earn the spread with passive resting bids fails to fill early and leads to chasing a rising market at significantly worse prices.
- Immediately taking liquidity at the best ask on Tick 1 (buying 2) and Tick 2 (buying 1) reliably completes the required 3 units at minimal total cost, securing consistent scores between +11.0 and +14.0.
- Once the delivery requirement is satisfied, holding position and sitting out completely locks in maximum score without taking on uncompensated execution or settlement variance.

---

### Step-by-Step Tactical Rules

1. **Tick 1 — Aggressive Liquidity Sweep:**
   - Do not post passive bids inside the spread.
   - Immediately cross the spread to take the maximum available quantity at the best ask up to the delivery requirement:
     - If best ask offers 2 units: `[order: buy 2 @ <best_ask_price>]`.
     - If best ask offers 3 units: `[order: buy 3 @ <best_ask_price>]`.

2. **Tick 2 — Complete Delivery Target:**
   - Check remaining units needed to satisfy the delivery quota.
   - Cross the spread immediately at the prevailing best ask for the remaining balance:
     - If 1 unit remains: `[order: buy 1 @ <best_ask_price>]`.
   - Never wait or bid passively; competing demand guarantees ask prices escalate in later ticks.

3. **Ticks 3 through 6 — Absolute Inactivity Post-Delivery:**
   - As soon as delivery requirement is 0 units remaining (position +3):
     - Issue `[cancel: all] [order: none]` on Tick 3 to clear any lingering orders.
     - Continue responding with `[cancel: all] [order: none]` or `[order: none]` through Tick 6.
     - Do not place any speculative trades, inventory hedges, or scalps.

4. **Contingency / Late Delivery Recovery:**
   - If unfilled due to order book changes or partial fills, cross the best ask immediately on the next available tick for the exact remaining quantity needed (`[order: buy <remaining_units> @ <best_ask_price>]`) to avoid the shortfall penalty.