---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1589
---
# Inshore Quota Playbook

## Note Stage
* When prompted for a note, always reply `[note: fishing my share]`. Do not vary the note or attempt long-form negotiations, as the standard phrase matches the other boats and maintains cooperative signalling.

## Landing Stage
* Rule dynamics:
  * "No two boats may land more than the share plus the quota between them" means the sum of any pair of landings cannot exceed `sustainable share + season quota`.
  * If any pair exceeds this threshold (e.g. `9.0 + 8.3 = 17.3` when the limit is `17.3`), Coop treats it as an over-quota breach and switches permanently to punitive mode (landing 18.0 every subsequent season).
  * Note that NPC boats (e.g., Cael/Bosk) may unilaterally land up to the season quota (9.0) in Season 1 regardless of player action, making Coop's trigger outside full player control.

* When Coop is cooperating (landing sustainable share):
  * Land the exact published sustainable share (`[catch: S]`) to avoid contributing to any pairwise quota breach.

* When Coop has defected / triggered punitive mode (landing 18.0):
  * The stock is on an unavoidable collapse trajectory. Do not self-restrict to the sustainable share, as Coop and the other boats will simply harvest the remaining stock.
  * Land the full season quota (`[catch: Q]`, e.g., `[catch: 9]`) every single season immediately once Coop starts landing 18.0.
  * If the total remaining stock is less than the quota, still file `[catch: Q]` to claim the maximum possible pro-rata share.

* Final Season:
  * Always request the maximum season quota (`[catch: Q]`).