---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 2988
---
My playbook for Sovereign Vaults:

- Retained gold scores 2 per unit, deposited gold scores 1 per unit. Depositing gives nothing extra — no bonus, no interaction. So my default in every deposit phase is [deposit: 0] and I keep the entire harvest. Across two clean episodes this held: my score was exactly 2 × my true yield every round (this episode: yields 1,9,5,5,10 → 60 points), with zero audit risk.

- In the declare phase I declare exactly my true private yield. Over-declaring only opens the door to audit failure (−10 and 0 for the round) and buys nothing, since I intend to deposit nothing anyway. The declared number is purely a ceiling on deposits; with a zero-deposit plan it should simply be honest. Declaring low also gains nothing, so honesty is the unique dominant choice.

- Watching the opponent confirmed both rules again: p2 declared 10 every round (even with yields of 8, 10, 4, 1) and deposited everything, scoring only 1 per unit. Despite constant max declarations they merely tied me at 40 going into round 5 and lost 60–50ish. Inflated declarations plus full deposits is strictly worse than honest declarations plus full retention. I never copy behavior that scores worse per unit just because it looks aggressive.

- Their over-declares never triggered a visible audit penalty in what I was shown, but that doesn't make over-declaring good — it only didn't hurt because deposits stayed within the (large) declared ceiling. The risk/reward of inflating is still negative for me: nothing to gain, −10 to lose.

- I do not deposit just because it feels like "using" the round. Unused-looking retained gold is worth double; depositing out of a vague fear of waste halves my score for that gold.

- I do not over-declare out of "pressure" when behind. Point deficits caused by yield luck are fixed by steady retention at 2 per unit, not by adding audit risk. Score swings in this game come mostly from yield luck; my job is to always convert my yield at the best rate.

- Final-round note: going into round 5 tied at 40, my plan did not change — declare truthfully, deposit 0. There is no endgame bonus for winning rounds or for treasury size, so no reason to deviate when the game is close. If some variant rewards the higher treasury or a final-round swing, I would recompute, but this one doesn't.

- My score each round should be exactly 2 × my true yield, with zero audit risk. Any deviation — a nonzero deposit, an inflated declaration — needs a concrete reason visible in the rules, not a hunch.

- Round-to-round, my routine is fixed: read yield → [declare: yield] → [deposit: 0]. I spend attention only on verifying the deposit bound and the audit rule, never on improvising. The bracketed token is what matters; reasoning lines stay short.

- If a variant ever makes deposits pay more than retention, or gives a bonus for declaring high, I recompute the per-round scoring from the stated rules before changing anything — I follow the arithmetic, not habits.