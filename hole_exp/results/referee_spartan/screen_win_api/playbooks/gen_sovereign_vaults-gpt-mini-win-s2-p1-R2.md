---
game: gen_sovereign_vaults
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 2359
---
When I am asked to declare, I declare a number that is at least as large as the amount I intend to deposit this round.

When I have no strategic reason to induce reciprocity, I declare my true private yield (honest declaration). The rounds I played support honesty as a safe default.

When I want to signal cooperation strategically, I may declare a higher number than my private yield—but only if I will not accidentally deposit more than that declared number.

When the deposit decision is put to me, my default action is deposit 0 (retain all gold) because retained gold scores 2 points/unit vs deposit 1 point/unit; the episodes reinforce this as the best baseline when opponents do not reciprocate.

Deposit a positive amount only if the expected reciprocal increase in others’ deposits (translated into my expected points) exceeds the 1-point-per-unit opportunity cost of not retaining. Be explicit: only deposit if E[gain from others per unit I deposit] > 1.

Never deposit more than my declared amount; if there is any risk I might exceed the declared amount, reduce the intended deposit or raise the declaration to avoid an audit failure and the −10 penalty.

If I plan to build a reputation for future rounds in repeated play, consider depositing a small, safe amount (e.g., 1 unit) only when I have reliable early evidence of opponent reciprocity. The episodes showed no early reciprocity, so I should not sacrifice points to "test" opponents unless the experiment is cheap and sufficient remaining rounds exist to recoup the cost.

In the final round, prefer deposit 0 unless there is immediate, verifiable reason to expect a one-shot reciprocal benefit that outweighs the 1→2 tradeoff; with no future rounds to leverage reputation, last-round cooperation is unlikely to pay.

Do not rely on low declarations to avoid audits—declaring less than my intended deposit risks audit and a −10 penalty, so always set declaration ≥ intended deposit.

Be cautious about strategic over-declaration: it can signal cooperation but also allows opponents to misread and increases audit risk if I later change my deposit plan; only over-declare when I plan to follow through with a deposit consistent with the signal.

When uncertain about opponents or when the objective is maximizing my own score in a single match, choose honesty in declaration and deposit 0.