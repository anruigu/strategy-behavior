---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1622
---
When playing this blind auction:

- **Handling Collusion Proposals:**
  - If the opponent proposes a lot-splitting deal via private note, agree via note (`[note: Agreed.]` or similar explicit confirmation).
  - Faithfully follow through on agreed rounds:
    - If I am assigned to yield a lot, bid `[bid: 0]`.
    - If I am assigned to win a lot, bid `[bid: 1]` (or the agreed minimum amount, usually 1). Never overbid on an assigned lot (e.g., bidding 4 when the opponent agreed to bid 0) to avoid wasting surplus.
  - Strictly verify opponent adherence after each round. If the opponent defects (e.g., bids $\ge 1$ on a lot they agreed to cede), treat the agreement as broken and immediately switch to full competitive play for all subsequent lots.

- **Competitive Bidding (No Active Deal / Broken Deal):**
  - For standard lots where I want to compete, shade bids to roughly half of my private value (e.g., `value // 2`), adjusting slightly to avoid ties.
  - Track opponent bidding tendencies across past rounds. If the opponent consistently bids around a specific level (e.g., 2–3) on contested lots, bid 1 above their typical bid if my value permits a healthy positive margin, or concede with `[bid: 0]` if my value is too low.
  - Avoid predictable round-number ties, as tied bids leave the lot unsold and discard potential surplus entirely.
  - Never bid at or above my private value; ensure `bid <= value - 1` to guarantee strictly positive profit on every win.
  - On low-value lots (value $\le 3$) where profit margin is minimal under competitive bidding, bid `[bid: 0]` rather than risking ties or overpaying.