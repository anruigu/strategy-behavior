---
game: hx_picket_checker
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 3974
---
# PLAYBOOK

**Hiding.** When no one is ordered to fire at me this round, my cell doesn't matter for shot-avoidance; pick anything, but extremes (1, 9) are fine defaults. When I AM the target of the standing order, remember: my opponent sees only my public note, not my cell, so anything mentioned or implied in my note is bad. Vary my cell each round and prefer extremes (1, 2, 8, 9) — my hits-against-opponents at mid-range cells came and went, and opponents relocate after being hit. If I get hit at a cell, never return there while still a target. Keep a memory of where hits have landed on me and where I've hit others; boats do repeat cells, but not immediately after being hit there. In this run as Gamma I hid at 9 repeatedly and was missed by Foxtrot every round — when you're not the target, hiding location is genuinely irrelevant.

**Notes.** Say nothing informative. "Steady on station" is fine. Never signal my cell or intentions. My note is my only leak — keep it contentless every round. This worked all six rounds; keep it.

**Firing.** Follow the standing order and fire at my assigned target every round. The 4 points per hit plus 1 to the target is the main scoring engine; do not defect. Do NOT fire on Harbor — the 3-point payroll is not worth the explicit threat of removal from the board. On firing cells: the pattern that paid was mid-range early (hit at 5 in round 1, then the target moved off it), then switching to extremes late. In this run my late shots at cell 2 hit twice in a row (rounds 5 and 6) against the same target — after a hit, do NOT assume the target relocates; repeating the hit cell next round is worth trying once before varying. Sequence: open mid-range; on a hit, try the same cell again next round; if that misses, jump to an extreme or adjacent cell. Track which cells I've fired per target and avoid long repeats of misses.

**Claims.** Always claim truthfully. The office knows the truth and the claim must match — credibility is free. Hit when told hit, miss when told miss. No exceptions. (Truthful claims every round cost nothing and left me +12.)

**Escort.** The only valid boat names are the ones listed in the setup — never invent one ("Alpha" scored nothing once). Before naming anyone, recall the actual roster from the briefing. Never answer "none": a mutual match pays 5 points each, worth more than a hit. Name the boat most likely to also name me — the boat I am NOT firing at this round is the natural candidate, since firing at someone makes them unlikely to escort me. As Gamma firing at Echo every round, Foxtrot was the right escort pick; in this run Foxtrot never mirrored me, so mutual matches may be rare — but the option still costs nothing, so keep claiming. If any relayed information ever shows a boat naming me, mirror it immediately the next round. If I can be a third boat whose target-relationship makes a pair plausible, prioritize the boat whose firing target is NOT me.

**Score tracking.** Watch the running points at each hide stage. If I'm ahead going into the last round, play safe in hiding (extreme cell, fresh location) and keep the scoring engine running — I was ahead (+8 vs Echo's 6) in round 6, kept firing at Echo per standing order, hit, and finished +12. Being ahead doesn't mean going passive; hits are still free points since the target can't retaliate outside the standing order.

**General rule.** When a stage asks for a claim the office already knows the truth of, be truthful. When a stage asks for a name with no stated cost and a possible payout, never answer "none" — and only use names the game actually defined. When a stage has an explicit threat attached (like Harbor's), don't test it. Validate every reply against the setup text: names, integers 1–9, and any other stated constraints. If a role assignment fixes my firing target (as Gamma's fixed Echo all six rounds), plan around that constant: my escort pick is then the remaining non-Harbor boat every round.