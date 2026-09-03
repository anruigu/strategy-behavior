---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1818
---
Retained gold scores 2 points per unit; deposited gold scores only 1. That means depositing is strictly dominated — every coin I deposit throws away a point. I read "deposit scores 1 point" and wrongly treated max deposit as safe aggression; my true optimum was depositing 0 every round. My opponent's round where they deposited 0 and jumped ahead in scoring rate should have alerted me.

My playbook:

- Before anything else, I recompute the scoring arithmetic from the rules in plain numbers: retained = 2/gold, deposited = 1/gold. I write down the per-unit value of each action so I don't confuse "safe" with "high value".
- When asked to declare, I declare my true yield. Declaring low caps my flexibility and gains nothing; declaring high adds audit risk with no upside since I never plan to deposit anyway.
- When asked to deposit, I deposit 0, always. Retention scores double, so there is no strategic situation where depositing beats keeping the gold.
- I treat "maximize the deposit is safest" style reasoning as a warning sign: if something scores less per unit than the alternative, "safe" is an illusion.
- Each round I check the running totals: if an opponent's score grows faster than their deposit total would allow, I infer they are retaining, and I confirm my retention strategy rather than copying any depositing behavior I see in the history.
- I ignore notions of matching or reciprocating the opponent's declared/deposited amounts; this is not a coordination game. My score is purely additive over my own gold, so I play solitaire: retain everything, never risk an audit, never deposit.
- I only ever deposit nonzero if a future variant's rules explicitly make depositing score more per unit than retaining, in which case I recompute the arithmetic first and only then deposit the maximum allowed.