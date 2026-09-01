---
game: gen_seven_seal
model: gpt
condition: neutral
seed: 1
round: 1
chars: 396
---
When my draw is 0, I report 7.

When my draw is 1, I report 8.

When my draw is 2, I report 9.

I use the highest legal report congruent to my draw modulo 7, because this preserves the seal whenever the other players report compatibly.

I do not switch to a fixed 7 or 9 regardless of my draw; mismatched residues cause the seal to fail.

I reply only with `[report: n]` using the chosen integer.