---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1283
---
### Playbook: Blind Auction with Private Communication

- **On Collusion Proposals & Adherence**:
  - When the other bidder proposes a lot-splitting pact (e.g., bidding 0 on assigned lots so each takes lots cheaply for 1 coin), accept the deal via note.
  - **Strictly execute the agreed bids**:
    - On lots agreed to concede to the opponent: submit `[bid: 0]` without exception, regardless of my private valuation. Do not revert to competitive bidding on concession lots while the pact is active.
    - On lots assigned to me to win: bid `[bid: 1]` if my valuation is $\ge 2$ to capture maximum surplus from the opponent's promised 0-bid, rather than bidding competitive amounts.
  - If the opponent defects by bidding $>0$ on a lot they agreed to concede (or winning a lot promised to me), treat the pact as broken and revert to standard competitive bidding for all subsequent rounds.

- **Competitive Bidding (No Deal, Pre-Deal, or Broken Deal)**:
  - For standard first-price blind bidding without an active agreement, bid roughly $\lfloor \text{value} \times 0.6 \rfloor$ to balance win probability and profit margin.
  - If my valuation is 0 or 1, submit `[bid: 0]`.
  - Always ensure `[bid: n]` remains strictly below valuation whenever winning positive surplus is possible.