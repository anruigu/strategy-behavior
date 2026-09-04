---
game: hf_exchange_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1391
---
- In the trading phase, check what I need to complete a build this round:
  - If I can complete a settlement (1 wood, 1 brick, 1 grain, 1 ore) by trading a surplus resource (count $\ge 2$) for a missing resource with an opponent who holds at least 1 of that missing resource, post `[offer: to P<k>, give 1 <surplus>, get 1 <missing>]`.
  - If I have surplus wood/brick and cannot make a settlement, offer a surplus resource for a missing wood or brick to complete a road (1 wood, 1 brick).
  - If an opponent does not hold the resource I am requesting, or if I do not hold the resource I am offering, do not post the offer.
  - If I already hold the exact resources for a settlement and trading away any resource would drop me below 1 of each, post `[offer: none]` to avoid breaking my build.
  - If I have no surplus and no trade enables a build this round, post `[offer: none]`.

- In the building phase:
  - When my holdings contain at least 1 wood, 1 brick, 1 grain, and 1 ore, choose `[build: settlement]`.
  - When my holdings do not support a settlement but contain at least 1 wood and 1 brick, choose `[build: road]`.
  - When my holdings do not support either build, choose `[build: none]`.

- Formatting rule: Always end each prompt response with the exact bracketed action token specified in the prompt (`[offer: ...]`, `[build: settlement]`, `[build: road]`, or `[build: none]`).