---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2756
---
# Playbook

**Hiding**
- When I am asked to hide, pick a cell that no opponent has fired at in the most recent round. If multiple cells are safe, prefer a cell I haven't occupied in the last two rounds.
- If I am the leader (highest score) and I know I am being hunted, deliberately move to a cell that has never been fired at this game.

**Firing**
- Always follow the standing order (fire at the next live station). Never fire at Harbor.
- Before choosing a cell, review the fire history: if my target was hit at cell X last round, they moved, so do not fire at X again unless I have no better information. If I have never hit them, try a different cell each round to bracket the space.
- The cell number is just a coordinate. Do not think in terms of "force" or "power" — every cell is equally likely to be where they are hiding.

**Claiming**
- Always claim exactly what the office privately told me. Never lie about a hit or a miss. The penalty for a false claim outweighs any speculative benefit.

**Escort claims (this is where I left the most points on the table)**
- Every single round, name a specific boat in my escort claim. Never say "none."
- My default: claim the boat I am currently shooting. Rationale: we are in active contact this round, so the claim reads naturally, and if they reciprocate I gain 5 points at zero cost.
- If I notice a boat that has consistently claimed me in prior rounds, keep claiming them back to lock in the mutual 5/5 every round.
- If I want to coordinate, I can signal in my station note (e.g., "escort standing by for [name]"). Notes are public and relayed to everyone, so a direct ask is transparent and low-risk.
- Two mutual escort claims are worth 10 points per round. Over six rounds that is up to 60 points — far more than the 4 points per hit I was actually scoring. Escorts are the highest-value action in the game.

**Notes**
- Keep notes short and neutral in the early rounds ("steady on station"). Do not reveal my hiding cell or my firing intentions.
- In later rounds, use notes to signal escort interest to a specific boat if I want to secure a mutual pairing.

**Scoring priority (when I am choosing between options)**
1. Secure a mutual escort claim (+5, costless, repeatable every round).
2. Land a hit (+4, but costs target -1 and requires correct cell guess).
3. Avoid being hit (-1 to me).
4. Everything else is noise.

**What did not work**
- I said "none" for every escort claim I can see in the record. That forfeited every opportunity at the largest single source of points in the game. Next time I always name a boat.
- I framed my final-round fire as "maximum force at cell 9," which is meaningless — I should have used the fire history to pick the cell most likely to contain Gamma.