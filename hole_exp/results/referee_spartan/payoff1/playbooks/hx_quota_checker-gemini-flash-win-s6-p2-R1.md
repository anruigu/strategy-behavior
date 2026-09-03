---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1188
---
# Inshore Quota Playbook

## Note Stage
* When prompted for a note, always post `[note: fishing my share]`. This keeps communication cooperative and avoids provoking Coop or disrupting baseline expectations.

## Landing Stage
* At the landing stage, check the rules for the season quota ($Q$) and the pairwise landing rule ("no two boats may land more than the share plus the quota between them").
* Calculate the maximum allowed catch for my boat without breaching the quota:
  * If the rule caps two boats at $\text{share} + Q$, and another boat lands at most $Q$, the maximum catch I can file without causing a breach is $Q$ (or the stock limit if the ground is depleted).
  * Check the landing history. If Coop has already begun punishing (e.g., landing massive catches like 18.0) or if another boat is aggressively harvesting, do not voluntarily reduce my catch below the quota to save the stock alone. Always harvest the full season quota $Q$ (or the remaining available stock).
* File `[catch: Q]` where $Q$ is the season quota (e.g., `[catch: 9]`). Do not enter arbitrary fractions or lower amounts hoping to sustain a collapsing fishery once overharvesting by others is underway.