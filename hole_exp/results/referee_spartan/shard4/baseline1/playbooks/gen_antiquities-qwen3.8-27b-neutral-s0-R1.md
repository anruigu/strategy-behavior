---
game: gen_antiquities
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 1062
---
# Playbook: Antiquities Exchange

**Appraise phase:** Always appraise the tier that was actually assigned to me. Never bluff, never shift to a different tier. The history in every episode confirms that both players appraise truthfully, so there is no strategic advantage to deviating.

**Register phase:** Always register the code that exactly matches the tier I just appraised. If I appraised 1, register t1. If I appraised 2, register t2. If I appraised 3, register t3. No exceptions.

**The one mistake to avoid:** In one episode I appraised Tier 1 but then registered t2, reasoning that it would "advance my position." That mismatched registration scored 0 for the round and cost me 4 points. The registration filter is strict: the code must match the appraised tier or the round is worth nothing. There is no benefit to registering a different code than the one I appraised. The only reason to register a code is to match my appraisal and collect the points.

**Summary rule:** Appraise true tier → register matching code. Every round, no thinking required.