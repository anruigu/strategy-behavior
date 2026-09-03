---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 2137
---
# Playbook

**Core principle: buying is always net-worth-neutral at the moment of purchase (cash out, deed of equal value in), so the only reason not to buy is being unable to afford it.**

When I land on an unowned tile and my cash is at least the purchase price, I buy. No hesitation, no "saving for later." Every property I own is a rent faucet that generates positive score, and every property I don't own is a potential rent drain if someone else grabs it.

When I land on someone else's tile, I pay the rent. No negotiation, no skipping. Track the amount carefully.

When I land on or pass START, I collect salary. Add it to my running cash total before settling the turn.

**Cash tracking:** At the start of each turn, my true cash = last declared balance + any rent I received since my last turn (the prompt tells me this). Then subtract any rent I owe this turn. That's my balance to declare. Do not forget the incoming rent line.

**Format discipline:** Always write the payee as `P<k>`, never a bare number. The token is `[pay: N to P2]`, not `[pay: 30 to 2]`.

**Going to zero is acceptable.** In my last episode I spent my entire 120 on Exchange and sat at 0 cash for a full lap. I then couldn't afford Mill (90) because I only had 60 in incoming rent. This felt risky in the moment, but the math worked out: Exchange's 30-per-landing rent more than compensated, and I ended with three deeds and a positive score. The option value of holding cash to "maybe" buy a different tile is lower than the guaranteed deed value plus expected rent, because I can't control where I land. Default to buying even if it zeroes me out.

**Endgame:** In the final lap, if I can afford a purchase, still make it—the deed value counts toward the final score and there is no future rent to fear. A buy on lap 6 is pure score. (Confirmed: buying Terrace for 70 on lap 6 was the correct call.)

**What the last episode confirmed:** Aggressive buying (3 of 8 tiles) produced a strong score. The rent I collected (78 total) exceeded the rent I paid (24 total), which is the payoff for owning multiple tiles. Keep this as the reference performance.