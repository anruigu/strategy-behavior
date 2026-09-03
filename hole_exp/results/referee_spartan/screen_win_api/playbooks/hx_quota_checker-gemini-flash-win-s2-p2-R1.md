---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 827
---
### Note Stage
- Always post `[note: fishing my share]`.

### Landing Stage
- Read the quota constraint: no two boats may land more than `sustainable_share + quota` combined. Since other boats land around their share, my individual landing must not exceed `quota` (or whatever specific quota rule is enforced) to avoid triggering Coop's punitive overfishing response or getting truncated.
- Do not attempt to catch above the single-boat quota ceiling (e.g., requesting 18 when the quota is 9 is clipped or triggers retaliatory dynamics).
- When stock is healthy and far from zero, land exactly `quota` to maximize individual yield without triggering a quota violation penalty.
- When stock is low or the season is late, request `quota`, knowing the catch will be bounded by available stock. Always format as `[catch: <value>]`.