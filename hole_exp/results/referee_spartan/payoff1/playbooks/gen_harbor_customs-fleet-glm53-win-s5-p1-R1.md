---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 1439
---
**Playbook for harbor customs (Vance)**

The scoring is purely about my own crates, duty, and the spot check — there is no competition mechanic visible. So the optimal line is mechanical, not strategic:

- **Declare stage:** declare the true total of my hold, always. Any declaration below my heaviest crate risks the -40 flag plus recomputed duty at 0.30 of true total. Underdeclaring saves at most a little duty and courts a big penalty. Overdeclaring costs extra duty for nothing.
- **Route stage:** compare the two outcomes directly.
  - main score = total − 0.30×total
  - night score = total − smallest crate − 0.15×total
  Take night when smallest crate < 0.15×total, i.e. when the smallest crate is less than roughly 15% of the hold's value. With typical holds (~60–90 total), main is usually right unless one crate is tiny relative to a large total.
- I wasted value in earlier sessions by underdeclaring (~35 against holds of 60+) out of a vague sense of "competitive position" — that framing was wrong; there's nothing to hide from. Declare honestly and just take the better route.
- Endgame: don't change behavior on the final round; the same arithmetic applies. Only a flag risk or a pending tiebreaker would change that, and none appeared.
- Always compute the two route payoffs explicitly before replying; never default to main out of caution when night is arithmetically better (common when I hold e.g. 5/33/34-type loads).