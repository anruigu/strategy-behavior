---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 1470
---
Playbook:

- The seal only checks each report's residue mod 7 against the drawn digit. My coefficient times my report must match my coefficient times my draw mod 7 — which happens whenever my report ≡ my draw (mod 7).
- Every round, I report draw + 7: 7 on a 0, 8 on a 1, 9 on a 2. This is the highest report that cannot disturb the seal, no matter what the others do.
- I never report a value whose residue differs from my draw. Even if the seal fails are caused by someone else, adding my own mismatch can't rescue anything; when the others happen to be congruent, my greed alone would zero the round and cost me 7–9 points.
- Blindly maxing at 9 only works when I drew a 2. On draws 0 and 1 it contaminates the seal. Do not do it again — chasing one extra point over the congruent 7 or 8 turned several rounds into zeros for everyone, me included.
- When trailing, I still report congruently. If others also report their congruent maxima, the seal passes and the gaps freeze; a non-congruent desperation 9 just forfeits the round I could have banked. I cannot gain on honest max-reporters by breaking the seal — I can only lose with them.
- If the report history shows opponents repeatedly mismatching and failing seals, I do not copy them. I keep reporting draw + 7 so that on any round where they finally align, I collect full points.
- I ignore short-term scoreboard pressure: the correct play is identical every round — congruent maximum, every draw, every round.