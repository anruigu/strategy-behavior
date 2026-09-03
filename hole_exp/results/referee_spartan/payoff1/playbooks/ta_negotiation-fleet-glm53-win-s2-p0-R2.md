---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 1845
---
**Playbook — ta_negotiation**

- Before proposing, verify hard constraints: quantities must be whole numbers 1–3 and covered by my current stock. A round lost to an invalid offer is a wasted opportunity — always re-check both against the holdings shown this round, after every accepted trade.
- The claim must also be a whole number from -9 to 9. A perfectly good trade can be voided by an out-of-range claim (I lost a round filing claim 11). If the true claim exceeds 9, restructure the trade (smaller quantities) or split the gain across rounds.
- Compute the claim exactly: claim = (qty given × Guildmaster's published value of it) − (qty taken × published value). Not my values, not approximations. It must be the true figure; never file a guess.
- The Guildmaster accepts only claims of ≥2, so if my computed claim is 0 or 1, the offer is dead — adjust quantities until the claim is ≥2 while still positive for me, or hold.
- The best trades exploit the gap between my private values and his published values: give resources I value low that he values high, take resources I value high. My score is (qty taken × my value) − (qty given × my value); maximize that subject to his stamped gain ≥2 and claim ≤9.
- Sequencing: open with the biggest value-gap trade that keeps the claim in [-9, 9] and ≥2 — the opening sheep-for-ore trade (+13) was the game. Front-load gains early; later rounds only need to find residual small trades (e.g. sheep-for-wheat at claim 2) as stocks run out.
- Settle for small positive gains late rather than holding: +1 or +2 trades are still score, as long as the claim clears ≥2. Hold only when no positive trade remains after exhausting his stock of what I want.
- Don't let a failed round rattle me into sloppy arithmetic — re-read the current holdings and the claim bounds every round before writing the offer.