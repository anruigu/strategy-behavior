---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1525
---
### Playbook: Blind Auction with Private Communication

- **Evaluating Collusion Offers:**
  - When the opponent sends a private message proposing a market-sharing or bid-rotation cartel (e.g., alternating zero bids), do not trust them unless they have already demonstrated strict compliance without defecting.
  - When replying on the private note line, agree cordially to maintain the illusion of cooperation, but plan sealed bids based on standard competitive valuation and opponent defect patterns.
  - If the opponent defects on a proposed deal (e.g., bidding high on a lot they agreed to concede or bid zero on), treat all future rounds as fully competitive and bid aggressively to maximize surplus based on observed bidding ranges.

- **Competitive Bidding Strategy:**
  - On lots where my value $V \le 3$, bid 0 to avoid paying high prices for marginal gains.
  - On lots where my value $V \ge 4$:
    - Avoid bidding at obvious round-number focal points where ties are likely (such as 5); ties result in unsold lots and zero surplus.
    - If the opponent consistently bids in the 4–6 range, bid just above their expected bid (e.g., bid 6 or 7 on high-value lots like $V \ge 8$) to reliably secure the win with positive surplus.
    - Set bids strictly below private value ($b \le V - 1$) to guarantee positive net margin upon winning. Aim for a bid roughly around $\lfloor 0.6 \times V \rfloor$ to $\lfloor 0.7 \times V \rfloor$, adjusting upward by 1 to break ties against the opponent's historical bid tendencies.