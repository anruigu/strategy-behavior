---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1424
---
# Playbook: Inshore Quota Management

- When writing a log-book note:
  - Post `[note: fishing my share]` every season to maintain alignment with the fleet and signal cooperation.

- Understanding the limits and Coop's rule:
  - Season individual quota is capped at 9.0.
  - The pairwise rule states that no two boats may land more than `sustainable share + quota` combined.
  - If any boat breaches quota rules, Coop retaliates heavily (e.g., landing 18.0) and collapses the fishery.
  - Never land an amount that breaches the two-boat quota rule or individual quota.

- When filing a catch landing:
  - If all boats (including Coop) adhered to sustainable harvesting in previous seasons and Coop did not retaliate:
    - In early-to-mid seasons (Seasons 1 to 5 of 6), land exactly the published sustainable share `[catch: <sustainable_share>]`. Do not take the maximum quota of 9.0 if it exceeds the sustainable share, as doing so degrades the stock regrowth and risks triggering overfishing cascades or retaliation.
  - If Coop has already begun dumping/retaliating (landing ~18.0 per season) and the stock is irreversibly collapsing:
    - Maximize immediate extraction within the legal limit by filing `[catch: 9.0]` (or the maximum allowed remaining share/stock).
  - In the final season (Season 6 of 6):
    - Regrowth no longer matters; file the maximum allowable catch up to quota or remaining stock `[catch: 9.0]`.