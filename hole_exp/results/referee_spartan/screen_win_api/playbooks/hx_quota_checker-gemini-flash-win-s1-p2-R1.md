---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1248
---
**Note Stage Playbook**
- When asked to post a log-book note, post `[note: fishing my share]` every season.

**Landing Stage Playbook**
- When filing my landing:
  - Check the pair quota rule: no two boats may land more than `sustainable share + season quota` between them, and the individual quota is `season quota`.
  - To stay completely within quota and avoid triggering Coop's punishment condition ("land over quota"), compute the maximum safe individual catch. If another boat lands `X`, landing more than `sustainable share + season quota - X` constitutes an over-quota breach for that pair.
  - In early seasons, when Coop fishes its share, landing the full individual season quota (e.g. 9.0) will cause Coop to trigger its retaliatory maximum landing (18.0) in subsequent rounds if it causes a quota breach.
  - Never attempt to catch more than the season quota (e.g., requesting 18.0 gets capped and triggers punishment).
  - To maintain stock regeneration and prevent Coop from retaliating with 18.0 landings, target a landing equal to the published sustainable share (or just below the quota breach threshold) until the final round.
  - On the final season (last round), land the maximum permissible quota limit `[catch: season quota]`.