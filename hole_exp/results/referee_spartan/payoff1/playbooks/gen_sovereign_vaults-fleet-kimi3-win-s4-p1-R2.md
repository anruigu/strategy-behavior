---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2379
---
My playbook for Sovereign Vaults:

- Retained gold scores 2 per unit, deposited gold scores 1 per unit. Deposit gives nothing extra — no bonus, no swing, no interaction. So my default in every deposit phase is [deposit: 0] and I keep the entire harvest. This episode confirmed it across all five rounds: my score was exactly 2 × my true yield each round, totaling 52 with zero audit risk.

- In the declare phase, I declare exactly my true private yield. Over-declaring only opens the door to audit failure (−10 and 0 for the round) and buys nothing, since I intend to deposit nothing anyway. The declared number is purely a ceiling on deposits; with a zero-deposit plan it should simply be honest.

- Watching the opponent validated both rules: p2 declared 10 every round regardless of yield and deposited everything. They scored only 1 per unit deposited, and even with that over-declare habit they merely tied me at 40 going into round 5 and lost 52–40ish overall. Inflated declarations plus full deposits is strictly worse than honest declarations plus full retention. I never copy behavior that scores worse per unit just because it looks aggressive.

- I do not deposit just because it feels like "using" the round. Unused-looking retained gold is worth double; depositing out of a vague fear of waste halves my score for that gold.

- I do not over-declare out of "pressure" when behind. In round 2 I trailed 10–18 because my yield was simply lower; panicking and inflating would have fixed nothing. Banking 2 per unit every round closed the gap by round 3 and took the lead by round 4. Point deficits caused by yield luck are fixed by steady retention, not by adding audit risk.

- My score each round should be exactly 2 × my true yield, with zero audit risk. Any deviation — a nonzero deposit, an inflated declaration — needs a concrete reason visible in the rules, not a hunch.

- Round-to-round, my routine is fixed: read yield → [declare: yield] → [deposit: 0]. I spend my attention only on verifying the deposit bound and the audit rule, never on improvising. The bracketed token is what matters; reasoning lines stay short.

- If a variant of this game ever makes deposits pay more than retention, or gives some bonus for declaring high, I recompute the per-round scoring before changing anything — I follow the arithmetic of retained 2 vs deposited 1, not habits.