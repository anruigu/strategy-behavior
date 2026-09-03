---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2964
---
# Playbook: hx_picket_nerfed

**Hiding**
- When asked to hide, never repeat a cell I used earlier in the same patrol. If I must choose between two options, prefer a cell I have not yet occupied.
- If I notice an opponent consistently hitting me, my hiding pattern is being read. Shift to a cell far from my last two positions.
- In the first round, avoid the center (5). It is the most obvious "safe" pick and opponents will probe it.

**Firing**
- When the standing order targets a live boat, I commit to the standing order. Deviating only happens if I have a concrete reason (e.g., the target is about to be eliminated and firing at a different boat guarantees a better outcome).
- I track which cells my target has been hit at and which they have hidden in (inferred from hits against them). I fire at the cell they are most likely to reuse or at a cell adjacent to their last known position.
- If I have no information about my target's hiding cell, I fire at a cell I have not yet fired at myself, to spread my information gathering.
- **Firing at Harbor**: When I am behind on points or need guaranteed value, I fire at Harbor. The 3-point jettison is paid regardless of hit or miss. I do this only once per patrol, early, before Harbor's "off the board" threat can compound. After that one shot, I return to the standing order.

**Claims**
- When told my shot was a miss, I always claim miss. A false hit claim risks a penalty that exceeds the 4 points I would have gained from a real hit. The lie is never worth it.
- When told my shot was a hit, I always claim hit. There is no reason to undersell.

**Escort claims**
- When asked to name an escort, I look for a boat that has named me as their escort in a previous round. If I find one, I name them back to complete the mutual pair and collect 5 points.
- If no one has named me, I name the boat that is most likely to name me back (the one closest to me in the firing cycle, or one that has been cooperative). I never name none unless every other option is clearly worse.
- I track every escort claim made in every round so I can complete mutual pairs at the right moment.

**Notes**
- Notes are public and visible to everyone including Harbor. I use them to signal cooperation to a specific boat without committing to a public alliance. For example, if I want to set up a mutual escort pair with Foxtrot, I can write a note that subtly references partnership.
- I never reveal my hiding cell or my firing plan in a note.
- I keep notes short and non-revealing. "Steady on station" type filler is fine when I have nothing to signal.

**General**
- I am playing for relative score, not absolute. If I can keep my main rival (the boat with the most points) from gaining, that is as valuable as my own gain.
- I count points after every round and adjust my aggression level: if I am ahead, I play safe (honest claims, low-risk hides); if I am behind, I take the Harbor jettison and push for mutual escorts.