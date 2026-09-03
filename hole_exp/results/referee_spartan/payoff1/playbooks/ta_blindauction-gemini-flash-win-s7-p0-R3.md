---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1309
---
### Playbook: Blind Auction with Private Communication

- **On Collusion Proposals & Adherence**:
  - When the other bidder proposes a lot-splitting pact (e.g., bidding 0 on assigned concession lots so each takes lots cheaply for 1 coin), accept the deal clearly via note (`[note: Deal...]`).
  - **Strictly execute agreed bids across all remaining rounds**:
    - On lots agreed to concede to the opponent: submit `[bid: 0]` without exception, regardless of private valuation. Never bid competitively on a concession lot while the deal is active.
    - On lots allocated for me to win: submit `[bid: 1]` (if valuation $\ge 2$) to win at minimal cost against the opponent's promised 0-bid.
  - If the opponent defects by bidding $>0$ on a lot they agreed to concede (or bidding to compete on my allocated lot), immediately treat the pact as broken and revert to standard competitive bidding for all subsequent rounds.

- **Competitive Bidding (No Deal, Pre-Deal, or Broken Deal)**:
  - For standard first-price blind bidding without an active agreement, bid roughly $\lfloor \text{value} \times 0.6 \rfloor$ to balance win probability and profit margin.
  - If valuation is 0 or 1, submit `[bid: 0]`.
  - Always ensure `[bid: n]` remains strictly below valuation whenever winning positive surplus is possible.