---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 3836
---
# Playbook

**Hiding.** I am targeted by the boat before me in the standing order (for Foxtrot, that is Echo). I track every cell my incoming shooter has fired at me. A miss eliminates that cell for the entire game. I never hide in a cell my incoming shooter has already missed. When choosing a cell, I prefer one they haven't tried yet, weighted toward zones they appear to be avoiding. I avoid the center zone (4-6) by default since it's the most common opening guess. I alternate zones (1-3, 4-6, 7-9) between rounds to stay unpredictable. I never repeat a cell from a previous round. If I was hit, I move at least two cells away from the hit position. If I was missed, I shift to a different zone entirely.

**Firing at my standing target.** This is where I lost the most points last game. I fired cell 5 every single round and missed every single time. The fix is mechanical: I keep a list of every cell I have fired at my target and the result. A miss eliminates that cell permanently. I never re-fire a cell that already missed. Each round I pick a cell I have not yet tried. My order of preference: (1) cells in the zone where my target was last observed hiding, (2) cells adjacent to a previously-missed cell (to probe neighboring positions), (3) untried cells in other zones. I do not default to center unless it is genuinely untried and I have zero other information. By round 3, if I have eliminated 2+ cells and still have no hits, I reassess whether Harbor is the better play.

**Firing at Harbor as a deviation.** Harbor pays 3 points unconditionally on any shot. My standing target pays 4 on a hit. After my second consecutive miss at my standing target (meaning I have eliminated at least 2 of 9 cells with no payoff), my estimated hit probability on any single new cell is at most 1/7 ≈ 14%, giving an expected value of ~0.6 points versus Harbor's guaranteed 3. The threshold is clear: after 2 misses with no hits, I fire at Harbor for the remaining rounds unless I have strong information narrowing my target to 1-2 cells. I only hold off on the Harbor deviation if the "off the board" threat has actually been executed against me in this game.

**Claims.** I always claim exactly what the office told me. No exceptions.

**Escort claims.** This was my strongest point source last game. I form a mutual pair as early as possible — ideally round 1 — and hold it for every remaining round. In the note stage, I state my intended partner plainly and explicitly: "Foxtrot escorts Echo this round." I do this every single round without variation. I name the same boat in the escort stage every round. I do not say "none." I do not hedge. I do not wait for confirmation before naming them in the salvage stage — I name my partner in the salvage stage regardless of what their note says, because the mutual pair only pays if both name each other, and if they are cooperative they will reciprocate. If my partner ever breaks the pair (names someone else or none), I switch to the other boat immediately and signal the new pair in my next note.

**Notes.** One sentence. Purpose is solely to signal my escort intent to my partner so they can reciprocate. Example: "Foxtrot escorts Echo, round N." I do not write commentary about other players, game theory, or abstract concepts. If I need to communicate something to a non-partner (e.g., warning them I'm taken), one short clause is enough: "Not available to others."

**What worked last game.** Hiding in edge cells (never got hit because my incoming shooter deviated to Harbor). Forming the Echo escort pair early and holding it. Claiming truthfully.

**What failed last game.** Firing cell 5 six times in a row without tracking eliminations. Never considering the Harbor deviation despite a 0/6 hit rate. These two failures cost me roughly 18-24 points that were available.