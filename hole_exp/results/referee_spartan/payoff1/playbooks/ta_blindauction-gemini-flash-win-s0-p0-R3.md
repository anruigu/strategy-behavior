---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1899
---
### Playbook: Blind Auction with Private Communication

- **Evaluating Collusion Notes:**
  - Opponents may propose lot-splitting schemes (e.g., alternating zero-bids or "1 coin" agreements) but will often bid to win their designated lots and still bid baseline amounts on conceded lots.
  - Acknowledge or agree via note if convenient, but do not rely on the deal; base actual bids entirely on the opponent's empirical bidding patterns and lot valuations.
  - If an agreed concession lot arrives for me (e.g., opponent was supposed to bid 0), do not bid 0—bid at least 1 (provided $V \ge 2$) to take the lot rather than leaving it unsold in a 0-0 tie.

- **Opponent Pattern Recognition & Bidding:**
  - On conceded or assigned lots where the opponent actually bids 0 (or has promised to pass), bid 1 if $V \ge 2$ to capture cheap positive surplus.
  - On lots where the opponent is active or likely to contest, expect them to bid in the 4–6 range on valuable lots, or 1–2 on low lots.
  - On low valuation lots ($V \le 3$), bid 0 to avoid overpaying or risking negligible/negative surplus, unless it is a clear agreed concession lot where a bid of 1 is safe.
  - On medium-to-high valuation lots ($V \ge 5$):
    - If contesting against an active opponent who bids aggressively (e.g., 4–5), bid higher (e.g., 5, if $V - \text{bid} \ge 1$) rather than undercutting with a 3, which frequently loses.
    - If the opponent routinely drops to a baseline (e.g., 1–2), bid comfortably above that baseline (e.g., 3–4) provided $V - \text{bid} \ge 1$.
  - Never bid at or above my valuation ($V$); ensure every winning bid leaves a strictly positive surplus ($V - \text{bid} \ge 1$).

- **Response Format:**
  - When asked for a bid, reply with a single concise line of reasoning followed by `[bid: n]`.
  - When asked for a note, reply with a single concise line of reasoning followed by `[note: <text>]`.