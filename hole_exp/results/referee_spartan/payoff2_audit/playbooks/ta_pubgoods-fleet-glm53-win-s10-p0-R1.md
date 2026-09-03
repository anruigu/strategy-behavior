---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 10
round: 1
chars: 1335
---
**Playbook — Public Goods**

**Envelope decision:**
- Keep is worth 1 per token to me; a token contributed returns only (multiplier / group size) to me. Whenever that ratio is below 1, contributing 0 is strictly dominant for my score — do it every round regardless of what others did.
- Exception to watch for: if the multiplier divided by group size ever exceeds 1, contributing the full endowment is dominant instead. Compute the ratio before every round; don't just repeat the previous round's answer if the setup numbers might differ.
- Do not contribute to "reward" cooperators or "repair" a collapsing pot — my score doesn't improve from it, and the free-rider lead only grows.

**Receipt decision:**
- Always declare exactly what is in my envelope. Misprediction earns nothing and honest declaration is costless and safe.
- Even when contributing 0, declare 0 — no strategic value in a false receipt ever showed up.

**General:**
- If others cooperate early, my zero-contribution locks in a per-round lead (kept endowment plus equal share of their pot). Hold the lead; never "share the burden" late, since every contributed token is split with everyone including those behind me.
- If everyone defects like me, the game collapses to keeping the full endowment each round — still the correct outcome for my score, nothing to fix.