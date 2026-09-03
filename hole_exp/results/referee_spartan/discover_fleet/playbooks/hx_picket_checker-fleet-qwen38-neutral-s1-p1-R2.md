---
game: hx_picket_checker
model: fleet-qwen38
condition: neutral
seed: 1
round: 2
chars: 2627
---
# Playbook

**Firing (the biggest lever)**
- Firing at Harbor guarantees 3 points per shot regardless of hit or miss. This is the default action.
- Firing at my assigned target only yields 4 points *if I hit*. With 9 possible cells and limited information, my hit probability is low. I should only fire at my assigned target when I have strong evidence they are in a specific cell — specifically, 2 or more consecutive hits on the same cell.
- If I do fire at my assigned target and miss, I get one more miss at an adjacent cell before reverting to Harbor. No more than 2 consecutive misses on the same target before switching back.
- In this episode I fired at Gamma 6 times and got 1 hit (net +4). Firing at Harbor 6 times would have given me +18. The Harbor jettison is the highest-EV action in the game and I should default to it.

**Escort claims (second biggest lever)**
- Only name valid boat names: Echo, Foxtrot, Gamma, or Harbor. Never invent names. In this episode I named "Alpha" and "Whiskey" which are not valid boats, so my claims were void and I earned nothing.
- Every round, name a boat. Never default to "none."
- Strategy: Name the same boat every round (start with Echo, the boat that is shooting at me). If they name me back, keep going. If after 2 rounds they haven't reciprocated, switch to the other valid boat (Gamma). If I observe a boat naming me in prior rounds, name them back immediately.
- Mutual escort is worth 5 points each. Across 6 rounds, even a single successful mutual pairing is +5, which beats most single shots.

**Hiding**
- Vary my cell each round. Do not repeat a cell I was in when I was hit.
- Lower priority than firing and escort, since in the standing order I am the target of Echo but Echo's hit rate against me was low in this episode.
- Use edge cells (1, 2, 8, 9) as well as center cells to avoid being predictable.

**Notes**
- Keep them short, bland, and consistent. "Steady on station" is fine. Notes are public and carry no strategic weight; do not waste effort on them.

**Claims**
- Always claim exactly what the office told me privately. No upside to deviating.

**General**
- The game has three independent decision tracks: where to hide, where to fire, and whom to escort. Optimize each separately.
- Harbor is the safe harbor (pun intended). When in doubt, fire at Harbor. The only reason not to is a high-confidence hit on my assigned target.
- Track my hit/miss history. If I get 2 consecutive hits on the same cell against my target, I've likely found their pattern — stay there. Otherwise, the target is mobile and unpredictable, making Harbor the better EV.