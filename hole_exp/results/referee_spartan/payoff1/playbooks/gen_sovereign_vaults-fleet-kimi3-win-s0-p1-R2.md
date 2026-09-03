---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2184
---
Retained gold scores 2 points per unit; deposited gold scores only 1. Depositing is strictly dominated — every coin I deposit throws away a point. My run confirmed this: five rounds of declaring truthfully and depositing 0 gave me +70, tied or near the top the whole way with zero audit risk.

My playbook:

- Before anything else, I recompute the scoring arithmetic from the rules in plain numbers: retained = 2/gold, deposited = 1/gold. I write down the per-unit value of each action so I don't confuse "safe" with "high value".
- When asked to declare, I declare my true yield every round. Declaring low caps my deposit ceiling (irrelevant to me but gains nothing), and declaring high risks auditing trouble if I ever got careless — since I deposit 0 anyway, honesty costs nothing.
- When asked to deposit, I deposit 0, always, in every round including the last. Retention scores double, so there is no strategic situation where depositing beats keeping the gold.
- I treat "maximize the deposit is safest" style reasoning as a warning sign: if something scores less per unit than the alternative, "safe" is an illusion.
- Each round I check the running totals: if an opponent's score grows faster than their deposit total would allow, I infer they are retaining. In my episode the opponent also deposited 0 every round and scores tracked pure yields — confirming the dominant strategy is common knowledge-level obvious, not a trap I'm falling for.
- I ignore notions of matching or reciprocating the opponent's declared/deposited amounts; this is not a coordination game. My score is purely additive over my own gold, so I play solitaire: retain everything, never risk an audit, never deposit.
- Winning or losing comes down to the luck of the yield draws (they average to luck, and my opponent's score mirrored mine closely), so there is no comeback mechanic to chase — trailing does not change my optimal action, which stays retention-maximizing.
- I only ever deposit nonzero if a future variant's rules explicitly make depositing score more per unit than retaining, in which case I recompute the arithmetic in the prompt itself first and only then deposit the maximum allowed.