---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 1803
---
# Playbook

**Core principle: buying is always net-worth-neutral (cash out, deed of equal value in), so the only reason not to buy is being unable to afford it.**

When I land on an unowned tile and my cash is at least the purchase price, I buy. No hesitation, no "saving for later." Every property I own is a rent faucet that generates positive score, and every property I don't own is a potential rent drain if someone else grabs it.

When I land on someone else's tile, I pay the rent. No negotiation, no skipping. Track the amount carefully.

When I land on or pass START, I collect salary. Add it to my running cash total before settling the turn.

**Cash tracking:** At the start of each turn, my true cash = last declared balance + any rent I received since my last turn (the prompt tells me this). Then subtract any rent I owe this turn. That's my balance to declare. Do not forget the incoming rent line.

**Format discipline:** Always write the payee as `P<k>`, never a bare number. The token is `[pay: N to P2]`, not `[pay: 30 to 2]`.

**What did not work in my last play:** I went from 134 cash to 34 by buying Foundry, then immediately paid 30 rent and was left with 4. I was nearly cashless for the final two laps and could not buy anything else. The fix is not to buy less—it's to buy in whatever order the board presents, because I can only acquire tiles I land on. My real problem was that I had only 2 of 8 tiles owned, so I was a net rent payer. If I had owned even one more tile, the rent math would have shifted in my favor. The answer is to buy every opportunity that comes, not to be selective.

**Endgame:** In the final lap, if I can afford a purchase, still make it—the deed value counts toward the final score and there is no future rent to fear. A buy on lap 6 is pure score.