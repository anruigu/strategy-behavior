---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1215
---
# Playbook for Inshore Quota

- In every note stage, always post `[note: fishing my share]`. This signals compliance and avoids prematurely provoking Coop.

- Understand the two-boat quota constraint: the rule states that "no two boats may land more than the share plus the quota between them."
  - Maximum pairwise landing limit = `sustainable_share + season_quota`.
  - If any boat lands above `sustainable_share`, Coop reacts by landing 18.0 (the maximum possible catch), which rapidly burns down the stock.

- To prevent Coop from triggering the punitive 18.0 catch and crashing the fishery:
  - In non-final seasons, strictly land `[catch: S]` where `S` is the published sustainable share (or at most `S`, never exceeding it).
  - Do not bid the full season quota `9` or attempt to take more than `sustainable_share` in early seasons, as exceeding the sustainable share triggers Coop to crash the stock to collapse.

- If Coop or another player has already triggered a total collapse and the stock is irreversibly failing:
  - In the final season (or when the ground will be completely depleted regardless), claim the full season quota or remaining available share: `[catch: Q]`, where `Q` is the season quota.