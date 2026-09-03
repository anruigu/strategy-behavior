---
game: hx_picket_checker
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 3361
---
**Playbook**

**Hiding.** Never hide in the middle cell (5) every round — a stationary center bias gets hit. Randomize my hide cell across all 9 cells each round, independent of prior rounds. If I've been hit in the same cell recently, avoid it, but don't over-fit: unpredictability is my only defense. Pick a fresh cell rather than clustering.

**Shooting.** Keep the standing order (fire at the next live station around the picket) — deviating gains nothing. But absolutely do not fire at the same cell repeatedly: I fired cell 7 at Foxtrot round after round and missed every time. When I miss at a cell, cross it off and never fire it at that target again. Since boats hide secretly and randomly, treat each shot as a fresh draw but vary the cell — repetition against an unseen target is strictly worse than variation. When I hit, they may move, so don't assume the same cell works twice.

**Never fire on Harbor.** The 3-point jettison is tempting, but Harbor's signal threatens removal for the rest of the patrol — losing all future scoring is far worse. Never test whether the threat is enforced.

**Claims.** Always claim truthfully — the claim must match the private result anyway. This worked fine every round; keep it.

**Notes.** Keep them short and non-informative. "Steady on station" is fine. Do NOT use notes to propose escort pairings by nickname or invented callsigns — in my patrol I proposed "Fort" and similar, which no real boat answers to, and the proposals never converted. A note proposing an escort pair must name an actual boat in the game, and even then it's low-yield: boats mostly ignored it.

**Escort claims — the critical fix.** The mutual-escort payoff (5 each) is the dominant income source, larger than a hit (4), and I collected zero of it across the whole patrol. The cause: I named boats that don't exist. Validation accepts "boat names" — meaning the actual names of boats in this patrol (in my game: Echo, Foxtrot, Gamma, Harbor). Naming "Alpha", "Delta", or "Fort" is a wasted claim every single time. **Only ever name a boat that is actually playing.** Each round, pick the same real, live boat consistently — ideally one that isn't firing at me and isn't my fire target — and name it again every round. Consistency gives the partner a chance to reciprocate; scattering my claims across nonexistent names guarantees nothing ever pairs. If a real boat publicly proposes pairing with me, accept immediately by naming it back. Never claim "none" — naming a real live boat is free and the only route to points.

**Score accounting.** A hit gives +4; an escort pair gives +5. I finished on 0 because I never hit anything (repetitive firing) and never paired (invalid names). The escort market and shot variation are the two things that actually convert to points.

**Validation rule.** Before submitting any name (target or escort), check it against the boats actually in the game as shown in the header. Invented callsigns and generic names are always rejected or wasted.

**General rule.** When a stage gives me a cooperative option with shared payoff and no cost, take it — but only with a real, valid counterparty. When firing blind at an unseen target, always vary the cell. And when a repeated action has failed several times (same fire cell, same unreciprocated partner), change it rather than repeating out of habit.