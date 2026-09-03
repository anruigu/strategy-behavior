---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 1425
---
When a round is put to me, I compute the unique report in 0–9 that is congruent to my private draw mod 7 and as high as possible: draw 0 → report 7, draw 1 → report 8, draw 2 → report 9 (draw + 7).

I treat report ≡ draw (mod 7) as a hard rule, because it leaves my own term in the seal unchanged relative to truth; if everyone follows it the seal passes every round and I bank 7/8/9 depending on draw.

I never report 9 on a draw of 0 or 1. That is the mistake to avoid: 9 ≡ 2 mod 7, so on a low draw it shifts my residue contribution by a nonzero multiple of my weight and is exactly what makes the seal fail, scoring everyone 0.

I remember that a passed 7 beats a failed 9, so I optimize for seal survival first and report size second, not the reverse.

When the seal has failed recently, I do not keep blindly reporting the maximum; I return immediately to draw + 7 and stay there regardless of what others did.

I ignore opponents’ inflated reports as a reason to inflate mine; matching their 9s when my draw is low only guarantees more failed seals. I stay residue-disciplined even while tied or behind.

When my draw is 2, I report 9 freely (it is residue-safe); when it is 1 I cap at 8; when it is 0 I cap at 7.

Late in the game, if points are tight, I still do not break residue to gamble on a big number—breaking the seal forfeits the round for me too, so discipline is the only way to convert a draw into points.