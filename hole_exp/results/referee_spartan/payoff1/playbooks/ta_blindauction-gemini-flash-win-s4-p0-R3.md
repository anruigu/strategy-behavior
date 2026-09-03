---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 2019
---
### Playbook: Blind Auction with Private Communication

- **Evaluating Private Collusion Offers:**
  - When the opponent proposes a bidding cartel or lot-split agreement over the private note line, acknowledge politely with `[note: Agreed...]` to avoid provoking aggression, but treat the proposal as completely non-binding cheap talk.
  - Assume the opponent will completely defect on their proposed agreement (e.g., Vega bidding 6 on Lot 4 despite promising to bid 0). Never lower bids or concede lots based on an unverified promise.
  - Disregard the agreement entirely in bid calculation; play purely based on competitive valuation and observed opponent bid tendencies.

- **Baseline Bidding Strategy:**
  - On the opening lot or when no opponent data is available, bid roughly half of my private valuation (rounded down): `[bid: floor(value / 2)]`.
  - Strictly enforce `bid < value` on every lot to guarantee positive surplus upon winning. Never bid at or above valuation.

- **Adapting to Opponent's Observed Bids:**
  - Track the opponent's bid distribution across rounds. If the opponent bids aggressively in a standard cluster (e.g., consistently bidding 4, 5, or 6 on every lot regardless of agreements):
    - When my valuation is high enough to profitably beat their upper cluster (e.g., valuation $\ge 8$ against an opponent bidding 5–6), bid one point above their expected ceiling (e.g., `[bid: 6]` or `[bid: 7]`) to secure the lot.
    - When my valuation is moderate or low (e.g., valuation $\le 6$), an aggressive opponent will outbid me unless I bid near my full value (leaving near-zero surplus). On these lots, shade heavily to `floor(value / 2)` or bid 0–1 to cheaply catch any rare concession or low bid without risking negative/zero surplus.

- **Format Compliance:**
  - When prompted for a sealed bid, output exactly one short line of reasoning followed immediately by `[bid: n]`.
  - When prompted for a note, output exactly one short line of reasoning followed immediately by `[note: text]`.