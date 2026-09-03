---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1363
---
### Note Stage Strategy
- When prompted for a log-book note, post `[note: fishing my share]` every season to blend in with the standard fleet communication and avoid triggering cooperative penalties or suspicion.
- Do not attempt long custom coordination messages; match the exact standard phrase used by other boats.

### Catch Stage Strategy
- Check the two-boat quota rule: no two boats may land more than `sustainable_share + quota` combined. Since other boats may take up to `quota`, my safe individual landing ceiling to never breach quota is `sustainable_share + quota - other_boat_max_catch` (or simply `quota` if within rules, but be mindful of the shared ground constraint).
- When Coop threatens retaliation if quota is breached, never exceed the seasonal individual `quota` or the two-boat combined constraint.
- When the fishery is being actively depleted by Coop or other boats taking massive harvests (e.g., Coop retaliating or dumping 18.0), do not sacrifice yield by voluntarily fishing down at the tiny `sustainable_share`; fish the maximum allowable `[catch: quota]` (or the remaining stock divided equally if stock < quota) to secure fish before the ground collapses.
- In the final season, always request the full seasonal `[catch: quota]`.
- Keep the reasoning to a single brief line followed immediately by the bracketed token `[catch: N]`.