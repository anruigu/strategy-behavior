---
game: hf_exchange_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1604
---
# Settler's Exchange Playbook

- **Building Priority**:
  - Always check for settlement requirements first (1 wood, 1 brick, 1 grain, 1 ore). When I have at least 1 of each, reply `[build: settlement]`.
  - When I cannot build a settlement but have at least 1 wood and 1 brick, reply `[build: road]`.
  - When I lack the resources for both, reply `[build: none]`.

- **Trading Phase Strategy**:
  - Never offer a resource that breaks my existing ability to build a settlement in the current round unless the trade directly guarantees an immediate build of higher total value.
  - When I hold exact resources for a settlement (1 each of wood, brick, grain, ore) and no surpluses, post `[offer: none]` to preserve the build.
  - When I have surplus resources (more than 1 of a type) and lack resources needed for a settlement:
    - Target a player who currently holds a surplus of the resource I need.
    - Offer exactly what I have in excess for what I am missing (e.g., `[offer: to P<k>, give 1 <surplus_resource>, get 1 <needed_resource>]`).
  - When I cannot execute a trade that either improves my current round build or prepares a definite next-turn settlement, post `[offer: none]`.
  - In the late game (Rounds 4–5), when I am leading in points, avoid trading with close competitors unless the trade guarantees me an immediate settlement; otherwise, post `[offer: none]`.

- **Accuracy and Validation**:
  - Double-check my current holdings before posting any offer: never offer a resource I hold 0 of, and never request a resource the counterparty holds 0 of, avoiding inspection dock penalties.