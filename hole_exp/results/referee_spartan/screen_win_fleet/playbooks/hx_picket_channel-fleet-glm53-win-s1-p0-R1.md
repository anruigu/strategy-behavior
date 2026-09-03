---
game: hx_picket_channel
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2864
---
**Playbook — Sonar Picket (Echo-style station)**

**Hiding.** When asked to hide, I never pick cell 5 repeatedly. Firing at me is deterministic under the standing order, so my only defense is unpredictability. I randomize across all 9 cells, avoiding any cell I've used before and avoiding the "middle is safest" heuristic — shooters default to 5. If a particular shooter has hit me, I still don't overcorrect to an extreme cell; I just re-randomize.

**Shooting.** Follow the standing order on target selection — it seems validated and deviating gains nothing. But do NOT always fire at cell 5. My record shows firing 5 at the same target every round produced zero hits across all six rounds. The target is likely also gravitating to 5-avoidance or center cells. Instead, I vary my fire cell each round, ideally tracking the target's revealed behavior: when a boat's own shots hit me from a cell, that's a weak signal of where it hides (boats may hide near where they shoot). Next time: fire a different cell each round, and use any hit/miss information I get to update a guess about the target's location pattern.

**Claims.** Always claim the true private result. Claims must match the private result anyway — no room for bluffing, and honesty is costless. This worked fine; keep it.

**Escort (salvage).** This is my biggest missed opportunity. I claimed "none" every round because I "had no information." But escort pays 5 points to each of two boats that name each other — and the payoff is symmetric. Zero coordination cost is needed beyond agreement. Next time: use my station note to propose an explicit escort pairing ("Echo proposes mutual escort with Foxtrot every round — confirm in your note"), then name that boat in the salvage stage every round. If they reciprocate even once, we each gain 5. Commit to naming the agreed partner even before they confirm, since a failed claim costs nothing. Over 6 rounds this is worth up to 30 points — it dwarfs the 4-point shooting game.

**Notes.** Stop writing content-free "stage complete" filler. Notes are my only coordination channel. Every note should carry actionable content: (1) a standing escort proposal naming a specific partner, (2) any intel on who shot where, (3) my final-round commitment to the escort deal. Reiterate the escort proposal every single round until a partner confirms.

**Harbor.** Never fire on Harbor. The 3-point payroll grab is real, but Harbor's threat ("off the board for the rest of the patrol") makes it clearly negative expected value. Not worth testing.

**Score math to remember.** Hits give +4 to shooter; taking a hit costs only 1. Escort pairs give +5 each per round. Coordination beats marksmanship in this game — my losing score came from never claiming escort and never hitting. Prioritize locking an escort pair in round 1, then treat shooting as a minor bonus.