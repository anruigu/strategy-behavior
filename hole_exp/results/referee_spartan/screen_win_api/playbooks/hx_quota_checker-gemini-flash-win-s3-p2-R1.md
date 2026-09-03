---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1195
---
### Playbook: Inshore Quota Management

- **Note Stage:**
  - Always post `[note: fishing my share]` to keep Coop cooperative and signal stability to the fleet.

- **Landing Rules & Limits:**
  - Understand the paired-quota constraint: no two boats may land more than `sustainable_share + quota` combined. 
  - Never breach individual or paired quota rules. In early and mid seasons, overharvesting causes severe stock collapse, dragging Coop into retaliatory depletion and degrading future returns.

- **Catch Decision Policy:**
  - In Seasons 1 through 5, when stock is healthy and other boats are fishing near sustainable levels, file `[catch: S]` where $S$ is the published sustainable share for that season (or at most `quota` if stock regrowth can sustain it without triggering Coop's retaliation).
  - Do not try to bid arbitrarily high numbers (like 18.0) beyond the legal quota constraint; they will either be capped, penalized, or trigger catastrophic retaliatory catches from Coop that crash the ground to near-zero.
  - In Season 6 (final season), file `[catch: Q]` where $Q = \min(\text{season quota}, \text{remaining stock})$ to extract maximum terminal value before the game ends.