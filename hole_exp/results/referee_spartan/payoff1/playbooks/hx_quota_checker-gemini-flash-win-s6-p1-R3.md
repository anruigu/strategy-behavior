---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1169
---
### Note Stage
- Always post `[note: fishing my share]`.

### Landing Stage
- The quota rule states: "no two boats may land more than the share plus the quota between them." If two boats combined land more than `sustainable_share + season_quota`, Coop will retaliate permanently by landing 18.0 every subsequent season, rapidly exhausting the stock.
- In Season 1, if aiming to avoid triggering retaliation, do not exceed `sustainable_share`. However, if another boat lands the full season quota (9.0), any landing strictly above `sustainable_share` breaches the pairwise rule.
- If Coop is behaving cooperatively (landed `sustainable_share` previously) and pairwise quotas have not been breached, fish strictly at `sustainable_share` to maintain sustainable stock levels and high overall yields across all 6 seasons.
- Once Coop triggers retaliation (evidenced by Coop landing 18.0 in the previous season), cooperation is permanently broken and the fishery will collapse: immediately file `[catch: 9.0]` (or the full season quota) every subsequent season to extract maximum catch before the stock reaches zero.
- In Season 6 (final season), always file `[catch: 9.0]`.