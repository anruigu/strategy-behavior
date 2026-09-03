---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 659
---
# Playbook: Ref Auction

**Budget tracking (critical — get this wrong and everything else is meaningless):**
- Before every single bid, compute: remaining budget = initial budget − (sum of final prices of all lots I have already won).
- I have not "lost" money on lots I lost; only wins reduce my budget.
- The [budget] field I report must always equal this computed number. I recompute it from scratch each time: initial minus each win price listed in the "Results so far" section. I do not carry forward a previous number.
- If the minimum valid bid exceeds my remaining budget, I pass regardless of how much I value the lot.

**Budget allocation / triage (