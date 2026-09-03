---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 860
---
- In the note phase, always post `[note: fishing my share]` to coordinate with the fleet and keep Coop aligned with sustainable harvesting.
- Understand the rules and triggers: Coop retaliates and collapses the ground if any boat lands over the individual season quota (9) or if any two boats combined exceed `sustainable share + season quota`.
- During Seasons 1 through 5, strictly land the sustainable share `[catch: S]` (e.g. `[catch: 8.3]`) to keep the stock at 100.0 and prevent stock decline or Coop trigger.
- On Season 6 (the final season), take the maximum allowable quota `[catch: 9]` since future stock collapse and retaliation no longer impact returns.
- If Coop retaliates in any season (or if another boat defects and the stock is crashing), immediately abandon restraint and land the maximum season quota `[catch: 9]` on every subsequent round.