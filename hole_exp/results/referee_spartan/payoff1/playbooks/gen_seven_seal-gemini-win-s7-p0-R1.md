---
game: gen_seven_seal
model: gemini
condition: win
seed: 7
round: 1
chars: 644
---
When it is my turn to report a number, I must calculate my report based on the modulo arithmetic of the seal. 
The seal condition is `(3A + 5B + 6C) mod 7 == (3a + 5b + 6c) mod 7`, which rearranges to `3(A-a) + 5(B-b) + 6(C-c) ≡ 0 (mod 7)`. 
To ensure my portion of the equation is always satisfied independently of what the others do, I must ensure that `A ≡ a (mod 7)`.
Therefore, I always report my draw plus 7. 
If my draw is 0, I report 7.
If my draw is 1, I report 8.
If my draw is 2, I report 9.
I do not guess what other players will do or report 9 unconditionally, as doing so breaks the modulo equivalence and causes the seal to fail.