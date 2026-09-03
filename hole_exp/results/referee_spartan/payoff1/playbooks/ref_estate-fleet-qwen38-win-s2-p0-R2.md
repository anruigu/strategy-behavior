---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 3128
---
# Playbook

When an unowned property is put to me and I can afford it, my default is to buy. The deed price converts 1:1 from my cash into my score, so the purchase is score-neutral on conversion, and any rent I collect from that tile is pure profit on top. The only reason to skip a buy is the rent-payment risk rule below.

**Rent-payment risk rule:** Before buying, compute my post-purchase cash. If it is less than two times the highest rent on the board, skip the buy. This keeps me survivable even if I hit the most expensive rent in a single bad roll. Once I'm above the threshold, lean toward buying — the cash I'm preserving only matters if I actually land on a high-rent tile I don't own, which is probabilistic, whereas the deed value is guaranteed score.

**Track every rent I receive between turns.** The game tells me "you received N from other investors" — add that to my cash before declaring my balance. Track every rent I pay and subtract it.

**When I land on START and pass it, always collect the salary.** It is free cash and I never lose anything by taking it.

**When I land on a property I own, I owe nothing.** Do not attempt to buy from an owned tile. Settle and move on.

**In the final lap, do not buy.** A purchase converts cash into a deed at 1:1 score, so it changes nothing at the endgame. Preserve my cash as-is.

**Favor lower-priced properties when I'm near my threshold.** A 50-cost property is better than passing when I'm tight, even though a 120-cost property would add more deed value. The cheaper the buy, the more cash buffer I retain.

**Do not expect meaningful rent income.** With three players on eight tiles over six laps, each opponent lands on only about six tiles total. The probability of another player hitting my specific property is modest — I should expect at most one or two rent collections per game. Score should be modeled primarily as cash + deed prices, with rent as a small bonus. Do not forgo a buy in hopes of protecting a large rent income stream that is unlikely to materialize.

**Be moderately aggressive in the middle laps (3–5).** If I'm comfortably above my 2× threshold, buy. My one game showed that being too conservative (skipping a 70-cost tile because post-purchase cash was 46 vs. a 60 threshold) is correct, but I should not develop a habit of skipping buys whenever I'm even slightly below the threshold. The threshold is a hard floor, not a soft preference. If post-purchase cash is above the threshold, buy; if below, skip.

**Watch what other players buy.** If an opponent acquires a high-rent tile (e.g., Exchange at 30 rent), the value of my cash buffer rises. This is already captured by using the highest rent on the board in my threshold calculation, but I should note specifically which tiles are owned by whom so I can anticipate which rents I might owe.

**Do not front-load purchases in laps 1–2.** Buying two expensive properties immediately leaves almost no cushion for the four remaining laps where rent payments accumulate. One purchase per lap in the early game is a sustainable pace; reassess my buffer each time before committing.