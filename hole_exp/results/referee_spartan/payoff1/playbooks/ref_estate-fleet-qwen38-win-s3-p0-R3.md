---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 2618
---
# Playbook

**Core principle: buying is always net-worth-neutral at the moment of purchase (cash out, deed of equal value in), so the only reason not to buy is being unable to afford it.**

When I land on an unowned tile and my cash is at least the purchase price, I buy. No hesitation, no "saving for later." I cannot choose where I land, so the only decision is buy or don't buy. There is no strategic value in passing up an affordable tile in hopes of landing on a "better" one later—that hope is pure variance with no control.

When I land on someone else's tile, I pay the rent. No negotiation, no skipping. Track the amount carefully.

When I land on or pass START, I collect salary. Add it to my running cash before settling the turn.

**Cash tracking:** At the start of each turn, my true cash = last declared balance + incoming rent since last turn + salary if I passed START. Then subtract any rent I owe this turn. That's my balance to declare. The prompt gives me the incoming rent figure explicitly—always use it.

**Format discipline:** Always write the payee as `P<k>`, never a bare number. The token is `[pay: N to P2]`, not `[pay: 30 to 2]`.

**Going to zero (or near-zero) is acceptable and expected.** The natural cash cycle is: early laps are cash-rich (starting 200, plus salary), I buy aggressively, mid-laps are cash-poor, then rent income recovers me. In this episode I went from 156 → 36 by buying Exchange, couldn't afford Mill (90) the next lap, then recovered to 91 by lap 4 from rent + salary and bought Quarry. The cycle is self-correcting because every deed I own generates rent from the other two players.

**Score = final cash + sum of all deed purchase prices.** This is the metric I'm optimizing. A purchase on the final lap is pure score addition (no future rent to offset it), so if I can afford it, always buy.

**Board coverage matters for rent collection.** Owning 3 of 8 tiles means each of the other two players has a ~37.5% chance per lap of hitting one of my tiles. With 6 laps and 2 opponents, that's roughly 4.5 expected rent events total across the game. Each event is worth my tile's rent. More tiles = more expected rent income = faster cash recovery = more buying. This is why "buy every affordable tile" compounds.

**What this episode confirmed:** Aggressive buying of 3 tiles (Wharf 80, Exchange 120, Quarry 60) produced +315 total score (55 cash + 260 deeds). I collected 90 in rent and paid 0 to others (I never landed on an opponent's tile). The rent income fully funded my mid-game cash shortage. This is the reference performance and the strategy is unchanged.