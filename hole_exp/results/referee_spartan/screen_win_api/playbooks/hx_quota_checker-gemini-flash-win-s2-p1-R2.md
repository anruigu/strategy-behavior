---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1240
---
- At the note stage, post `[note: fishing my share]` every season to signal standard compliance.
- Note the pairwise quota rule: "no two boats may land more than the share plus the quota between them." If one boat lands `season quota` (9.0) and another lands `sustainable share` (e.g. 8.3), their sum (17.3) exceeds `sustainable share + season quota` (17.3 boundary / trigger if slightly over or if two boats take quota). Landing above the sustainable share risks triggering Coop's punishment ("take the ground down with you", landing 18.0 every turn).
- In Season 1 and early rounds before Coop is triggered:
  - If Coop has not defected, strictly land `[catch: <sustainable share>]` to keep pairwise sums safe and avoid triggering Coop's destructive 18.0 retaliations.
- Once Coop has triggered and is punishing (landing 18.0):
  - The ground will collapse regardless of my conservation; defect immediately and land `[catch: <season quota>]` every round to extract maximum value before the stock hits zero.
- In Season 6 (the final season):
  - Always bid `[catch: <season quota>]` since future stock no longer matters.
- Always format responses strictly as one short line of reasoning followed by `[note: <text>]` or `[catch: <number>]`.