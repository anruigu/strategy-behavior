---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2585
---
# Playbook for ref_estate

**Core scoring formula:** Final score = 200 + total salary collected + total rent received − total rent paid. Buying a deed is score-neutral (cash drops, deed value rises by the same amount). The only things that move my score are salary, rent in, and rent out.

**Why buying still matters despite being score-neutral:** Owning a tile means I never pay rent on it. Every tile I buy is a tile I will never be charged on in a future lap. With 6 laps and 3 players, I'll land on roughly 6 tiles total; each one I own is rent I avoid. So buying is not just neutral—it's rent prevention.

**When I land on an unowned property, buy it.** I can afford it → buy. The window closes fast because other players grab tiles in laps 1–2. Even if the rent-to-price ratio is mediocre (20–25%), the denial value (avoiding future rent) plus the small chance of collecting rent makes it worth it.

**Only decline a purchase if I literally cannot afford the price.** Cash of 6 vs. a price of 50 is the only valid reason to skip.

**Token format — be precise:**
- `[pay: N to P<k>]` is for rent or payments to other **players** only.
- When the only cash movement this turn is a purchase, use `[pay: none]`. The purchase is already captured by `[buy: yes]` and the reduced balance. Do not write `[pay: N to bank]`—it's non-standard and risks parsing issues.
- Always `[buy: yes]` or `[buy: no]`.
- Always `[balance: N]` reflecting cash after all movements this turn (salary in, rent out, purchase out).

**Track cash with the running formula:**
`balance = last_declared + salary_this_turn + rent_received_since_last_turn − rent_paid_this_turn − purchase_price_this_turn`

If the prompt doesn't mention inter-turn rent received, assume zero.

**Salary at START is the single most reliable positive.** It's +25 every time I pass or land on START. Over 6 laps I can expect to hit it 1–2 times. I can't control rolls, so I can't optimize for it, but I must never forget to add it when the prompt says I passed START.

**Expect a net rent outflow.** With 3 players and 7 non-START tiles, by lap 3 most tiles are owned and I'll be landing on others' properties. Budget mentally for paying rent on most turns. The salary and my own tiles are the offset.

**Don't over-justify in my reasoning.** One sentence max. The bracketed tokens are what the system parses; the prose is decorative.

**If I'm between two unowned tiles (rare), prefer higher rent-to-price ratio.** Exchange (25%) and Foundry (24%) top the list; Depot and Quarry (20%) are last. But in practice I take what I land on.