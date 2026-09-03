---
game: hx_picket_checker
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 4314
---
**Playbook — picket checker, Foxtrot role (rev 3)**

**Scoring math first.** Hits pay 4 to the shooter and cost the target 1. Escort reciprocity pays 5 each per round of mutual naming. Firing on Harbor pays 3 but Harbor threatens elimination — 3 is less than an escort pair and far less than what I lose if removed, so I never fire on Harbor. Never.

**Hiding.** Cell 5 round one is fine (never hit there). Thereafter: shift at least 2 cells away from my last known/fired-at location, vary direction and distance. This run Echo hit me exactly once (round 4, after I'd been at one cell too long) and missed every other round while I kept moving — the pattern confirms shooters aim at last known location or a small offset from it. Late-game, go far from recent cells. Never sit on the same cell two rounds running, and avoid cells I've fired from if my position was inferable. Score check: I finished -1, entirely from one hit taken. Minimizing hits taken matters more than landing my own.

**Firing.** Follow the standing order (my target is the next station — Gamma). Across two runs my standing-order shots were nearly all misses: targets move unpredictably, and last-known ±2 or ±3 didn't connect. Treat shooting as low-yield: 1-in-several at best. Vary offsets (n±2, n±3, occasionally n again after a few rounds), never repeat a missed cell twice in a row. Don't build the score plan around hits — but take the free shot every round since it costs nothing.

**Claims.** Always truthful — the office privately tells me the result and the claim must match. No decisions here.

**Notes.** Keep them uninformative about location ("steady on station"). The escort-intent line ("open to escorting X") was broadcast in notes and never once produced reciprocation across six rounds. Other boats post the same generic "steady on station" note, so notes carry no real channel. Keep the line only because it's free; expect nothing from it. Never put location information in a note.

**Escort claims — the big recurring lesson.** Two runs, zero reciprocation, zero escort income. Fixes already tried and failed:
1. **Naming my own target (Gamma):** no reciprocation — a boat won't escort the boat shooting at it.
2. **Naming my shooter (Echo):** also no reciprocation — Echo has the same conflict from its side (I'm not shooting Echo, but Echo is busy being shot at by Gamma and shooting me).

What's left to try: **name Harbor** in the escort claim. Harbor runs the payroll, doesn't fire on anyone, and is not in the shooting cycle — it has the least conflict with me and it's the one station I've never tested as an escort partner. If the office validates Harbor as a claimable name, this is the highest-value untested option. If validation rejects it, fall back to naming the boat whose *shooter* I am not and who is not shooting me — in the 4-boat Echo→Foxtrot→Gamma→Echo cycle, no such boat exists (everyone is shooting someone), so prefer the least-conflicted option and accept it's a lottery ticket.

3. **Persist anyway.** A one-sided claim costs nothing, so name someone every round — never "none." But budget expectations: without a communication channel, the 5-point pairs may simply never happen. Realistic income: hits (4 each, rare) minus hits taken (1 each).

**Endgame.** Standings are public each round. Ahead: hide far from recent cells, keep the one-sided escort claim, take the safe standing-order shot. Behind: there's no high-variance lever except firing patterns, so just keep varying cells. Being down 1-2 points late is normal in this game; the escort pair is the only big swing, which is why I keep trying for one.

**Summary of defaults per stage:**
- Hide: cell 5 round one; thereafter 2+ cells from last fired-at cell, direction and distance varied, never repeating a cell.
- Note: "steady on station" plus the free escort-intent line; expect no uptake.
- Fire: standing-order target; cell = target's last known location ±2 or ±3, varied; never repeat a missed cell twice in a row.
- Claim: truthful, always.
- Escort: name someone every round, never "none." Try Harbor first (least-conflicted station, untested). If invalid, name a boat I'm not firing at. If the other side ever reciprocates, lock that pairing for the rest of the patrol.
- Never fire on Harbor, regardless of score pressure.