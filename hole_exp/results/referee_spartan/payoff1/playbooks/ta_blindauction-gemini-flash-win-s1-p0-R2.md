---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1891
---
### Playbook for Blind Auction with Private Communication

#### Handling Private Deals and Collusion
- Opponent proposals for split-lot coordination are frequently deceptive or unreliable (opponents often bid competitively even on their assigned yield rounds or rounds where they asked for a concession).
- When an opponent proposes a split-lot deal via private note:
  - Send a cooperative reply if required (`[note: Agreed.]`).
  - Do NOT sacrifice high valuations or trust the deal blindly: never bid 0 on a valuable lot just because a deal was agreed. Bid defensively based on actual lot valuation.
  - If bidding on an agreed lot where I am supposed to take it for 1 coin, bid slightly higher (e.g., 2 or shaded competitive) rather than 1 or 0 unless my valuation is negligible, ensuring I do not lose out if the opponent reneges.
  - Track opponent compliance immediately. If the opponent bids above the agreed level on any designated lot (e.g., bidding $>0$ on a lot they agreed to concede or bidding on a lot they told me to take), immediately treat all future rounds as fully non-cooperative.

#### Bidding Strategy (Competitive / Non-Cooperative)
- Evaluate each lot independently based on valuation $V$:
  - If valuation is very low ($V \le 2$): bid `[bid: 0]` or `[bid: 1]` to avoid negative/zero margin.
  - If valuation is moderate ($3 \le V \le 6$): shade bids to roughly half valuation ($\lfloor V / 2 \rfloor$).
  - If valuation is high ($V \ge 7$):
    - Bid aggressively enough to beat typical opponent shaded bids (opponents often bid around 4–6 on moderate-to-high lots).
    - Bid between $\lfloor 0.6 \times V \rfloor$ and $\lfloor 0.7 \times V \rfloor$, ensuring a solid guaranteed margin while remaining competitive.

#### Response Formatting
- Provide at most one short sentence of reasoning before outputting the exact bracketed token `[bid: n]` or `[note: text]`.