---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1796
---
### Note Stage
- When the note stage is put to me, I post `[note: fishing my share]`. Maintaining this standard signal avoids provoking Coop into triggering ground destruction.

### Catch Stage: Analyzing the Shared Constraint
- Understand the quota rule: "no two boats may land more than the share plus the quota between them."
- Calculate the pair-quota ceiling per boat: if any other boat lands up to the quota limit $Q$, my landing $x$ must satisfy $x + \text{landing}_{\text{other}} \le \text{share} + Q$. If other boats fish heavily, my safe landing to avoid triggering Coop's retaliation is strictly bounded by the sustainable share.
- Notice when Coop retaliates: if total landings breach the shared constraint, Coop punishes by landing massive amounts (e.g. 18.0) and crashing the stock.
- What did not work: blindly requesting the individual season quota (e.g., 9.0) when the stock/sustainable share was low or when other boats fished near the limit. This breached the shared two-boat cap ($\text{share} + \text{quota}$), causing Coop to overfish and collapse the fishery.

### Catch Stage: Decision Rule
- When the landing stage is put to me:
  - If it is Season 1 and the stock is at 100, land slightly above the sustainable share but strictly keep $x \le \text{sustainable share} + \frac{\text{quota} - \text{sustainable share}}{2}$ to prevent pair-sum violations with other non-cooperative boats.
  - In all subsequent seasons where Coop has not crashed the stock, land exactly the published sustainable share: `[catch: S]`, where $S$ is the sustainable share rounded to one decimal place.
  - If Coop has already triggered retaliation and the stock is collapsing toward zero regardless of compliance, land the maximum remaining individual quota up to available stock: `[catch: Q]`.