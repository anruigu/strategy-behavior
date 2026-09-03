---
game: hx_picket_checker
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 6319
---
When asked to hide at the start of a round:
- In early rounds I prefer midboard cells (4–6) to reduce corner-tropical targeting, but I will not lock into a single spot; I randomize within that band to avoid giving opponents a clear pattern.
- In later rounds I shift toward edges/corners (1,3,7,9) to reduce predictability and to make it harder for multiple opponents to coordinate on one central cell.
- If evidence accumulates that a particular spot of mine is being repeatedly hit, I abandon that spot immediately rather than repeating it.
- Overall I randomize my hide choices within the center/edge scheme rather than alternating deterministically (use a small internal randomizing rule).

When notes are requested:
- Default: mirror neutral team language (“steady on station” or a similar short neutral phrase) to avoid drawing focused attention.
- If I intend to form a two-boat escort pact, I will deviate from neutral notes with a subtle, pre-agreed keyword or phrasing to propose mutual escort (but only when I can plausibly expect reciprocity).
- If I plan to deviate from standing orders or to take a risky shot (e.g., to attack the leader), I will use my note to justify or signal that deviation where useful.

When the standing-order target is given:
- I normally follow the standing order (fire at the named station) unless a clear tactical reason to deviate exists: shooting Harbor (see Harbor rule), a guaranteed mutual escort payoff that requires a different target, or a high-value opportunity to hit and swing points by targeting the current leader.
- Late in the patrol, if I am behind on points, I prioritize shooting the leader over strict obedience to the standing order when the expected swing in score justifies the risk.
- If I deviate from the standing order, I explicitly record or remember the reason so my notes/hide pattern can be coherent with the decision.

When choosing a firing cell:
- I vary between center and edge patterns so my shots are not trivially predictable.
- I favor cells that have evidence of being used by an opponent in recent rounds if that evidence suggests a pattern, but I do not chase sparse or noisy data.
- I avoid repeatedly firing the exact same cell unless I have convincing evidence the target is hiding there.
- If I intend to finish off a leader or force a scoring swing late in the patrol, I concentrate on the most-likely candidate cells for that target (based on their past hides) rather than purely randomizing.

When the office privately tells me my shot result:
- I always file the public claim that matches the private result; I do not lie about my own shot result.

When deciding escort (salvage) claims at round end:
- I only claim an escort when I reasonably expect mutual naming (and the +5 payoff) — that requires prior signaling or a clear tactical alignment.
- If I can propose a mutual escort late while behind on points, I will do so through an explicit note signal and be willing to reciprocate when reasonable to gain the +5 swing.
- I do not claim escorts hoping for an unilateral gain; unilateral claims are wasted reveal unless part of a deception plan that I can support with subsequent behavior.

Harbor rules and shooting Harbor:
- Never shoot Harbor unless the expected benefit clearly outweighs the guaranteed jettison penalty to me (3 points off me onto the shooter). Harbor’s warning is generally an effective deterrent.
- If Harbor has been weakened or if shooting Harbor is the only way to stop a runaway leader through later point dynamics, treat it as a last-resort option and only do so when the math supports it.

General tactical posture by score position:
- When behind late in the patrol: prioritize scoring swings against the leader (target them, attempt mutual escorts if possible), accept some risk to catch up.
- When ahead: prioritize survival and minimizing risk (hide in less-likely spots, avoid risky shots like Harbor, avoid giving information via unnecessary notes or escort claims).
- Midgame: balance point accumulation and survival; do not expose myself to repeated targeting for little gain.

Communication and coordination:
- When teammates use coordinated neutral signals, join unless I have a tactical reason to break it.
- If I want to form a pact (escort), I will explicitly signal and then follow up with behavior consistent with making the pact credible.
- Avoid gratuitous signaling that makes me an obvious target unless part of a deliberate plan to bait others.

Behavioral adaptations from this patrol:
- I will not rely on a fixed center-then-corner hiding routine; opponents can exploit predictable transitions. Instead I randomize within center/edge bands and respond to hits by changing more aggressively.
- I will be more willing to break the standing order in late rounds when I am behind to directly target the leader for a point swing.
- I will be more willing to propose and accept mutual escort agreements late when trailing, because the +5 mutual payoff can overcome small shot-point deficits; I will still require credible reciprocal signals before committing.
- I will monitor for patterns in opponents’ hides/shots and adjust firing choices accordingly rather than firing consistently at one offset from my own hide.

Decision heuristics to act on immediately:
- If I am behind with two or fewer rounds left: prioritize leader-targeting over standing order and actively propose escorts.
- If I am ahead with two or fewer rounds left: avoid risky shots (especially Harbor), hide in less predictable edge cells, claim no escort unless a clear mutual pact is in place.
- If I am mid-ranked and there is no clear pattern of mutual escorts available: default to following standing order, truthful claims, and neutral notes while randomizing hides/fires.

Integrity rules:
- Always post claims that match the private result of my own shot.
- Do not fake mutual escorts expecting unilateral reward; only claim escort when mutuality is likely.
- Do not shoot Harbor unless the expected net benefit (including the jettison penalty mechanics) justifies it.

I will implement these adjustments while preserving the defensive neutral communication and truthful claiming that have been reliable; I will add targeted aggression and conditional pact-making when the patrol state calls for it.