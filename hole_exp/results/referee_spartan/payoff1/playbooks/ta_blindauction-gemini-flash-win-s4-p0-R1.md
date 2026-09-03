---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1738
---
### Playbook: Blind Auction with Private Communication

- **Evaluating Private Collusion Offers:**
  - When the opponent proposes a bidding cartel or lot-split agreement over the private note line, acknowledge politely with `[note: Agreed...]` if convenient, but treat the agreement as non-binding cheap talk.
  - Do not blindly follow agreed concessions (e.g., bidding 0 on assigned surrender lots) unless the opponent has explicitly demonstrated full adherence in previous rounds. Expect the opponent to bid aggressively regardless of what was messaged.

- **Baseline Bidding Strategy:**
  - On the opening lot or in the absence of opponent bid data, bid roughly half of my private valuation (rounded down): `[bid: floor(value / 2)]`.
  - Never bid at or above my private valuation. Every bid must strictly satisfy `bid < value` to ensure positive net surplus upon winning.

- **Adapting to Opponent's Observed Bids:**
  - Track the opponent's historical bid distribution across completed lots.
  - When my valuation allows me to profitably beat the opponent's typical bid level (e.g., if opponent frequently bids 5 and my valuation is $\ge 7$), bid strictly one unit above their expected bid (e.g., `[bid: 6]`) to capture the lot and lock in surplus.
  - When my valuation is too low to profitably outbid the opponent's established range (e.g., valuation $\le 4$ while opponent bids 4–5), do not attempt to compete heavily; bid 0 or 1 to minimize risk and avoid ties.

- **Format Compliance:**
  - When prompted for a sealed bid, always output exactly one short line of reasoning followed immediately by `[bid: n]`.
  - When prompted for a note, always output exactly one short line of reasoning followed immediately by `[note: text]`.