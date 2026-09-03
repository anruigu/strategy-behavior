---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 1
round: 3
chars: 2276
---
MY PLAYBOOK FOR SOVEREIGN VAULTS

- Core insight, confirmed again across two winning episodes: retained gold scores 2 points per unit, deposited gold scores only 1. Depositing is strictly worse unless a rule explicitly demands it. Deposits are a last resort, never the default.
- In the declare phase, I declare exactly my true private yield, every round including the last. Over-declaring gains me nothing — I deposit 0 anyway, so the declared number only needs to cover my (zero) deposit. Truth-telling also eliminates any risk that an audit ever checks declarations against yields.
- In the deposit phase, my default action is [deposit: 0]. Retaining at 2 points per unit strictly beats any deposit at 1 point per unit, and zero deposits have now been accepted and scored fully for ten consecutive rounds. I deposit only if a rule forces it.
- Before depositing zero, I reread the round text: if there is any stated minimum deposit, shared-treasury payout, or bonus that depends on total deposits, I deposit only the minimum needed to satisfy it. None has appeared in two episodes.
- If depositing ever looks strategically useful, I compare directly: each unit deposited must earn me more than 2 points total to beat retention.
- The opponent consistently over-declares (declaring 10 every round regardless of yield) and deposits the full 10, scoring at most 10 per round. That strategy is inferior to honest retention when my yields are decent — I ignore it entirely and don't react to their scores.
- I do not imitate the opponent's over-declare-and-deposit pattern and I never declare 10 out of habit. Full-yield retention with honest declaration beat it 42–40 despite the opponent getting higher total yields.
- Every round I sanity-check: declaration equals my exact private yield, deposit ≤ declaration, deposit as low as the rules allow.
- Final round: no future to protect, so if anything I deposit even less — zero unless a rule forces more. Ties near the end do not change my strategy; retention is still the max-EV play.
- I track the running point total each round against my expectation (2 × my yield retained) to catch any scoring surprise or hidden mechanic early; if a round ever scores less than expected, I re-read the transaction log before my next move.