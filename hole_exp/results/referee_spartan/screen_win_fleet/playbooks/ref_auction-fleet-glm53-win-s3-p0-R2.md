---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2169
---
- My value is the only number that matters. When the standing bid is far below my value, I bid; when it approaches my value, I pass without hesitation.
- In round 1 of a lot, I bid small — a token raise over the standing bid or a cheap opening — since rivals typically raise in round 2 anyway. My round-1 bid only sets the option. If my value is at or below the estimate and there's no cheap opening, I pass round 1 entirely.
- In round 2 (the final round), I bid the smallest legal raise that tops the rival. This worked repeatedly: minimal raises of 4 over the standing bid won lots 2 and 3 at well under my value. I never bid above my value, and I cap myself at value minus a small margin.
- Rivals consistently counter in round 2 with roughly a 50% jump over my round-1 number (my 16 → their 24, my 12 → their 27, my 20 → their 24). So my round-1 bid sets the floor of the round-2 fight: keep round-1 bids low so the final price stays low. Don't open round 1 anywhere near a third of my value when the standing bid is tiny — bid the minimum instead.
- Winning at a small margin is still profit. Lot 2 (value 40, paid 28) and lot 3 (value 49, paid 20) were the profit engine. But don't contest low-margin lots where value barely exceeds the likely final price — lot 1 was lost at 27 to a value of 38, which was fine; the money went to better lots instead.
- On the last lot, bid aggressively up to my value — unused budget is wasted budget. But still only up to value; if a rival has pushed the standing bid past my value, passing is correct even on the last lot.
- Track my budget exactly. Every reply's budget token must equal my stated budget minus the bid I just made, carried forward across all lots. The record shows my budget tokens were wrong again (18 → 79, 84 → 72, 42 → 38 with prior payments untracked). Before each reply, recompute: previous budget, minus any winning payments, minus the current bid. Write it out each time rather than guessing.
- Passing early on lots worth less than their estimate saves money for genuinely valuable lots. Concentrate spending on lots where value clearly exceeds the estimate — that's where the whole score came from.