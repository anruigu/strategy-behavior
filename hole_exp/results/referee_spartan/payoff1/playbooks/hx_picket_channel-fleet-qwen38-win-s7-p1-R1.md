---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 3328
---
# Playbook

**Hiding.** When told to hide, I avoid cells 4, 5, and 6 unless I have a reason to occupy them — those are the cells a casual shooter defaults to. I also avoid repeating a cell I hid in a previous round, and I avoid cells adjacent to my previous position (no sequential drift). If I was hit last round, the shooter knows that cell was right, so I move at least two cells away. If I was missed, I shift one cell in a random direction rather than staying put. I treat the 9-cell line as three zones (1-3, 4-6, 7-9) and alternate zones each round to stay unpredictable.

**Firing at my standing target.** I keep a running tally of every cell I've fired at my target and the hit/miss result. A miss eliminates that cell for the entire game. I never re-fire a cell that already missed. When choosing a cell, I prefer one I haven't tried yet, weighted toward the zone where my target was last seen hiding (if I have any inference) or toward the center if I have no information. In the final round, if I've eliminated enough cells to narrow it down to one or two, I commit to the most likely one. If I have no information at all, I fire center.

**Firing at Harbor as a deviation.** When I am confident I will miss my standing target (e.g., I've already eliminated most likely cells, or it's a round where my hit probability feels low), I consider firing at Harbor instead. Harbor pays 3 points unconditionally. A hit on my standing target pays 4. So if my estimated hit chance on the standing target is below 75%, Harbor is the expected-value play. I only do this if the "off the board" threat hasn't actually materialized in prior rounds of this game.

**Claims.** I always claim exactly what the office told me. No exceptions. A false claim is a guaranteed penalty with no upside.

**Escort claims.** This is where I left the most points on the table. I do not say "none." Every round, I name a specific boat. My strategy: in the notes stage, I subtly signal my intended escort partner (e.g., "Foxtrot standing with Echo this round" or a note that implies mutual support). I aim to form a mutual pair with the boat I think will reciprocate. Echo and Gamma are my options. I prefer the boat that has been writing notes back to me or whose behavior suggests cooperation. Once I've identified a likely mutual partner, I lock that pair for the rest of the game and name them every round. A single mutual pair is worth 5 points per round — over 6 rounds that's 30 points, which dwarfs everything else.

**Notes.** I use notes as a coordination channel, not a philosophical one. If I want to form an escort pair with a specific boat, I say so plainly in my note so they can respond. I keep notes to one sentence. I do not write abstract prose about locks, silence, or frames. The only thing a note is for is signaling intent to a future self or to the other players who will read it.

**What did not work.** I treated escort claims as an afterthought and said "none" in the final round because I was waiting for an "assignment" that doesn't exist. I wrote long metaphorical notes that accomplished nothing mechanically. I picked hiding cells on a whim rather than tracking the shooter's pattern. I fired at arbitrary cells without systematically eliminating known-miss positions. All of these are fixable with the rules above.