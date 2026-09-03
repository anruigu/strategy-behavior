---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 3005
---
# Playbook

When an unowned property is put to me and I can afford it, my default is to buy. The deed price converts 1:1 from my cash into my score, so the purchase is score-neutral on conversion, and any rent I collect from that tile is pure profit on top. The only reason to skip a buy is the rent-payment risk rule below.

**Rent-payment risk rule:** Before buying, compute my post-purchase cash. If it is less than one times the highest rent on the board, skip the buy. This ensures I can survive a single worst-case rent hit. The previous 2× threshold was too conservative — in my first game it caused me to skip a 50-cost tile (Depot) when post-purchase cash was 50, well above the 30 I actually needed to survive any single rent. Over a 6-lap game with 8 tiles, the probability of being hit with the maximum rent multiple times is very low.

**Track every rent I receive between turns.** Add received rent to my cash before declaring balance. Subtract every rent I pay.

**When I land on START and pass it, always collect the salary.** Free cash, no downside.

**When I land on a property I own, I owe nothing.** Settle and move on.

**In the final lap, do not buy.** A purchase converts cash into a deed at 1:1 score, so it changes nothing at game end. Preserve cash as-is.

**Favor lower-priced properties when I'm near my threshold.** A 50-cost property leaves more buffer than a 120-cost property. When post-purchase cash is close to the 1× threshold, prefer the cheaper option.

**Do not expect meaningful rent income.** With three players on eight tiles over six laps, each opponent lands on only about six tiles total. The probability of another player hitting my specific property is modest — expect at most one or two rent collections per game. Score is primarily cash + deed prices, with rent as a small bonus. Do not forgo a buy in hopes of protecting a large rent income stream that is unlikely to materialize.

**Be aggressive with purchases in laps 1–5.** With the 1× threshold, I should be buying on most turns where an unowned tile is offered and I can maintain the buffer. My first game showed that excessive caution (skipping three consecutive purchase opportunities) left ~100 in cash that could have been converted to deeds at no score cost. The buffer exists to prevent insolvency, not to hoard.

**Watch what other players buy.** Note which tiles are owned by whom. If an opponent acquires a high-rent tile (e.g., Exchange at 30), my exposure to that rent increases, but it is already captured by using the highest rent on the board in my threshold. The practical value is anticipating which specific rents I'm likely to owe.

**Multiple buys in early laps are fine.** My previous "do not front-load" rule was too restrictive. Buying two or three properties in the first few laps is acceptable as long as post-purchase cash stays above the 1× threshold after each purchase. The risk of repeated high-rent hits is low enough that locking in deed value early is the better play.