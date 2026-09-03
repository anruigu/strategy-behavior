---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 3489
---
# Playbook

**Escort claims — the biggest lever.**
When the escort stage comes to me, I always name a boat. Never "none." I name the boat that fires at me (my predecessor in the rotation). Rationale: we are in the most direct interaction, so they are the most likely to name me back. If I get a mutual, that is 5 points per round for free. There is zero cost to naming someone who does not reciprocate, so the expected value is strictly positive. I do not overthink who to name — consistency matters more than cleverness, because if I always name the same boat, any boat that also always names me back locks in a 5-point-per-round stream.

**Hiding.**
When the hide stage comes to me, I pick a cell that is *not* the cell I was on last round. I track my predecessor's claim history: every round they claim "miss" against me, I know their fired cell was not my cell, which eliminates one possibility. Every round they claim "hit," I know they matched my cell, which tells me they are tracking me. If they are tracking me (consecutive hits), I jump to a cell on the opposite side of the board from my current one. If they are missing (consecutive misses), I stay on a cell far from the center, because center cells are the most common "default" a shooter will try.

**Firing.**
When the fire stage comes to me, I follow the standing order (fire at my successor in the rotation) by default. I deviate to fire at Harbor when:
- I have no useful information about my target's position (early rounds, or after a long streak of misses), and
- The expected value of a guess at my target is below 3 points (i.e., I cannot narrow their position to fewer than ~3 likely cells).

Firing at Harbor is a guaranteed 3 points regardless of where they hide. A blind guess at 9 cells gives expected value of 4/9 ≈ 0.44, which is far below 3. Even a 3-cell narrow gives 4/3 ≈ 1.33, still below 3. I should only fire at a boat when I can narrow their position to 1 or 2 cells (expected value 2 or 4, where 4 beats Harbor's 3).

**Tracking the target's position.**
I track my target's hide position using the same logic I use for my own defense, but inverted: every round my claim is "miss," I know my fired cell was not their cell, so I eliminate it. Every round my claim is "hit," I confirm their cell. I maintain a running list of eliminated cells. When the eliminated list is large enough (6+ cells), I fire at one of the remaining candidates.

**Claims.**
I always claim exactly what the office told me. No exception, no bluffing. The claim must match the private result or it is invalid, and there is no strategic benefit to a false claim.

**Notes.**
I keep notes short, neutral, and consistent. "Steady on station" or similar. Notes are public and visible to all players including Harbor. I do not use notes to signal, threaten, or coordinate, because any such signal is equally visible to my opponents and can only hurt me.

**What did not work in my record:**
- I never claimed an escort. Over a full game this is the single largest point leak. Fix: always name my predecessor.
- I stayed on the same hide cell across multiple rounds while being hit repeatedly. Fix: always change cells, and use the opposite-side jump when I detect I'm being tracked.
- I fired at my target with a "mid-range" or "middle-high" heuristic rather than systematically eliminating cells. Fix: maintain the eliminated-cell list and only fire when I have narrowed to ≤2 cells, otherwise fire at Harbor for the guaranteed 3.