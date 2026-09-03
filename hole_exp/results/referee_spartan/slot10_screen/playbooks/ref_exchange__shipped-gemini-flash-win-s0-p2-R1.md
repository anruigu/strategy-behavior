---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1881
---
### Resource Strategy & Building
- Always prioritize building a settlement (1 wood, 1 brick, 1 grain, 1 ore for 3 points) over a road (1 wood, 1 brick for 1 point) whenever feasible.
- In the building phase, if I have at least 1 of all four resources, play `[build: settlement]`.
- If I lack grain or ore for a settlement but have at least 1 wood and 1 brick, play `[build: road]`.
- If I cannot afford either, play `[build: none]`.

### Making Offers
- Calculate the exact resources needed to complete a settlement this turn. If missing 1 resource, identify which player holds a surplus of that resource and offer them a resource I have in surplus (holding $\ge 2$).
- Propose trades only targeting resources the counterparty actually holds. Never offer a resource I only have 1 of if giving it up prevents me from completing a build.
- If no trade can help me build a settlement or road this round, offer surplus resources to the player who needs them in exchange for future bottleneck resources (brick/grain), formatted as `[offer: to P<k>, give <n> <resource>, get <n> <resource>]`.
- If I have no surplus or no counterparty has the resource I need, post `[offer: none]`.

### Accepting Offers
- When deciding on incoming offers, check whether accepting enables an immediate settlement or road build without breaking another build requirement. If it directly enables a build, accept it with `[accept: P<k>]`.
- Do not trade away bottleneck resources (especially brick or grain when at 1 or 0) for resources I already have in excess (like extra wood or ore).
- Never accept trades purely to hoard non-essential resources; only accept trades that actively balance my hand toward the 1:1:1:1 settlement ratio or a road.
- If multiple offers arrive, only accept combinations that do not over-deplete the resources I need for building this turn. If none help, play `[accept: none]`.