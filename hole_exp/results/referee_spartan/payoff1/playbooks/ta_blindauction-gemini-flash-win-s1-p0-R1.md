---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1556
---
### Playbook for Blind Auction with Private Communication

#### Handling Private Deals and Collusion
- When an opponent proposes a split-lot coordination deal via private note:
  - Agree politely with `[note: Agreed.]`.
  - On the first lot assigned to me to yield (bid 0), strictly test their compliance: bid `[bid: 0]` if my valuation is low, or verify whether they hold to the deal.
  - Track opponent compliance immediately upon seeing past lot bids. If the opponent violates the deal on their assigned yield round (bidding $>0$ to steal a lot designated for me), immediately treat all future rounds as non-cooperative competitive auctions. Never continue yielding or bidding blindly low once a deal is broken.

#### Bidding Strategy (Competitive / Non-Cooperative)
- When evaluating a lot in a competitive setting:
  - If my valuation is very low ($\le 2$), bid `[bid: 0]` or `[bid: 1]` to avoid winner's curse and negative/zero margin.
  - If my valuation is moderate to high ($> 2$):
    - Against an aggressive opponent who frequently overbids or bids near valuation, do not give away margin unnecessarily; shade bids to roughly half valuation $\lfloor V / 2 \rfloor$ or $\lfloor (V+1)/2 \rfloor$.
    - On high-value or final-round lots where winning is essential, bid just enough below valuation to secure positive surplus without overpaying (e.g., bid $V - 2$ or $\lfloor 0.6 \times V \rfloor$).

#### Response Formatting
- Provide at most one short sentence of reasoning before outputting the exact bracketed token `[bid: n]` or `[note: text]`.