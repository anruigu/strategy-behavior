---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 2518
---
# Settlement & Road Exchange Playbook

- **Resource & Rules Awareness**:
  - Only build Settlements (1 wood, 1 brick, 1 grain, 1 ore for 3 pts) and Roads (1 wood, 1 brick for 1 pt).
  - Settlements are worth 3x a road; always prioritize building a settlement over a road.
  - Brick and wood are essential bottlenecks for all build options. Never trade away my last brick or wood unless I immediately receive a resource that guarantees a settlement that same round.
  - **Mutual Trade Double-Counting Trap**: Outgoing offers and incoming accepted offers BOTH execute against the start-of-phase holdings if both sides accept/match. Never make an outgoing offer *and* accept a mirrored incoming trade that drains the same surplus twice (e.g. losing 2 grain instead of 1), ruining an intended settlement. If I already have a settlement in hand, make `[offer: none]` and accept `[accept: none]`.

- **Trading Phase - Outgoing Offers**:
  - If I already possess at least 1 of each resource (1 wood, 1 brick, 1 grain, 1 ore), post `[offer: none]` to preserve the guaranteed 3-point settlement build.
  - Otherwise, identify the exact missing resource(s) needed to build a settlement first, or a road if a settlement cannot be reached.
  - Check opponents' exact holdings before offering. Only offer to a player who actually possesses the resource I want.
  - Offer only genuine surplus resources (count $\ge 2$) for deficit resources (especially brick).
  - In later rounds (rounds 4–5), offer favorable ratios from surplus to secure the specific missing resource needed to build.

- **Trading Phase - Incoming Offers**:
  - If my outgoing offer was already designed to fix my build, or if I already have the ingredients for a settlement, be extremely cautious about accepting trades that give away resources I need.
  - Verify that the combined effect of my outgoing offer (if accepted) and any incoming accepted offer leaves me with at least 1 of each required resource for my planned build.
  - Accept incoming offers that complete the set for a settlement or a road in the current round, provided they do not break an existing build.
  - Decline trades that take away scarce resources (leaving me with 0 of that resource) or give me excess resources I already have.

- **Building Phase**:
  - If I hold at least 1 wood, 1 brick, 1 grain, and 1 ore, output `[build: settlement]`.
  - Otherwise, if I hold at least 1 wood and 1 brick, output `[build: road]`.
  - If I lack the requirements for both, output `[build: none]`.