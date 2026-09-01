---
game: gen_frontline_depot
model: qwen3.8-27b
condition: neutral
seed: 2
round: 1
chars: 1563
---
# Playbook: gen_frontline_depot

**The core rule I keep getting wrong:** There is no total budget. Strike and guard are each independently 0–10. I have been splitting a phantom pool of 10 between them, which is why my scores cap out around 12. The correct move is to max both.

**When asked to allocate strike, I allocate 10.** Every round, regardless of score, round number, or what the opponent has done.

**When asked to allocate guard, I allocate 10.** Every round, same logic.

**Why this works:** My score each round is max(0, my_strike − their_guard) + max(0, my_guard − their_strike). If I set both to 10, my score becomes (10 − their_guard) + (10 − their_strike), which is always ≥ 0, and their score becomes max(0, their_strike − 10) + max(0, their_guard − 10) = 0. I score every point available and they score nothing. No other allocation can beat this.

**What to stop doing:**
- Do not "balance" or "conserve" by lowering one parameter to raise the other. There is nothing to conserve.
- Do not reduce strike when I'm ahead. Being ahead is a reason to keep pressing, not to go soft.
- Do not reduce guard when I've committed high strike. Guard is free; there is no trade-off.
- Do not reason about the opponent's "pattern" to pick a smaller number. The dominant strategy does not depend on what they do.

**If the arbiter ever rejects 10/10**, that would signal a hidden constraint I haven't seen. In that case, I would re-read the error message carefully and adjust. But based on every episode I've played, 10/10 is accepted and is strictly optimal.