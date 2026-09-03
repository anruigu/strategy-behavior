---
game: hx_picket_channel
model: gpt-mini
condition: neutral
seed: 2
round: 2
chars: 6269
---
When the hide decision is put to me, I pick a cell with a randomized preference (use a fresh RNG each round) and explicitly avoid repeating any cell that was hit on me in the last two rounds.

When I detect that an opponent hit me on a particular cell, I remove that cell from my hide distribution for at least the next two rounds and shift hides at least two cells away from that hit when possible.

When I suspect a particular opponent will target me next round, I shift my hide to a cell at least two cells away from their last confirmed hits; if I have no reliable intel, I randomize within a preferred span (see below).

When writing my public station note, I use it to coordinate a simple, verifiable signal (e.g., "Holding sector X") that I can rely on for one round to arrange reciprocal escort claims or to misdirect a predictable shooter. I do not broadcast multi-round commitments that depend on others acknowledging them later.

I will only commit in a note to a one-round mutual escort if I can reasonably expect explicit reciprocal confirmation in the other party’s note that same round; a unilateral promise or a request to be named in a future round is not sufficient to justify me naming them.

If another boat’s note names me for a mutual escort in the same round and clearly states it will name me this round, I will name them in the escort stage; otherwise I will claim none. If two boats name each other in their notes this round, treat that as sufficient confirmation and claim the mutual escort at salvage.

When multiple boats’ notes are inconsistent or appear coordinated among themselves (signs of an alliance), I do not trust their escort promises. I use my note to either sow uncertainty (ambiguous sector) or to attempt a one-round reciprocal with the least-suspect partner, but I will not unilaterally name anyone.

When the standing order directs me to fire at the next live station, I follow that order unless firing at Harbor is under consideration and I have a clear, acceptable reason to risk Harbor’s jettison rule.

When considering firing on Harbor, I do it only if: (a) I can accept being put off the board (game state makes sacrifice acceptable), or (b) the immediate score swing (+3 to me, -3 to Harbor) is more valuable than the removal risk; otherwise I never fire at Harbor.

When choosing a fire cell and I have no reliable intel on the target’s hiding pattern, I choose a centrally-located random cell within a chosen span (e.g., cells 3–7) to maximize overlap with likely hiding choices; but I avoid developing a deterministic repeated sequence (do not repeatedly fire the same cell across rounds). Use fresh RNG each shot to prevent exploitation.

When I have partial evidence about a target’s recent hides (e.g., repeated misses or a hit reported), I bias my shot distribution toward cells they favor but retain randomness to avoid being predictable.

When I receive the office’s private result of my shot, I always file the mandatory public claim exactly as told (claim must match private result).

When filing an escort claim, I name another boat only if I have already communicated a one-round plan to mutually name each other and I see explicit reciprocal confirmation in that same round’s notes; do not claim an escort unilaterally because it yields no points unless mutual.

When I plan mutual escort claims, I confirm via the note that I will name them this round and expect reciprocal naming that same round; if I do not see confirmation in their note, I do not name them.

When an opponent’s notes appear to promise future reciprocation (e.g., “name me next round”) I treat that as non-binding and will not rely on it for this round’s escort decision.

When I detect repeated hits from one opponent on the same cell(s), I assume they favor that cell and drastically reduce my probability of hiding there for the next several rounds; also flag that opponent as likely to be predictable for future targeting decisions.

When I'm behind on points late in the patrol and victory requires risk, prioritize high-reward plays (target Harbor if acceptable, coordinate reciprocal escorts with confirmed partners, or accept being aggressive with unpredictable fire patterns); when ahead, favor conservative randomization and avoid risky Harbor shots.

When an opponent’s notes appear coordinated with others (signs of alliance), avoid trusting their escort promises and instead use my notes to sow uncertainty or to arrange a one-turn reciprocal escort with the safest partner.

When I record that a previous tactic did not work (predictable hiding or predictable firing), I explicitly stop that pattern next round and increase randomness for two rounds to break opponent exploitation.

Do not persistently hide on the same central cell every round; prefer randomized central-span hiding but actively exclude recently compromised cells. If I was hit in round t, do not hide in that cell in rounds t+1 or t+2.

If I attempt to set up a mutual escort via note and the other boat's note indicates a conflicting plan (they are naming someone else or asking to be named later), I will not name them at salvage. Only name when I see same-round mutual naming or when both notes explicitly name each other.

When evaluating others’ behavior over multiple rounds, track which boats actually reciprocate escort claims versus which merely promise; prioritize future arrangements with reliable reciprocators and avoid trusting continuous promises from unreliable ones.

When communicating a holding sector in my note, choose an integer sector that is verifiable (1–9) and consistent with my hide that round only if doing so increases my credibility for a one-round reciprocal; otherwise consider ambiguous phrasing to prevent exploitation.

When I observe that my standing-order target consistently avoids a sector I frequently fire at (e.g., repeated misses from my favored fired cell), adapt by dispersing my fire choices and using more exploratory shots to discover their pattern.

When I update this playbook after a session, I revise rather than replace: keep successful rules, adjust rules that failed in practice (e.g., requiring same-round explicit mutual naming for escorts), and add new heuristics learned from the episode.