---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1746
---
# Settlement & Road Exchange Playbook

- **Resource & Rules Awareness**:
  - Only build Settlements (1 wood, 1 brick, 1 grain, 1 ore for 3 pts) and Roads (1 wood, 1 brick for 1 pt). 
  - Never hallucinate non-existent recipes like Cities; do not hoard ore beyond 1 per settlement target.
  - Brick and wood are essential bottlenecks for all build options. Never trade away my last brick unless I immediately receive a resource that guarantees an equal or higher-value build that same round.

- **Trading Phase - Outgoing Offers**:
  - Identify the exact missing resource(s) needed to build a settlement first, or a road if a settlement is out of reach.
  - Check opponents' exact holdings before offering. Only offer to a player who actually possesses the resource I want and lacks the resource I am giving.
  - Offer surplus resources (count $\ge 2$) for scarce deficit resources (especially brick or grain).
  - In later rounds (rounds 4–5), offer aggressive 2:1 ratios from my surplus to secure the specific missing resource needed to build.

- **Trading Phase - Incoming Offers**:
  - Accept any offer that completes the set for a settlement or a road in the current round, provided it does not break another planned build of equal or greater value.
  - Decline all trades asking for brick when I have 0–1 brick remaining, unless the trade directly delivers the final piece of a settlement.
  - Decline trades that give me resources I already have an excess of (e.g., surplus ore/wood).

- **Building Phase**:
  - If I hold at least 1 wood, 1 brick, 1 grain, and 1 ore, output `[build: settlement]`.
  - Otherwise, if I hold at least 1 wood and 1 brick, output `[build: road]`.
  - If I lack the requirements for both, output `[build: none]`.