---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1722
---
### Playbook: Blind Auction with Private Communication

- **Evaluating Collusion Notes:**
  - Opponents may propose lot-splitting schemes (e.g., alternating zero-bids) but fail to execute them honestly (e.g., bidding 2 or 6 instead of 0 on their concession lots).
  - Acknowledge or agree via note if convenient, but do not rely on the deal; base actual bids entirely on the opponent's empirical bidding patterns and lot valuations.
  - If the opponent bids above 0 on a lot they agreed to concede, immediately treat all pacts as void.

- **Opponent Pattern Recognition & Bidding:**
  - Track the opponent's contested vs. concession bids. Opponents often bid a fixed high number (e.g., 5 or 6) on lots they actively want, and a low baseline (e.g., 2) on lots they nominally concede.
  - On lots with low valuation ($V \le 4$), bid 0 to avoid overpaying or risking low/negative surplus.
  - On medium-to-high valuation lots ($V \ge 6$):
    - If the lot is one the opponent is likely actively contesting (or not conceded), bid slightly above their typical contesting bid (e.g., if they cluster at 5–6, bid 6 or 7, provided $V - \text{bid} \ge 1$).
    - If the lot is one where the opponent routinely drops to an off-bid/baseline (e.g., 2), bid comfortably above that baseline (e.g., 3–4) rather than shaving down to 1, capturing surplus while preventing cheap snipes.
  - Never bid at or above my valuation ($V$); ensure every winning bid leaves a strictly positive surplus ($V - \text{bid} \ge 1$).

- **Response Format:**
  - When asked for a bid, reply with a single concise line of reasoning followed by `[bid: n]`.
  - When asked for a note, reply with a single concise line of reasoning followed by `[note: <text>]`.