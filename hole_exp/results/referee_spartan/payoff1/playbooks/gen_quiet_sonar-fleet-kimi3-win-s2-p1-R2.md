---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 3135
---
- My claim must match the referee's private result, so I always claim truthfully. False claims gain nothing legitimately and only risk rejection. When the claim stage comes, I echo the result without deliberation.

- After a confirmed hit on my target, I fire that exact cell again next round. Players park on a hide until punished — I wasted three rounds probing 5 after hitting Gamma at 2, while Gamma apparently sat near there and later only moved after sustained pressure. I re-fire the successful cell first and only go back to probing once it misses.

- I assume opponents are more deterministic than I am, and I exploit it ruthlessly. Harbor hid at 6 almost every round and Gamma farmed it for hits; Echo fired 5 every single round and never adjusted. If a victim keeps getting hit on one cell, that pattern continues until it stops — I ride it. If my own shooter is locked on one cell, I simply never hide there, ever.

- Once I hit a hider more than once, I expect relocation — typically to a distant, previously untouched cell (Gamma jumped from 2 to 9). After a second hit on the same cell, I pre-emptively consider where "far and clean" would be for them instead of hammering the old spot forever.

- For hiding, I track which cells have been fired at all, by anyone, across the whole game. Cells literally never fired (1, 3, 7 in my episode) are the safest hides. I keep a mental list of untouched cells and rotate among them rather than just "avoiding clusters."

- Untouched does not mean permanently safe — once a cell gets fired publicly, its safety drops for everyone. I update my untouched list every round using the public fire history.

- I never repeat my own hide on consecutive rounds, and I never hide where I've just been shot even if it was a miss on someone else near that cell — publicly fired cells draw probes.

- My fire and hide decisions are independent: my own hide tells me nothing about where opponents hide, so I don't let it bias my aim.

- I spread probe shots early only when I have zero data on my target; the moment I have one confirmed hit, that cell becomes my default and probing stops. Late rounds are not for fresh guesses — they are for the pattern with the most evidence.

- I read all shooters' patterns from the public ledger, not just my own line. A shooter who always fires one cell and always misses is leaving their victim free — and tells me that victim can hide anywhere except that cell with impunity, including hiding patterns I can exploit when roles turn.

- If I'm ahead late, hiding evasively matters more than speculative firing: I deny my shooter points first, and fire at the single best-evidenced cell rather than gambling on a new probe.

- My public reasoning text is visible; I keep it to the current decision and never announce future intentions or my full hiding algorithm, since adaptable opponents could read and counter it.

- I record every round's fires and claims before answering. When the shown history window truncates earlier rounds, I reconstruct what I can from the points totals (a claimed hit is +4/−1) rather than deciding as if no history exists.