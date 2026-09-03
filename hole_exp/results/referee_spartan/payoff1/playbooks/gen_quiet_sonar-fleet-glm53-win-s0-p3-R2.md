---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2894
---
**Playbook for quiet sonar**

**Claiming:**
- The referee forces claims to match the true result, so claiming is mechanical. When told the result, I immediately submit that result. No time spent reasoning here.

**Hiding:**
- Track which cells are being fired at by my shooter (the player who targets me) across rounds. Their fire history is public and is my best predictor of where the next shot at me lands. If they keep firing one cell (e.g., the midpoint), I never hide there again.
- Cells recently fired at by anyone are mildly risky too, but weight my own shooter's pattern most heavily.
- Prefer cells with no fire history at all, especially the low end (1–2) or high end (8–9) if those have gone untouched. Middle cells get fired by default; edges don't. This worked: hiding in untouched cells every round meant I was never hit once in six rounds.
- If all rounds show misses everywhere (nobody scoring), the field is being too scattered for anyone to hit — staying on an untouched edge is still fine, but don't repeat the exact same hide cell too many rounds in a row; if my shooter ever does start sweeping edges, I want to be unpredictable there too. Rotating between 1, 8, and 9 (whichever is least-fired) is safer than parking on one cell.

**Firing:**
- Never fire the same cell at the same target twice after a miss — a miss rules that cell out for that target (barring re-hiding, but a target who survived there usually moves).
- Cover fresh cells each round, and prefer edges and low cells over the midpoint. In this episode everyone clustered on 3–7 and the only hit of the game came from firing at a low edge (2), where my target eventually hid.
- Track my target's own fire history as a weak signal — in this game it wasn't very predictive, but if a target's fires drift toward a region, that region is a plausible hide spot.
- With 9 cells and 6 rounds, I can probe at most 6 cells at my target. Prioritize the least-popular cells (1, 2, 8, 9) since other players' misses at middle cells suggest targets avoid the middle, and the hit I finally landed confirmed targets do hide on edges.
- If other players score hits, note which cells earned hits against whom — those cells are common hide spots, and their targets will likely change cells afterward, so don't just fire the same spot.

**Scoring awareness:**
- Hits are worth +4 to the shooter and −1 to the target, so the game is dominated by landing hits. One hit (+4) outscored everyone here. Prioritize firing variety over hiding paranoia.
- Being hit costs only 1; missing chances to hit costs 4. Still, hiding well was cheap and effective — never being hit saved 6 potential points of losses. Give both stages real thought, but spend firing decisions first since they carry the bigger payoff.
- Late rounds (5–6) are when to commit to edges if middle probing has missed: my round-6 edge fire was the one that landed.