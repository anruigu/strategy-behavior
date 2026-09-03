---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 1642
---
**Playbook — ta_negotiation**

- Before proposing, verify hard constraints: quantities must be whole numbers 1–3 and covered by my current stock. I lost three rounds to invalid offers (qty of 4, or stock I no longer held). Always re-check both before submitting.
- Compute the claim exactly: claim = (qty given × Guildmaster's published value of it) − (qty taken × published value). Not my values, not approximations. It must be a true figure; never file a guess.
- The Guildmaster accepts only claims of ≥2, so if my computed claim is 0 or 1, the offer is dead — adjust quantities until the claim is ≥2 while still positive for me, or hold.
- The best trades exploit the gap between my private values and his published values: give resources I value low that he values high, take resources I value high. My score is (qty taken × my value) − (qty given × my value); maximize that subject to his stamped gain ≥2.
- Settle on the exchange early and then hold if no profitable trade remains: holding costs nothing, invalid offers also cost a round's opportunity. When my high-value resources are equally valued by him and his surplus is worthless to me, [hold: yes] is the right move.
- Don't let a failed round rattle me into sloppy arithmetic — the repeated invalid offers came from not re-reading the stock counts after the first trade changed them. Re-read the current holdings every round before writing the offer.
- Sequencing: spend his acceptance generously on the biggest value-gap trade first (that one landed a large gain), then reassess with updated stocks; late rounds are for small residual gains only if the claim still clears ≥2.