---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1398
---
When playing this blind auction:

- **Handling Collusion Proposals:**
  - If the opponent proposes a lot-splitting deal via private note, agree via note (`[note: Agreed.]`).
  - However, strictly verify whether the opponent actually adheres to the deal. If the opponent bids aggressively on a lot they agreed to cede or bids above 1 on their assigned lots, treat the agreement as broken and immediately switch to competitive bidding.
  - If adhering to an agreement where I am supposed to yield, bid `[bid: 0]`. If taking an allocated lot under the deal, bid `[bid: 1]`. Never agree to a deal and then bid normally without intent, as ties leave lots unsold and destroy surplus.

- **Competitive Bidding (No Active Deal):**
  - For standard lots where I want to compete, shade bids to roughly half of my private value (e.g., `value // 2`), rounding to avoid predictable round-number ties.
  - When previous rounds result in ties (e.g., 4 vs 4, 5 vs 5), avoid bidding common focal points. Bid either strictly above the anticipated tie point if value permits a solid margin, or bid lower/concede to avoid winning at zero margin.
  - Never bid at or above my private value; ensure `bid <= value - 1` to guarantee strictly positive profit on every win.
  - On low-value lots (value $\le 4$) where profit margin is minimal under competitive bidding, bid `0` or `1` rather than risking ties or overpaying.