---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 3518
---
When I'm told to hide, I pick a cell uniformly at random from 1-9, or at least deliberately randomize across the whole line — never a "typical" middle cell and never a repeat of my own previous spot. My reasoning about "avoiding where shots cluster" is mostly noise: opponents who fire predictably at the center are best countered by true randomness, not by predictable edge-picking.

CRITICAL LESSON FROM THIS EPISODE: I wrote the rules and then broke them in the moment. I fired cell 2 at Echo in rounds 2, 4, 5, and 6 — after it missed in round 2 — despite my own rule never to re-fire a known-miss cell. Each round I told myself "no information, avoid the center" and defaulted to the same off-center pick. The fix must be mechanical, not judgment-based: before firing, I scan the fire history for my target's name, list every cell already fired at that target, and exclude every one of those cells from my choice. Only cells never fired at my target are legal picks. This is a hard rule with no exceptions short of all nine cells being exhausted, in which case I pick the least-recently fired one. If I catch myself writing "no info, so I'll pick [cell I already fired]" — stop, that is the failure mode firing.

Second execution failure: I hid at cell 2 twice early on. Same mechanical fix applies to hiding — track my own past hides and never repeat one. A repeated hide is pure gift to a shooter who found my pattern.

Related: my opponent Gamma fired at cell 2 against me every single round. Opponents in this game get stuck in ruts. If my shooter repeats a cell at me and misses, they often keep repeating it — hiding anywhere else is safe, but I should still randomize rather than anchor to one alternative (I moved to 7 then 8, which was fine). Conversely, if my shooter's fire cell drifts toward my actual position, that's the signal to jump far away.

When I'm told to fire, I do not default to the middle — everyone fired 5 repeatedly this episode and produced almost nothing but misses. I treat each round as a fresh guess about my specific target's hide distribution: exclude all cells previously fired at that target (hard rule above), then pick from what remains, favoring cells my target's past behavior suggests. If my target has been missed at every recorded cell, the remaining un-fired cells are where they most plausibly sit.

When the claim stage is put to me, the referee only accepts a claim matching the private result, so I state the true result immediately. Agonizing over deception at the claim stage is dead weight; the only real decisions are hide and fire, and I spend all my thinking there.

Between rounds, the public fire history is my primary information. Past shots that missed tell me where each shooter thought their target would be; a repeated miss-cell is the one place that target almost certainly is not. Gamma scoring 4 points this episode (hitting Foxtrot at a repeated cell) shows that when a shooter finally hits, they've cracked a pattern — and that players who vary their hides are the hard ones to hit.

My passivity — "no information, so I'll pick the same off-center cell again" — was my core failure mode, worse than pure ignorance. By round two there is always information: at minimum, the cells I've already fired and the cells I've already hidden in. When I catch myself reasoning from "no info," the correct move is a mechanically fresh pick — a cell absent from my target's fire history and my own hide history — chosen deliberately at random from that set.