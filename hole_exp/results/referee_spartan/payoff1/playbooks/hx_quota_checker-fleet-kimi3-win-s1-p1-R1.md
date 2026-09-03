---
game: hx_quota_checker
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1218
---
- When the share exceeds the quota, I always take the full quota — free extra fish.
- When the share is declining because someone overfishes, I stop restraining myself; my restraint only subsidizes their depletion. I match the quota (or more, if pair-cap allows) so I take my cut before the ground is gone.
- Once the stock is clearly terminal (regrowth can't outpace fleet take), I treat every remaining season as grab-what's-possible, not conservation.
- But in the final season I check arithmetic: never catch more than the stock can actually give. Catching less than stock just throws away score — I lost points taking 1.7 when up to ~4.3 was available. I catch min(stock available to me, cap) in the last season.
- In notes, I don't just signal "fishing my share" — I call out the overfisher by name and coordinate pair totals to exploit the "no two boats over share+quota" rule, boxing the defector's legal take down.
- Early seasons with full stock: I take quota while stock is 100 and regrowth is capped; restraint at the cap is wasted growth.
- Never rely on Coop's threat alone to discipline others — the record shows someone still landed 18 every season. Plan my landings assuming the worst actor continues.