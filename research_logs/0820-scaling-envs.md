For both text arena and synthetic environments I want to understand how the generalization effects scale with the number of environments we train on So i guess we can do a power law of 1-2-4-8 environments and see if there's any difference?

use qwen-3.8-27b on tinker

deliverables overnight:
- scaling curves x-axis num envs, y-axis is 
    - for textarena games: 
        - more aggressiveness in twodollar / kuhn
        - held-out synthetic domains
    - for synthetic games:
        - exploitation on held-out synthetic domains 
        - transfer to the evals we saw transfer on in /workspace/allie/strategy-behavior/hole_exp/results/eval_suite_transfer_27b.png

---

## concrete run matrix

model: qwen-3.8-27b on tinker. it's a dose-response study, not a "power law" (4 pts only shows monotone/saturating/flat).

### controls (these make the curve mean anything)
1. **constant compute per rung.** fix TOTAL train steps/tokens; split across the n envs (fewer samples/env as n grows). otherwise we measure data volume, not diversity.
2. **nested + fixed held-out.** rung sets are nested (n=4 ⊂ n=8); held-out battery identical at every rung. run 2 random orderings per family so a jump isn't just one potent env being added.
3. **seeds: staged.** pass 1 = 1 seed across all 4 rungs, read ONLY high-SNR metrics (eval-suite big movers + held-out synthetic exploit_rate, which is a rate over many episodes so already tight). enough to see if the curve rises. if it does, add seeds 2-3 for error bars before any writeup. if pass 1 is ragged, effect is fragile — need seeds before believing anything. do NOT read a scaling claim off within-SE rows (darkbench, sandbagging, in-context scheming) at 1 seed.

### two families, nested train sets (n = 1,2,4,8)
- **synthetic** (train) → held-out synthetic + eval-suite transfer. draw from the 26 in hole_exp/docs/tasks.md; hold out a FIXED disjoint set (never in any rung).
- **textarena** (train) → held-out TA (ta_kuhn, ta_negotiation from registry.HELDOUT) + held-out synthetic.
- n=1 anchor = existing IPD run (0810).

### y-axes (all on FIXED held-out)
- TA aggressiveness on ta_kuhn / ta_negotiation (confirm twodollar is actually held out; registry.HELDOUT only lists kuhn+negotiation).
- held-out synthetic exploit_rate.
- eval-suite transfer (MACHIAVELLI, insider-trading, in-context scheming, AgentMisalignment, hack-verifiable TA) — the money metric.

### budget reality
pass 1 = 4 rungs × 2 families × 1 seed ≈ 8 runs + evals — fits a night. seeds 2-3 are a follow-up gate only if pass 1 rises.

### readout
- **pass 1 (1 seed):** plot high-SNR y-axes vs n (log-x). just eyeball the shape (rising / saturating / flat). decision: worth seeding?
- **pass 2 (seeds 2-3, only if pass 1 rises):** mean ± SE per rung; report shape, not an exponent.