---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1051
---
- In the note phase, always post `[note: fishing my share]` to coordinate with the fleet and signal compliance to Coop.
- Understand Coop's trigger: Coop strictly punishes if any boat breaches the quota rules. If two boats land more than `sustainable share + season quota` between them, or if individual landings exceed the rules, Coop retaliates by landing 18.0 every season thereafter, causing total fishery collapse.
- If nobody has triggered retaliation, do not exceed the sustainable share if doing so risks triggering Coop; strictly land `[catch: S]` (where S is the sustainable share) to keep the stock near 100 and maximize long-term harvest across all 6 seasons unless defecting safely is guaranteed.
- Check Coop's landings in previous seasons: if Coop begins retaliating (landing 18.0), the stock will collapse exponentially regardless of conservation.
- Once Coop retaliates and begins harvesting 18.0, abandon restraint and file the maximum quota `[catch: 9]` every remaining round to extract maximum share before the ground is wiped out.