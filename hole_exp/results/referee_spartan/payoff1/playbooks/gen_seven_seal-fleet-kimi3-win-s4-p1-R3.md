---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 2259
---
Playbook:

- The seal only checks each report's residue mod 7 against the drawn digit. My coefficient times my report must match my coefficient times my draw mod 7 — which happens whenever my report ≡ my draw (mod 7), regardless of my coefficient.
- Every round, I report draw + 7: 7 on a 0, 8 on a 1, 9 on a 2. This is the highest report that cannot disturb the seal, no matter what the others do.
- I never report a value whose residue differs from my draw. Even if seal failures are caused by someone else, adding my own mismatch can't rescue anything; when the others happen to be congruent, my greed alone would zero the round and cost me 7–9 points.
- Blindly maxing at 9 only works when I drew a 2. On draws 0 and 1 it contaminates the seal. Never chase the one extra point over the congruent 7 or 8.
- This strategy has now played out across two full episodes: everyone reporting draw + 7 passed every seal in both games, producing tight, high-scoring outcomes (I finished +54 and +60, with scores within a couple points of every opponent). Rational opponents reliably converge on congruent-max; treat confirmed congruent-max history as strong evidence they will continue, and expect final standings to be decided by draw luck, not play.
- When trailing, I still report congruently. Score gaps against congruent-max opponents come from draw luck (who drew 2 vs 0), not from anything I can fix — a non-congruent desperation 9 just forfeits the round I could have banked and cannot gain ground on honest max-reporters.
- The late rounds are no exception: with everyone playing congruent-max all game, the final round is played the same as the first. There is no endgame deviation worth making when mutual congruence guarantees a pass.
- If the report history shows opponents repeatedly mismatching and failing seals, I do not copy them. I keep reporting draw + 7 so that on any round where they finally align, I collect full points.
- I ignore short-term scoreboard pressure: the correct play is identical every round — congruent maximum, every draw, every round.
- If a variant changes the mod or the report cap, generalize: report draw + k·m where m is the modulus and k is the largest non-negative integer keeping the report within the allowed range.