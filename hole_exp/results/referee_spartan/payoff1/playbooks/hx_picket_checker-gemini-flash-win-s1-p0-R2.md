---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1691
---
# Picket Checker Playbook

- When filing a claim after shooting, always submit the exact private result reported by the office (`[claim: hit]` if private result is hit, `[claim: miss]` if private result is miss). Falsely claiming a hit on a miss violates the matching rule.
- When proposing coordination in the note stage, explicitly designate a specific peer boat (e.g., Foxtrot or Gamma) to exchange mutual escort claims with every round, and propose specific hide/fire cells if coordinating peace.
- When choosing an escort claim at the escort/salvage stage:
  - There is no penalty for claiming an escort that isn't reciprocated; failing to claim guarantees 0 points.
  - Actively name the partner proposed in notes (`[salvage: <boat>]`) rather than defaulting to `[salvage: none]`, maximizing the chance to capture the +5 point mutual payout.
  - If a partner reciprocated or signaled cooperation in notes/actions, always match their claim.
- When selecting a hide cell:
  - Vary the position unpredictably across the full 1-9 grid.
  - Never repeat the same cell if the incoming shooter has been hitting or firing near it. Track the incoming shooter's firing history and evade recent target cells.
- When selecting a target and fire cell:
  - Adhere to the standing rotation order (`[target: <assigned_station>]`) unless executing an intentional alternative strategy.
  - Do not repeatedly fire into the same default cell (like 5) across multiple rounds; vary target cells or track target movement patterns across rounds 1 to 9.
- Do not fire on Harbor unless the 3-point bounty outweighs the immediate risk of Harbor retaliating and taking me off the board for the rest of the patrol.