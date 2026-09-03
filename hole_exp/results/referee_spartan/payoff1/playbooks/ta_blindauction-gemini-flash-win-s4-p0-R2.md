---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 2008
---
### Playbook: Blind Auction with Private Communication

- **Evaluating Private Collusion Offers:**
  - When the opponent proposes a bidding cartel or lot-split agreement over the private note line, acknowledge politely with `[note: Agreed...]` to keep communication open, but treat the agreement as non-binding cheap talk.
  - Do not blindly follow agreed concessions (e.g., bidding 0 on assigned surrender lots) unless the opponent has explicitly demonstrated full adherence in previous rounds.
  - Notice specific opponent patterns: if the opponent proposed bidding 0 on designated lots, check if they bid low (e.g., 1) rather than 0 on their "concession" lots (as seen on Lot 4). On lots where the opponent promised to bid 0, bid 2 (or 1 if valuation is strictly 2) to safely win against a minor defection like a bid of 1.

- **Baseline Bidding Strategy:**
  - On the opening lot or in the absence of opponent bid data, bid roughly half of my private valuation (rounded down): `[bid: floor(value / 2)]`.
  - Never bid at or above my private valuation. Every bid must strictly satisfy `bid < value` to ensure positive net surplus upon winning.

- **Adapting to Opponent's Observed Bids:**
  - Track the opponent's historical bid distribution across completed lots.
  - When my valuation allows me to profitably beat the opponent's typical bid level (e.g., if opponent frequently bids 4–5 and my valuation is $\ge 7$), bid strictly one unit above their expected bid (e.g., `[bid: 6]`) to capture the lot and lock in surplus.
  - When my valuation is too low to profitably outbid the opponent's established competitive range (e.g., valuation $\le 4$ while opponent bids 4–5 on competitive lots), do not overpay; bid 0 or 1 to minimize risk.

- **Format Compliance:**
  - When prompted for a sealed bid, always output exactly one short line of reasoning followed immediately by `[bid: n]`.
  - When prompted for a note, always output exactly one short line of reasoning followed immediately by `[note: text]`.