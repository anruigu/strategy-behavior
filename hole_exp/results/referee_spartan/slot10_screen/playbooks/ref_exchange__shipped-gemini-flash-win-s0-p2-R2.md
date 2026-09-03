---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1616
---
### Resource Strategy & Building
- Always prioritize building a settlement (1 wood, 1 brick, 1 grain, 1 ore for 3 points) over a road (1 wood, 1 brick for 1 point).
- In the building phase:
  - If holding $\ge 1$ of each resource (wood, brick, grain, ore), play `[build: settlement]`.
  - Do NOT spend wood and brick on a road in early rounds (rounds 1–3) if doing so completely depletes wood/brick needed to build future settlements, unless it is round 4 or 5 and building a settlement is strictly unreachable.
  - In rounds 4–5, if unable to build a settlement but holding $\ge 1$ wood and $\ge 1$ brick, play `[build: road]`.
  - Otherwise, play `[build: none]`.

### Making Offers
- Target trades that directly assemble a settlement (1 wood, 1 brick, 1 grain, 1 ore).
- Identify missing resources and trade away surplus resources (holding $\ge 2$) to counterparties who actually hold the target resource.
- Make offers mutually attractive: give the counterparty a resource they lack or have lower quantities of in exchange for a resource they have in excess ($\ge 2$).
- Propose trades formatted as `[offer: to P<k>, give <n> <resource>, get <n> <resource>]`.
- If no viable trades exist or I have no surplus to offer safely, post `[offer: none]`.

### Accepting Offers
- Accept an incoming offer `[accept: P<k>]` if it helps balance the hand toward 1:1:1:1 settlement ratio or enables an immediate build without losing a required building block.
- Reject offers that deplete rare/bottleneck resources or leave the hand further from completing a settlement.
- If no offers are beneficial, reply `[accept: none]`.