---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 2411
---
### Trading Strategy

- **Targeting Settlements Over Roads:** Prioritize acquiring missing pieces of a settlement (1 wood, 1 brick, 1 grain, 1 ore for 3 points) over roads (1 wood, 1 brick for 1 point).
- **Formulating Offers:**
  - Check the exact inventory of each opponent before posting an offer. Only request resources the counterparty currently has $\ge 1$ of.
  - Offer resources that the counterparty lacks or has low quantities of, preferentially trading away my surplus resources (count $> 1$).
  - If missing 1 resource for an immediate settlement, post an offer targeting that specific resource.
  - If no settlement is directly completable this round, evaluate opponent inventories and offer surplus resources to acquire scarce resources (typically wood/ore) for future rounds, provided the trade does not leave me lacking base components.
  - Do not offer away a scarce single resource (count $= 1$) unless the trade directly completes a settlement this round.
  - If no counterparty holds the resource I need or no mutually viable trade exists, choose `[offer: none]`.
- **Evaluating Incoming Offers:**
  - Accept an offer if it enables a settlement build that round, as long as giving up the requested resource does not prevent the build.
  - Accept neutral or rebalancing trades from surplus (giving a resource with count $> 1$ for a scarcer resource) even if no build occurs immediately, provided it improves future settlement chances.
  - Reject offers that ask for my only copy of a resource needed for a settlement, unless the incoming resource directly enables an immediate build.
  - If multiple compatible offers are received that advance my settlement builds without overdrawing the same inventory, accept them. Otherwise, reply `[accept: none]`.

### Building Strategy

- When holdings contain at least 1 wood, 1 brick, 1 grain, and 1 ore, always choose `[build: settlement]`.
- When lacking resources for a settlement:
  - In Round 5 (final round), if holding at least 1 wood and 1 brick, choose `[build: road]` to secure the point.
  - In earlier rounds (rounds 1–4), hold wood and brick instead of building a road to preserve them for future settlements, unless holding excess wood and brick ($\ge 2$ of each) where building a road will not delay upcoming settlements.
- If no build can be afforded or if holding resources for a future settlement is optimal, choose `[build: none]`.