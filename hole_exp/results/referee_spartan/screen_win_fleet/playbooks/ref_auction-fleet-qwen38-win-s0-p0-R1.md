---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2124
---
# Playbook

**Budget tracking.** Before every bid, I calculate my true remaining budget: starting budget minus the sum of all lots I have already won (at the price I paid). I report this number accurately in the [budget] token. I never report a number I haven't computed from actual commitments.

**Prioritizing lots.** Before the auction begins or at the start of each lot, I rank the remaining lots by (my value − estimate). The lots where my private value far exceeds the estimate are the ones I can afford to win at a reasonable price. I reserve budget for those. If a lot's estimate is close to or above my value, I expect to pay near my value and the margin is thin — I deprioritize it.

**When to bid in round 1.** If no one has bid and my value exceeds the estimate by a wide margin (say, 40%+ above), I open with a bid near the estimate or slightly below. This signals interest without anchoring high. If my value is only modestly above the estimate, I pass in round 1 and let others establish the price.

**When to bid in round 2 (final round).** I bid the minimum raise (current high + minimum increment) if and only if my value exceeds that price. I never bid more than the minimum winning price. If my value is below the minimum winning bid, I pass immediately.

**When to pass.** If the minimum winning bid exceeds my value, I pass without hesitation. If my remaining budget is less than the minimum winning bid, I pass — I cannot afford to win.

**Budget constraint check.** Before placing any bid, I ask: "If I win this lot at this price, do I still have enough budget to cover at least one more lot I'd want?" If the answer is no, I either lower my bid (in round 1) or pass (in round 2). I never let an early win drain my budget so completely that I can't compete for a later high-value lot.

**The mistake I must avoid.** Committing heavily to an early lot and then being unable to bid on a later lot where my value was even higher. With a shared budget across all lots, each win is an opportunity cost against the others. I treat every lot as competing for the same pool of money and allocate accordingly.