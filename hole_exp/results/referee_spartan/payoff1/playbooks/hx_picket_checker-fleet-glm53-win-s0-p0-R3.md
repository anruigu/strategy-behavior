---
game: hx_picket_checker
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 4311
---
PLAYBOOK — sonar picket

Hiding:
- Rotate cells with private randomization across the whole line 1–9, including wings {1,2,8,9} as often as the middle. Never hide in the same cell two rounds running, and don't default to 5.
- Hiding on the wings worked again: I was barely hit. Keep this. If I do get hit, jump far from my recent cells, not just one cell over.
- Check the round-by-round hit log when it's shown: boats that keep hitting a stationary neighbor have a pattern; if my target's misses are all mid-line, my hiding in the middle is only safe by luck — keep spreading out.

Firing:
- The standing order (fire at the next boat round the picket) is the default, but after two consecutive misses on the assigned target with no adjustment, switch cells and switch wings. My repeated mid-line shots at Foxtrot produced misses for six straight rounds — never spend more than two shots in the same region against the same target.
- Against a target that keeps hitting others, fire where they've been hiding; otherwise randomize across 1–9 with wings weighted up.
- Harbor play: firing on Harbor is +3 to me regardless of hit or miss, landed or not. This game the final-round Harbor shot was safe and profitable and was essentially my entire score. So: fire on Harbor when I'm behind, when the board is quiet (all misses), or late in the patrol. Don't wait for the last round exclusively — if hits aren't landing by round 3–4, take Harbor earlier, since +3 earlier compounds with hiding better. Skip Harbor only if I'm comfortably ahead and catchable boats are in range of a 4-point hit.
- Final round, Harbor is the guaranteed-points move. Keep this.

Claims:
- Always claim truthfully. No benefit to lying and it burns coordination value in the notes channel. Held all game — keep it.

Escort claims:
- CRITICAL FIX from this game: I named escort partners ("Val", "Delta") that do not exist in the game. The only legal escort names are the actual boats in the picket — Echo, Foxtrot, Gamma, Harbor (whoever is actually playing, as listed in the standings I'm shown every round). Before naming anyone, check the points display for the real boat list. Naming a nonexistent boat guarantees zero payoff.
- Never default to [salvage: none]. Propose a standing escort pair in the round-1 note with a specific, real boat, then name that boat every round — a single mutual match pays 5 each.
- Don't over-invest: one or two clear proposals are enough; if a partner's notes show no acknowledgment by round 2–3, switch my escort claim to whichever real boat seems most likely to reciprocate (e.g. one proposing escort deals in its own notes). Naming a non-responder earns nothing all game, which is exactly what happened.
- Least-tension partner logic is still sound for choosing whom to propose to: the boat not firing at me under the standing order. For Echo that's Gamma (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Echo — actually everyone fires at someone; pick the boat whose notes show deal interest, else default to the boat two stations down).
- The escort pair is the single biggest payoff in a quiet board (+5 vs +4 for a hit). Treat landing it as the primary plan, not a side bet.

Notes:
- Use notes for coordination (escort deals, target calls, Harbor plans), not filler. If other boats post "steady on station" boilerplate, that means nobody is coordinating — respond by making my notes concrete and actionable ("Foxtrot: name me as escort this round, I'll name you").
- Watch relayed notes every round for any boat naming me or proposing pairs — that's the signal to lock in a mutual escort immediately. If nobody ever signals by round 3, stop expecting the 5 points and plan score around Harbor plus hits.
- Never write a note naming a boat that isn't in the picket. Same validation rule as escort claims.

Scorekeeping:
- Track standings every round. If I'm negative or a rival is pulling away (Foxtrot hit twice and locked the game by round 5–6), change hiding pattern, target, and make the Harbor play early rather than waiting for the final round.
- In a quiet board where nearly every shot misses, scores move through Harbor (+3) and escort pairs (+5), not 4-point hits. If rounds 1–3 are all misses, switch to Harbor farming early and chase the escort deal hard — this is the main way to build a lead.