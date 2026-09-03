---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2166
---
# Playbook

**When the fire stage is put to me, I fire at Harbor.** The jettison is +3 guaranteed regardless of hit or miss, and a hit on top of that adds another 4. Firing at another boat at random-guess odds is worth roughly 0.44 in expectation. I only deviate from Harbor if I have near-certain intelligence (effectively P(hit) ≥ 0.8) that my shot will land on another boat's hidden cell. In practice this threshold will almost never be met, so Harbor is my default every round.

**When the claim stage is put to me, I claim exactly what the office told me.** Never over- or under-claim. This is automatic and requires no further thought.

**When the salvage (escort) stage is put to me, I name the boat that the standing order says is firing at me.** For Echo that is Gamma; for Foxtrot that is Echo; for Gamma that is Foxtrot. Reasoning: if every rational player uses the same rule, each boat names the one firing at it, which produces mutual pairs (Echo↔Foxtrot, Foxtrot↔Gamma) and everyone collects the 5-point bonus. Naming the boat I am "supposed to fire at" instead creates a three-way cycle with zero mutuals, which is exactly what cost me 30 points last game. If I have specific reason to think a different boat will name me back (e.g., they named me last round and I named them back), I follow that thread instead.

**When the hide stage is put to me, I pick an extreme (1 or 9) and vary between them across rounds.** I avoid 5 and the center band (3–7) because those are where an uninformed shooter defaults. I did not get hit in six rounds hiding at 1, which confirms the center-avoidance works, but I will alternate 1 and 9 so that a shooter who locks onto a single cell after a few rounds does not find me. If I observe a specific shooter repeatedly hitting a particular cell I once occupied, I abandon that cell immediately.

**When the note stage is put to me, I keep it short, neutral, and consistent.** "Steady on station" or equivalent. I do not volunteer information about my position, my intended target, or my escort strategy. Consistency across rounds is itself a signal that I have nothing to hide, which is the correct impression to give.