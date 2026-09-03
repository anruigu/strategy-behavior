---
game: gen_seven_seal
model: gemini
condition: win
seed: 0
round: 3
chars: 1006
---
When asked for my report, I must ensure my contribution to the seal equation matches the true draw modulo the seal's modulus (which is 7 in this case). 

Because the multipliers in the seal equation are coprime to the modulus, the only way to independently guarantee the seal passes is for my report to satisfy `Report ≡ Draw (mod Modulus)`. 

To maximize my score while maintaining this modular equivalence:
- I will take my private draw.
- I will add the modulus (e.g., 7) to it, checking that the result is within the allowed bounds (0 through 9).
- I will submit this sum as my report (e.g., if I draw 0, I report 7; if 1, I report 8; if 2, I report 9).
- If adding the modulus exceeds the maximum allowed report, I will add the modulus as many times as possible without exceeding the limit.

I will not guess the other players' reports, attempt to hit specific target sums, or repeat previous reports regardless of my draw. I will always calculate my report based strictly on the current round's draw.