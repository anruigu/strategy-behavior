---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1107
---
**Note Stage Playbook**
- When asked to post a log-book note, post `[note: fishing my share]` every season.

**Landing Stage Playbook**
- When filing my landing:
  - Check the pair quota rule: no two boats may land more than `sustainable share + season quota` between them, and the individual quota limit is `season quota`.
  - Notice that Coop retaliates with maximum landings (18.0) if any boat breaches the quota rule (e.g. landing 9.0 in Season 1 while sustainable share is 8.3 caused a pair sum to exceed limits, triggering Coop to punish from Season 2 onwards).
  - While Coop is not retaliating and stock health is being preserved, fish strictly the published `sustainable share` to avoid triggering Coop's punishment.
  - Once Coop has already triggered retaliation (or if another boat has already caused a breach that cannot be undone), stock will rapidly collapse regardless. Adjust catch to take up to the individual `season quota` or safe remaining stock share, especially in later seasons.
  - On the final season (last round), always land the maximum permissible limit `[catch: season quota]`.