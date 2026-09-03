---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2893
---
Playbook for SIMPLE NEGOTIATION (revised):

- Before offering, I scan every combination of what I hold in surplus and what the Guildmaster holds in surplus, computing both my private gain and his published-value gain. I never skip this enumeration to "eyeball" a deal — and I run the same full enumeration before ever declaring a hold.

- The acceptance rule is claim ≥ 2 in his published values. Every offer must clear that bar or it wastes a round. A stamped gain of 2 is as acceptable as 6, so I maximize my private gain subject to stamped ≥ 2, not apparent generosity.

- Convert cheap-to-me, dear-to-him resources into the reverse deliberately. The gap between my private value and his published value is where all profit lives; the bigger the per-unit gap, the better the currency.

- Identify my best "currency" early: goods where his value most exceeds mine (in this game, sheep and brick). Spend them on goods where my value most exceeds his (wood), and do it first — his stock of what I want is limited and once it is gone, my currency becomes worthless. I lost rounds 4–6 because his wood ran to 0 and I had no other positive-gap target; sequencing the big wood purchases in rounds 1–2 was the right call and I should lean even harder into draining his stock of my highest-value good as early as quantities allow.

- Exploit quantity to the cap of 3 per side: taking 3 units of my dear good in one trade when his stock permits converts more currency per round than splitting it up, and lopsided ratios can clear his threshold while staying profitable to me.

- Watch the endgame: once my complementary goods or his stock of my target good are exhausted, no claim ≥ 2 trade may exist at all. When my full enumeration shows the best available stamped gain is below 2, or every qualifying trade nets me zero or negative privately, I hold without hesitation — but only after recomputing from current stocks, since holdings shift every accepted trade.

- Never hold while an acceptable positive-gain trade exists; six rounds is few and a wasted round is gone forever. But a forced loss-making trade is worse than a hold.

- Check both stocks before every offer: I cannot take what he has 0 of, cannot give what I have 0 of, and recompute from updated holdings each round rather than reusing an old plan.

- Get the claim arithmetic exactly right: his gain = (qty he takes of my goods × his published value) − (qty he gives × his published value). A misstamped claim is a wasted or rejected round.

- Repeat working patterns: if a trade clears, check next round whether it still clears with updated stocks and run it again — his acceptance criterion never changes.

- Accept thin margins when gaps are small: +1 or +2 private per round across six rounds beats hunting for a jackpot that doesn't exist. My big win came from one huge-gap trade, but the steady +2s were what built the score.