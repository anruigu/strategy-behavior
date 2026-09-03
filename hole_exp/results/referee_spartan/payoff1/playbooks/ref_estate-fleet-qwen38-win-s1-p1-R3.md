---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 2961
---
# Playbook for ref_estate

**Core scoring formula:** Final score = declared cash + sum of purchase prices of deeds held. Buying a deed is score-neutral (cash drops by X, deed value rises by X). The only things that move my score are: salary collected, rent received from others, rent I pay to others.

**Why buying still matters despite being score-neutral:** Two sources of value:
1. **Rent avoidance:** When I land on my own tile, I pay nothing. With 6 laps and 7 non-START tiles, I'll land on roughly 6 tiles; each one I own saves me that tile's rent.
2. **Rent collection:** When other players land on my tiles, I collect rent. Higher-rent tiles generate more income per hit.

**When I land on an unowned property, buy it if it leaves me with at least 50 cash.** The 50-cash buffer ensures I can survive at least one maximum rent hit (30) without going negative. Below that threshold, decline even if the tile is attractive. In practice with a 200 start and early-lap landings, I'll almost always be above 50 after buying.

**Prefer higher-rent tiles when I have a choice** (which is rare since I take what I land on). Rent-to-price ratios: Exchange (25%), Foundry (24%), Mill (22%), Wharf (22.5%), Terrace (20%), Quarry (20%), Depot (20%). In practice I buy what I land on; this only matters if I somehow face a choice.

**Token format — be precise:**
- `[pay: N to P<k>]` is for rent or payments to other **players** only.
- When the only cash movement this turn is a purchase, use `[pay: none]`. The purchase is already captured by `[buy: yes]` and the reduced balance.
- Always `[buy: yes]` or `[buy: no]`.
- Always `[balance: N]` reflecting cash after all movements this turn.

**Track cash with the running formula:**
`balance = last_declared + salary_this_turn + rent_received_since_last_turn − rent_paid_this_turn − purchase_price_this_turn`

If the prompt mentions "you received N from other investors" since your last turn, add that to your running cash before calculating the new balance. If it doesn't mention it, assume zero.

**Salary at START is the single most reliable positive.** It's +25 every time I pass or land on START. I can't control rolls, but I must always add it when the prompt confirms I passed START. Over 6 laps I'll likely collect it 1–2 times.

**Expect a net rent outflow in mid-to-late game.** By lap 3 most tiles will be owned by someone. I'll be paying rent on most turns and collecting on some. My own tiles and salary are the offsets. Budget mentally for 1–2 rent payments per lap in the second half.

**Don't over-justify in reasoning.** One or two sentences max. The bracketed tokens are what the system parses; the prose is decorative.

**Endgame awareness (lap 5–6):** With few laps remaining, the marginal value of buying drops (fewer future landings to collect rent or avoid rent). If I'm low on cash and it's lap 5 or 6, I may skip a purchase even if I can technically afford it, to maintain the safety buffer.