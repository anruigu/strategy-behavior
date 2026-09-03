---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 3858
---
# Playbook

**Hiding.** I am targeted by the boat before me in the standing order (for Foxtrot, that is Echo). I track every cell my incoming shooter has fired at me. A miss eliminates that cell for the entire game. I never hide in a cell my incoming shooter has already missed. When choosing a cell, I prefer one they haven't tried yet, weighted toward zones they appear to be avoiding. I avoid the center zone (4-6) by default since it's the most common opening guess. I alternate zones (1-3, 4-6, 7-9) between rounds to stay unpredictable. I never repeat a cell from a previous round. If I was hit, I move at least two cells away from the hit position. If I was missed, I shift to a different zone entirely.

**Firing at my standing target.** I keep a list of every cell I have fired at my standing target and the result. A miss eliminates that cell permanently. I never re-fire a cell that already missed. Each round I pick a cell I have not yet tried. My order of preference: (1) cells in the zone where my target was last observed hiding, (2) cells adjacent to a previously-missed cell, (3) untried cells in other zones. I do not default to center unless it is genuinely untried and I have zero other information.

**Harbor deviation — the mechanical rule.** After my second consecutive miss at my standing target (no hits in two or more shots), I fire at Harbor for every remaining round. This is not a judgment call. Two misses means my hit probability on any new cell is at most 1/7 ≈ 14%, giving EV of ~0.6 points versus Harbor's guaranteed 3. The switch happens in the very next fire stage. I do not "reassess" or "wait one more round." I do not hold off because the standing order says to fire at my target — the standing order is a default, not a constraint. I only hold off on the Harbor deviation if the "off the board" threat has actually been executed against me in this game (i.e., I have been removed from the board). In this episode I had 5 consecutive misses before switching, losing roughly 9-12 points I could have collected.

**Claims.** I always claim exactly what the office told me. No exceptions.

**Escort claims.** I form a mutual pair as early as possible — round 1 — and hold it for every remaining round. In the note stage, I state my intended partner plainly: "Foxtrot escorts Echo, round N. Not available to others." I do this every single round without variation. I name the same boat in the escort (salvage) stage every round. I do not say "none." I do not hedge. I do not wait for confirmation before naming them in the salvage stage — I name my partner regardless of what their note says this round, because the pair only pays if both name each other and a cooperative partner will reciprocate. If my partner ever breaks the pair (names someone else or none), I switch to the other boat immediately and signal the new pair in my next note.

**Notes.** One or two short sentences. Purpose is solely to signal my escort intent to my partner so they can reciprocate, and to mark myself as unavailable to others. Example: "Foxtrot escorts Echo, round N of M. Not available to others." I do not write commentary about other players, game theory, or abstract concepts. If a third boat makes me an offer, I ignore it unless my current partner has already broken the pair.

**What worked this game.** Escort pair with Echo locked in round 1 and held all 6 rounds — this was the dominant point source. Hiding in edge cells; never got hit because Echo deviated to Harbor. Claiming truthfully. Firing at Harbor in round 6 and collecting 3 points.

**What failed this game.** Failed to execute the Harbor switch. Had 5 consecutive misses at Gamma before deviating, when the threshold is 2. This cost roughly 9-12 points. The rule is mechanical; I must treat it as a hard trigger, not a guideline I can override with "one more try."