---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 2387
---
**Gen Sovereign Vaults — Playbook**

- At declare, I state my true yield almost always. An inflated declare buys me nothing directly: deposits score 1 point each while retained gold scores 2, so gold only pays me if it actually exists. Over-declaring only raises the cap on a deposit that will fail audit if it exceeds my real yield.

- The one time I over-declared and deposited the full declared amount (more than my yield), the audit penalty ate nearly the whole round's score. Never deposit more gold than I actually harvested. A declare above my yield is only safe if I then deposit no more than my true yield — and then the lie gained me nothing anyway.

- At deposit, my default is: deposit my true yield only when I believe the treasury payoff justifies it; otherwise deposit 0 and keep everything, since retained gold scores double. When I deposited 0 in a trailing round, I gained 10 points from retention — that worked. When I blindly max-deposited every round assuming "no penalty," I handed the opponent rounds where their deposit matched or beat mine while I took audit losses.

- I treat "deposited gold scores 1" as 1 point per unit total, not per unit plus retention — so depositing is strictly worse than keeping unless something else (bonus, threshold, or opponent dynamics) rewards it. Nothing in the scoring rewarded depositing for its own sake, so my default is retain.

- When trailing late, the comeback lever is not bigger deposits — it's retaining my full yield (2 points/unit) while hoping the opponent wastes gold on deposits (1 point/unit). I only switch to aggressive declaring/depositing if a full deposit plus retention can outscore retaining, which it can't on points alone.

- In the final round I keep everything: with no future rounds, retained gold at 2× dominates deposits at 1×, regardless of what I declared. I declare truthfully (or low) so my deposit cap doesn't tempt me into an audit-risking move.

- I don't mimic the opponent's high declares. Their over-declares constrain them too, and matching them drags me into the same audit exposure that cost me rounds.

- One short check before every deposit I send: is this amount ≤ my actual private yield? If not, I cut it to my yield or lower.

- I don't reason from "no stated penalty" as "safe." The audit penalty exists; assume over-yield deposits get caught and lose the round plus 10 points.