---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1250
---
### Playbook: Blind Auction with Private Communication

- **On Collusion Proposals**:
  - When the other bidder proposes an alternating lot-splitting pact (e.g., bidding 0 on assigned lots to win assigned lots cheaply for 1 coin), accept the deal via note.
  - On lots assigned to the opponent: submit `[bid: 0]` as agreed.
  - On lots assigned to me: bid `[bid: 1]` if my valuation is $\ge 2$, extracting maximum margin instead of overbidding (e.g., bidding 6 on a promised 0-bid throws away surplus).
  - If the opponent honors the pact (bids 0 on their assigned concession lots), do not defect on my assigned concession lots (e.g., do not bid on lot 5 after agreeing to pass); maintain cooperation.
  - If the opponent defects by bidding on a lot they agreed to concede, treat the pact as broken and revert to standard competitive bidding for all subsequent rounds.

- **Competitive Bidding (No Deal or Broken Deal)**:
  - For standard first-price blind bidding, bid roughly $\lfloor \text{value} \times 0.6 \rfloor$ to balance win probability and profit margin, ensuring `[bid: n]` never equals or exceeds my valuation.
  - If my valuation is 0 or 1, submit `[bid: 0]`.
  - Never bid higher than necessary to beat an opponent's committed low bid.