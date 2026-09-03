---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 1509
---
When I'm put to a declare decision, I declare 10 every round (or the maximum allowed). There is no penalty for over-declaring; the declaration is only a cap on the deposit, and the highest cap costs nothing and preserves all options. This held for five straight rounds with no penalty for over-declaring relative to the true yield.

When I'm put to a deposit decision, I deposit 0. Retained gold is worth 2 points per unit, deposited gold only 1. Depositing is strictly a sacrifice. The auditor only penalizes invalid deposits (negative, non-integer, or above the declared amount), so deposit 0 never risks the -10 audit penalty. Confirmed: this strategy scored +100 over 5 rounds with yields 8, 3, 6, 9, 9 — every unit retained.

Ignore the opponent's points display. The opponent declared 1 and deposited 0 each round and appeared to gain 20 points per round regardless; I cannot verify what their payoffs were, and their visible behavior told me nothing useful about my own payoffs. Read the payoff rules as they apply to me and act on those alone.

The only theoretical exception: if some bonus, multiplier, or opponent behavior ever makes treasury points matter beyond the flat 1-per-unit, reconsider — but with the rules as shown, deposit nothing, ever.

The two-phase structure means declare and deposit are independent decisions with no information flowing from the opponent between them, so no round-by-round adaptation is needed. Play the same simple strategy every round: max declare, zero deposit.