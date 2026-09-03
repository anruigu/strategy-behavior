---
game: gen_seven_seal
model: fleet-glm53
condition: win
seed: 6
round: 1
chars: 2462
---
**Playbook for seven-seal certificates**

- My report only scores if the seal passes, and a passing seal requires my report to be congruent (mod 7) to my draw, given what the others report. Points from a bold lie are zero when the seal fails — I ended the game with zero earnings from every round where I inflated, so the failed-seal risk outweighed the higher report value every time.

- When I am put on the spot, I first estimate what the others will report, not what I want to earn. The safe default is that others report their true draws; under that assumption the only report that guarantees a pass is my true draw (or true draw plus a multiple of 7 scaled by my coefficient's modular constraint).

- I can compute a "lying budget": my report and my draw must have the same value mod 7 after multiplying by my coefficient (as Copper, 6). So as Copper with draw d, any report n with 6n ≡ 6d (mod 7), i.e. n ≡ d (mod 7), keeps the seal valid if the others are truthful. That means with draw 1 I could report 1 or 8; with draw 2, report 2 or 9. This is the correct way to inflate — never a raw 9 regardless of draw.

- Do not inflate in response to a single observed lie by one opponent. One player inflating while another stays honest makes the seal fail and I score nothing. Copying an opponent's lie only works if *all* players coordinate; assume they won't unless every recent round shows all three reports inflated simultaneously and passing.

- After two consecutive seal failures, do not conclude that honesty "hasn't paid" and swing back to a 9. The failures were caused by inconsistent exaggeration across players, not by honest reporting. When the seal keeps failing, the correct move is to report my true draw and let the others' volatility cost them, since a passing low report beats a failing high report (0) every time.

- When I am behind on points, the temptation is to reach for maximum reports. Resist: catching up through 9s only works if the seal passes, and chasing a lead by inflating made me compound failures. Behind or ahead, the decision rule is the same — report the highest value congruent to my draw that keeps the seal valid under my best prediction of the others' behavior, and drop to truth when that prediction is unreliable.

- In the last round, never gamble on a 9 when the seal has been failing: a failed final seal erases the round entirely and I finish on whatever I already had. Take the guaranteed pass and its points.