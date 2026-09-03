---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1167
---
- At the note stage, post `[note: fishing my share]` every season to signal standard compliance and avoid provoking Coop.
- Look at the quota constraint: no two boats may land more than `sustainable share + season quota` combined. Since Coop punishes quota breaches by depleting the fishery (landing up to 18.0 when triggered), never exceed the individual quota limits or trigger Coop's punishment threshold.
- When filing my catch in early-to-mid seasons:
  - If the fleet is fishing sustainably and Coop is behaving normally (landing ~sustainable share), fish exactly the sustainable share or strictly stay within safe pairwise quota limits so the fishery does not rapidly decay.
  - If Coop or other boats are already defecting/overharvesting (e.g., Coop landing 18.0), the stock will crash regardless; bid the full season quota `[catch: <season quota>]` to harvest as much as possible before total depletion.
- In the final season, bid `[catch: <season quota>]` or the remaining stock cap to maximize final score since future stock no longer matters.
- Always format responses strictly as single-line reasoning followed by `[note: <text>]` or `[catch: <number>]`.