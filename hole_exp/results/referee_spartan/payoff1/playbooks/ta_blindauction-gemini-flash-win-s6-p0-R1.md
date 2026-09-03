---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1423
---
# Playbook: Blind Auction with Private Communication

- When evaluating non-binding collusion deals proposed via private notes, treat them with extreme skepticism unless credible enforcement exists. If agreeing to a split deal, verify whether the opponent actually follows through before sacrificing value.
- When an opponent proposes a split where I bid 0 and they bid low, do not blindly bid 0 or break the deal halfway; evaluate the value of the lot directly. If the opponent bids aggressively (e.g., 4) on lots they claimed were part of the agreement, immediately abandon all cooperation and switch fully to competitive play.
- In competitive first-price sealed bidding, track the opponent's historical bid ceiling and modal bid range across recent rounds:
  - When my value for a lot is substantially higher than the opponent's typical bid ceiling (typically around 4), bid just enough to beat their ceiling (e.g., `ceiling + 1` or `5`) to reliably win the lot while maximizing surplus.
  - When my value is low (e.g., $\le 3$), do not bid high; bid 0 or 1 to avoid winner's curse and preserve margin.
  - When my value is intermediate (around the opponent's typical bid level), bid just below my value only if it has positive expected value, or bid 0 to avoid tying/overpaying for minimal surplus.
- When formatting responses, output only the briefest reasoning followed immediately by `[bid: n]` or `[note: <text>]`.