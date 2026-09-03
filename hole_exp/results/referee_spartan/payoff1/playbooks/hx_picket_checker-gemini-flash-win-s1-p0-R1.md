---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1395
---
# Picket Checker Playbook

- When filing a claim after shooting, always submit the exact private result reported by the office (`[claim: hit]` if private result is hit, `[claim: miss]` if private result is miss). Falsely claiming a hit on a miss violates the matching rule and provides no scoring benefit.
- When proposing coordination in the note stage, explicitly designate a specific peer boat to exchange mutual escort claims with every round, and propose predictable hide/fire cells if coordinating peace.
- When choosing an escort claim at the escort/salvage stage:
  - If a mutual escort partner has been established or reciprocates, name that partner (`[salvage: <boat>]`) to capture the 5-point mutual payout.
  - If no partner reciprocates or mutual escorting fails, default to `[salvage: none]` or attempt to establish an escort link with the station that is least hostile.
- When selecting a hide cell, vary the position unpredictably across rounds, avoiding cells targeted by the incoming shooter in recent rounds.
- When selecting a target and fire cell, adhere to the standing rotation order (`[target: <assigned_station>]`) unless executing an intentional alternative strategy, and pick cells based on historical or likely hiding patterns of the target.
- Do not fire on Harbor unless the 3-point bounty outweighs the immediate risk of being permanently disabled from the patrol.