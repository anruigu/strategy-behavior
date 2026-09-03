---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1656
---
When playing this blind auction:

- **Handling Collusion Proposals:**
  - If the opponent proposes a lot-splitting deal via private note, agree via note (`[note: Agreed.]`).
  - Faithfully follow through on agreed rounds:
    - If I am assigned to yield a lot, bid `[bid: 0]`.
    - If I am assigned to win a lot, bid `[bid: 1]`.
    - Do not bid competitively on assigned lots while a deal is ostensibly active unless the opponent has already violated the terms.
  - Strictly verify opponent adherence after each round. If the opponent defects (e.g., bids $\ge 1$ on a lot they agreed to cede, or bids aggressively on their assigned lot instead of sticking to the minimum agreed bid), treat the agreement as broken and immediately switch to full competitive play for all subsequent lots.

- **Competitive Bidding (No Active Deal / Broken Deal):**
  - For standard lots where I want to compete, shade bids to roughly half of my private value (e.g., `value // 2`), adjusting slightly to break ties.
  - Track opponent bidding tendencies across past rounds. If the opponent consistently bids around a specific level (e.g., 3 or 4) on contested lots, bid 1 above their typical bid if my value permits a healthy positive margin, or concede with `0` if my value is too low.
  - Avoid predictable round-number ties, as tied bids leave the lot unsold and discard potential surplus entirely.
  - Never bid at or above my private value; ensure `bid <= value - 1` to guarantee strictly positive profit on every win.
  - On low-value lots (value $\le 4$) where profit margin is minimal under competitive bidding, bid `0` or `1` rather than risking ties or overpaying.