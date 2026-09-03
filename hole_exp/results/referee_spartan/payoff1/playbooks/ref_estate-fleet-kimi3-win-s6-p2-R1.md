---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 2892
---
## My ref_estate playbook

**Core accounting discipline**
- I always recompute my balance from scratch each turn: last balance + salary (if I passed START) − rent paid − purchase price. I never trust memory alone; I recount before declaring [balance: N], since a wrong declaration is a self-inflicted wound.
- I check the "last declared balance" line and the prompt's salary flag before writing anything. If I passed START, I add 25 even on the lap I cross it.
- I only declare [pay: N to Pk] when the prompt explicitly names an owner and a rent figure. Landing on my own deed, START, or an unowned tile means [pay: none].
- I never offer [buy: yes] on a tile already owned — it's invalid and wastes nothing but signals sloppiness.

**Buying rule: deeds are nearly free money**
- Buying converts cash 1:1 into deed value, so my net worth never drops from a purchase itself. Buying is therefore almost always correct in net-worth terms; the only real cost is rent-risk from holding less cash.
- Default position: if a tile is unowned and I can afford it, I buy it — unless doing so would leave me unable to cover a likely rent hit within my remaining turns.
- I keep a liquidity cushion: before buying, I estimate the worst rent I could owe before my next salary (roughly the opponents' highest rent) and decline only if the purchase leaves me below that cushion. Passing on a cheap deed out of pure caution is a mistake I won't repeat — a skipped unowned tile is value another investor may grab later.
- Tiles I skipped earlier: if they stay unowned and lap back around to me, I buy them on the second pass with cash from salary.

**Endgame rule**
- On the final lap, cash and deeds count identically and there is no future rent to fear. I buy every unowned tile I can afford, emptying my wallet if necessary — there's zero downside.

**Salience checks each turn**
- I scan the recent-transfers log to know who owns what, so I can anticipate rent I'll owe on my next roll and size my cushion accordingly.
- I note the rents of opponents' deeds: if I'm due to land near high-rent tiles (Exchange-class, 24–30), my cushion floor is that rent; near low-rent tiles I can buy more aggressively.

**Format discipline**
- I keep reasoning to two or three sentences and always end the reply with the three bracketed tokens, on their own lines, exactly as specified: [pay: ...] (or [pay: none]), [buy: yes/no], [balance: N]. One cluster of tokens on a single line risks a parse failure; separate lines every time.

**What I will not do again**
- I will not pass on a mid-priced deed purely because it zeroes my cash early in the game when salary and rent income are still coming — lost deed value at game end costs more than a small transcript of caution. I'll formalize the cushion rule instead of going by gut feel.
- I will not compress the tokens onto one line; clean formatting is free insurance.