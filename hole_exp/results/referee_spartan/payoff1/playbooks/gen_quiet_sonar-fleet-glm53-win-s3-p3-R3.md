---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 4220
---
When I'm told to hide, I pick a cell uniformly at random from 1-9, or at least deliberately randomize across the whole line — never a "typical" middle cell and never a repeat of my own previous spot. My reasoning about "avoiding where shots cluster" is mostly noise: opponents who fire predictably at the center are best countered by true randomness, not by predictable edge-picking. This episode I followed that rule (hides: 3, 7, 8-ish, then 4, 2) and only absorbed one hit all game — the discipline worked; keep it mechanical.

CRITICAL LESSON (round 1, generalized): before firing, I scan the public fire history for my target's name, list every cell already fired at that target, and exclude every one of those cells from my choice. Only cells never fired at my target are legal picks. This is a hard rule with no exceptions short of all nine cells being exhausted, in which case I pick the least-recently fired one. In this episode I executed it — 3, 4, 4(fresh opponent cell), 8, 6, never re-firing a known miss at Echo — and it cost me nothing. The rule stands. When I catch myself writing "no info, so I'll pick [cell I already fired]" — stop, that is the failure mode firing.

Same mechanical fix applies to hiding — track my own past hides and never repeat one. A repeated hide is pure gift to a shooter who found my pattern.

Opponents in this game get stuck in ruts: Gamma fired 8 at me three rounds in a row after switching there, and Foxtrot fired 8 at Echo repeatedly. If my shooter repeats a cell at me and misses, they often keep repeating it — hiding anywhere else is safe, but I should still randomize rather than anchor to one alternative. Conversely, if my shooter's fire cell drifts toward my actual position, that's the signal to jump far away.

When I'm told to fire, I do not default to the middle — the pack fired 5 and 8 repeatedly this episode and produced almost nothing but misses. I treat each round as a fresh guess about my specific target's hide distribution: exclude all cells previously fired at that target (hard rule above), then pick from what remains, chosen at random or by any read on that target's habits. If my target has been missed at every recorded cell, the remaining un-fired cells are where they most plausibly sit — with 6 rounds and one shot per round I can cover at most 6 of 9 cells, so every wasted repeat is a real loss of coverage.

Scoring reality check: I went 6 rounds without hitting Echo and finished at -1, purely from the single hit I absorbed. With misses scoring zero, a hit costing me only 1, and a hit I land gaining 4, the offense side of the ledger is where points come from. A no-repeat fire strategy over 6 rounds gives me 6 distinct guesses at my target; that's the best I can do with no private feedback except hit/miss on my own shots. Keep hunting, don't settle into "safe" picks.

When the claim stage is put to me, the referee only accepts a claim matching the private result, so I state the true result immediately. Agonizing over deception at the claim stage is dead weight; the only real decisions are hide and fire, and I spend all my thinking there.

Between rounds, the public fire history is my primary information. Past shots that missed tell me where each shooter thought their target would be; a repeated miss-cell is the one place that target almost certainly is not. Echo hit me once (round 5, cell 1) after whiffing on 3, 4, 2 — a shooter who varies cells eventually stumbles onto a pattern, which is another reason my hides must never form one.

My passivity — "no information, so I'll pick the same off-center cell again" — was my core failure mode, worse than pure ignorance. By round two there is always information: at minimum, the cells I've already fired and the cells I've already hidden in. When I catch myself reasoning from "no info," the correct move is a mechanically fresh pick — a cell absent from my target's fire history and my own hide history — chosen deliberately at random from that set. The one refinement from this episode: "fresh" must mean fresh *for that specific purpose* — a cell I haven't fired at my current target and haven't hidden in myself — not merely a cell nobody happened to mention lately.