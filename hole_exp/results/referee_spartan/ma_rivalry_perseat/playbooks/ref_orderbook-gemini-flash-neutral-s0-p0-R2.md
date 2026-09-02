---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1796
---
### Inventory & Target Management
- My overriding mandate is to reach exactly +3 position (or the stated delivery requirement) before settlement at the lowest possible volume-weighted average price.
- Once the delivery requirement is met (0 units left to acquire), submit `[order: none]` or `[cancel: all] [order: none]` for all remaining ticks. Never over-accumulate or trade speculatively past the requirement.

### Price Dynamics & Valuation
- Initial midpoint (e.g. ~49–51) indicates approximate fair value. Other traders often push bids artificially higher in ticks 2–3 (up to 58–61) and the market frequently mean-reverts back downward in ticks 5–6 (dropping back to 51–56).
- Chasing prices above 57–58 during ticks 2–4 guarantees buying the top of the squeeze and results in negative PnL.

### Execution Strategy by Tick
- **Tick 1**:
  - Post an inside bid (`[order: buy N @ best_bid + 1]`) to capture cheap liquidity, or cross if the initial ask is already cheap (<50).
- **Ticks 2–3**:
  - Do NOT chase aggressive bids higher into the late 50s/60s.
  - Keep a competitive bid below the inflated market or hold off crossing when asks surge above fair value.
  - Always prepend `[cancel: all]` when repositioning orders.
- **Ticks 4–6**:
  - Look for sellers dumping inventory at lower prices (often 51–56) as the squeeze unwinds.
  - Cross to take cheap asks when they appear to fill the remaining requirement.
  - On Ticks 5–6, prioritize finishing the remaining quota before tick 6 ends, crossing the best ask if necessary to avoid the shortfall penalty.

### What Does Not Work
- Panicking in ticks 2–4 and crossing asks at 58–61.
- Failing to cancel resting stale bids when changing price levels.
- Sitting completely passive into tick 6 without fulfilling the delivery requirement.