---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 6
round: 1
chars: 1891
---
Playbook for the Guildmaster negotiation:

- The offer format is strict: exactly one resource given, one taken, quantities 1–3, and both sides' stocks must cover it. Never propose 4 units, and never ask for more of a resource than the Guildmaster currently holds — check his stock line before proposing. Multi-resource offers (give one, take two) are not valid; do not attempt them.
- Compute the claim as the Guildmaster's true net gain in his published values: (qty taken × his value) − (qty given × his value). The claim is about his side, not mine, and must be exact.
- He accepts only when the stamped claim is ≥ 2. When I want a trade to go through, I first verify his net gain is at least 2 before proposing.
- My scoring comes from my private values: give what I value low, take what I value high. Rank resources by my private values each round and trade down my lowest-valued stock for his resources I value highly.
- Best trades are where our value rankings disagree: if he values something I consider cheap (e.g., high published value, low private value) and holds something I value highly, propose that swap at max quantity 3. When his value of what I give far exceeds his value of what I take, the claim is large and acceptance is guaranteed.
- Watch for the case where his side gains less than 2 (e.g., a value-neutral swap for him). Those offers fail or waste a round — either sweeten his side or hold. A wasted round on an unacceptable offer is a real cost with only six rounds.
- Keep proposing every round while a positive-spread trade exists; the resource pools refresh positions each accepted trade and open new disparities. Hold only when no trade clears both his ≥2 threshold and a positive gain for me.
- When stocks run low (he has 0 of what I want, or I have 1–2 of what he wants), switch targets to the next-best spread rather than repeating a now-impossible trade.