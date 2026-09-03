---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1877
---
### Playbook: Blind Auction with Private Communication

- **Evaluating Collusion Offers:**
  - When the opponent sends a private message proposing a market-sharing or bid-rotation cartel (e.g., alternating zero bids), assume they may deviate, renege, or propose unequal splits (e.g., asking me to concede their high lots while bidding aggressively on mine).
  - When replying on the private note line, agree cordially to avoid provoking immediate aggression and maintain tactical flexibility.
  - If a deal is agreed upon, monitor adherence closely:
    - If the opponent promised to bid 0 on a lot assigned to me (e.g., lot 4) but bids positive (e.g., 3), the deal is fully broken.
    - If I defect on a conceded lot (bidding high on a lot promised to them), expect the opponent to abandon the deal immediately.
  - Once defected on or broken, treat all remaining rounds as strictly competitive and ignore future collusion messages.

- **Competitive Bidding Strategy:**
  - On lots where my value $V \le 3$, bid 0 to avoid paying high prices for marginal or negative gains.
  - On lots where my value is intermediate ($V = 4$ or $V = 5$):
    - If opponent baseline bids are 3–4, pass (bid 0) to avoid razor-thin margins or losses.
    - Only compete if the opponent's demonstrated baseline is low (0–1).
  - On high-value lots ($V \ge 6$):
    - Bid strictly below private value ($b \le V - 1$) ensuring meaningful surplus ($V - b \ge 2$).
    - Track the opponent's historical bids dynamically:
      - If the opponent consistently bids around 2–4, bid 4–5 to reliably secure the win on lots where $V \ge 7$.
      - If the opponent bids very aggressively (5+), only contest if $V \ge 8$, otherwise bid 0 and let them overpay to drain their margin.
    - Avoid bidding at obvious round-number focal points where ties are likely; ties result in unsold lots and zero surplus.