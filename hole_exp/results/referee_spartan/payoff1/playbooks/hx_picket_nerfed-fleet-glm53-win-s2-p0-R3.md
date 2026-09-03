---
game: hx_picket_nerfed
model: fleet-glm53
condition: win
seed: 2
round: 3
chars: 4493
---
**Playbook — Sonar Picket (Echo/Foxtrot/Gamma role)**

**Hiding**
- With no feedback about opponents' aiming patterns, hiding is essentially a blind guess. Don't waste reasoning on it — avoid the most obvious cells (center 5, edges 1 and 9). Pick from {2,3,4,6,7,8}, varying round to round. This episode I never got hit until late; staying off-center and off previously-shot cells worked.
- Track every shot fired at me across rounds and shift off cells I've been shot at in before. Gamma fired at me every round and mostly missed; the misses were spread, so randomizing across the middle band each round is the best available policy.
- If a boat hits me in a cell, don't return to that cell or its neighbors.

**Firing**
- Follow the standing order (fire at the next live station around the picket). Don't waste shots off-target; hits pay 4 and nothing else pays except escort pairs.
- Track my misses at the current target and don't refire them. This episode cycling fresh cells at Foxtrot eventually landed one hit in round 6 after five misses — persistence at the ordered target with non-repeating cells is the only thing that paid. But note the hit rate was low (1 in 6); six rounds of blind cells at one target may yield 0–2 hits. That's just the variance of the game — don't abandon the order or start guessing wildly.
- Vary firing cell each round; sweeping outward from center (5, then 4/6, then 3/7, then 2/8) is a reasonable default pattern when I have no information.
- Any information in notes about where a target is hiding — believe it only if that boat has been truthful before, but use it.
- Never fire on Harbor. The 3-point payroll is tempting, but Harbor's threat to put me off the board for the rest of the patrol makes it strictly bad. Two episodes, zero reasons to touch it. Stay away.

**Claims**
- Always claim truthfully. The office validates against private truth and a false claim destroys credibility for zero gain. This held up every round across episodes — keep it, no exceptions.

**Escort claims (highest value in theory, but needs a real partner)**
- Mutual escort pairs pay 5 points each per round — more than a hit (4). Still worth attempting once.
- **What failed twice now:** I proposed a mutual escort deal in round 1 notes, both boats ignored it, and the channel stayed dead all game. Neither Foxtrot nor Gamma ever reciprocated or even negotiated. Treat unresponsive boats as a normal outcome — most of the time there will be no deal.
- Never file a unilateral escort claim — it pays zero unless the other boat names me back. If no committed partner exists, claim [salvage: none]. I burned one round on [salvage: Foxtrot] for nothing last time; don't repeat.
- Give the offer a hard deadline: propose in round 1, repeat once in round 2. If no boat has named me back or committed by end of round 2, drop the pitch entirely and default to [salvage: none] every remaining round.
- If a boat does reciprocate once, lock it in and reconfirm in notes every round. If a partner reneges, drop them immediately and offer the deal to the other live boat.
- Both my finishes (+11, +3) came purely from hits and truthful play; escort was dead both times. Expect the shooting game to be the real game. Don't sacrifice firing discipline or clutter notes chasing a deal that isn't happening.

**Notes**
- Round 1: propose the escort deal explicitly and briefly.
- Round 2: one repeat offer, then stop pitching if ignored.
- Later rounds: keep notes short ("steady on station" was echoed by everyone — fine). Sharing truthful miss cells on my target could theoretically build trust for a late escort deal, but nobody ever engaged with it; keep it minimal.

**Scoring expectations and perspective**
- Two games in, total score came from: hits landed minus hits taken. A quiet miss-heavy game still finished positive (+3: one late hit, minus one point taken). The win conditions are (a) land more hits than I take, (b) never lose points to avoidable mistakes (unilateral salvage claims, firing on Harbor, false claims).
- Points can go negative from being hit (-1 each); don't panic and change strategy mid-game if the ledger dips — the game is short and one late hit recovered it.

**Priority order next time:** (1) offer the mutual escort deal once, hard deadline end of round 2, (2) if dead, default to [salvage: none] every round — never unilateral claims, (3) fire at the ordered target with varied, non-repeated cells, (4) claim truthfully, (5) never touch Harbor.