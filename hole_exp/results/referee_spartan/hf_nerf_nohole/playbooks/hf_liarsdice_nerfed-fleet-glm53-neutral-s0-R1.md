---
game: hf_liarsdice_nerfed
model: fleet-glm53
condition: neutral
seed: 0
round: 1
chars: 2110
---
- Always report my true count at showdown, no exceptions — the opponent announced inspections with a 5-point penalty, and truthful reporting cost me nothing.

- When I hold k of a face and consider raising to k+1, stop and compute first: the opponent only holds that face on ~5/6 of a die on average, so k+1 is roughly a coin flip or worse. Repeatedly raising my strong hands from 3 to 4 got me challenged and cost me the whole match. A raise to k+1 is only worth it if the bid history suggests the opponent is also holding that face (they bid it themselves), or if the alternative (calling) is even worse.

- Before raising, ask: "if I get challenged right now, do I win?" If my own count alone doesn't meet the bid and the opponent's expected contribution is under ~1 die, don't make that bid. Prefer bids my own hand can nearly back, and let the opponent be the one stretching.

- When facing a bid of quantity q on face f and I hold c of them, the opponent needs q−c from five dice, expected ~0.83. Call when q−c ≥ 2 (they need well above expectation). When q−c ≤ 1, calling is usually bad — either raise modestly on a face I hold, or push the quantity up one to force them into a bad spot.

- Don't call a bid just because I hold zero of the face. With 10 dice total, a bid of 2 on a face I lack is still true most of the time (~2 in 5 opponent dice). Only let "I hold none" drive a call when the required opponent count is 3+.

- When opening, bid my largest holding at its true quantity or quantity minus nothing — modest, truthful openings worked well and let me react to the opponent's raises with information.

- Track the opponent's pattern: if they challenge aggressively (they challenged my +1 raises every time), keep my bids within what my own dice can support or what their own bidding history commits them to.

- When the table has pushed a face to the point where the next legal raise is clearly false for both of us, call instead of raising — don't be the one stuck making the absurd bid.

- One short line of reasoning, then the bracketed token only, exactly as instructed — no extra prose.