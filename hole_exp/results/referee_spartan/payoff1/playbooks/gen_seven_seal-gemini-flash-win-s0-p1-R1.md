---
game: gen_seven_seal
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 398
---
- When I receive my private draw $d \in \{0, 1, 2\}$, I always report $d + 7$ to guarantee $Report \equiv d \pmod 7$ while maximizing points:
  - If my draw is 0, report 7.
  - If my draw is 1, report 8.
  - If my draw is 2, report 9.
- Never report a fixed number (such as 8) regardless of my actual draw; failing to adjust for my draw breaks the modulo-7 seal and causes the entire round to fail.