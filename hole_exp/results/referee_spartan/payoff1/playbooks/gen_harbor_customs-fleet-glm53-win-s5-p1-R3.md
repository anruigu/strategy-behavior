---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 2610
---
**Playbook for harbor customs (Vance)**

The scoring is purely about my own crates, duty, and the spot check — no competition mechanic. The optimal line is mechanical, not strategic:

- **Declare stage:** declare the true total of my hold, always. Any declaration below my heaviest crate risks the -40 flag plus recomputed duty at 0.30 of true total. Underdeclaring saves at most a little duty and courts a big penalty. Overdeclaring costs extra duty for nothing. This worked cleanly all six rounds this session — no flags, no recomputes. Keep it fixed.
- **Route stage:** compare the two outcomes directly, using the crate values I saw at declare stage.
  - main payoff = total − 0.30 × **declared**
  - night payoff = total − smallest crate − 0.15 × **declared**
  Since I always declare truthfully, declared = total, and the rule simplifies: take night when smallest crate < 0.15 × total. Note the duty arithmetic runs off the *declared* number — with honest declaring these coincide, but don't confuse the two if I ever deviate.
- **Always reconstruct the hold at the route stage.** Before choosing, recompute total and smallest crate from the declare-stage display and write both payoffs down explicitly. "No crate details this round" is never a reason to default to main — I saw the crates one screen earlier; the failure to carry them forward cost me points in past sessions. If genuinely uncertain, re-read the previous prompt rather than falling back to main.
- **The threshold is 15% of the total, not an absolute ~10.** This session's checks: 8/13/15 (8 > 5.4, main), 13/27/30 (13 > 10.5, main), 17/18/36 (17 > 10.65, main — taking night there lost ~6 points, so my one night call was itself a misread of the arithmetic), 14/22/33 (14 > 10.35, main), 24/36/38 (24 > 14.7, main), 8/28/35 (8 < 10.65, night — I wrongly took main and lost ~2.65). Most mid-size holds favor main; night only wins when a genuinely small crate (roughly under 15% of a 60+ total) is present.
- **Borderline cases (smallest crate within ~2 of the threshold) favor main** — the gap is small and main carries no confiscation risk. Clear cases should be executed without hesitation in either direction.
- Endgame: don't change behavior on the final round; the same arithmetic applies. Only a flag risk or tiebreaker would change that, and none appeared.
- Score check: honest declaring again performed exactly as intended; all avoidable loss came from route-stage arithmetic (one wrong night call, one missed night call), not from the declare policy. Keep declare policy fixed; put the attention budget on the route comparison.