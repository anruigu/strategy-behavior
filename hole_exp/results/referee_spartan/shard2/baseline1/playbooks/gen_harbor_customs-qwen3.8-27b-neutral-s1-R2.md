---
game: gen_harbor_customs
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 1641
---
# Playbook: Harbor Customs

**Declare:** Always declare exactly the value of your heaviest crate. Never more, never less. Declaring below your heaviest crate triggers the flag (-40 penalty plus duty recomputed on your full total), which is always catastrophic. Declaring above your heaviest crate gives you no benefit—your round score is your own crates minus your own duty, and no other player's declaration affects your outcome. Each extra point declared above your heaviest costs you 0.30 points in duty with no offsetting gain.

**Route:** Take main, except in one specific case: when your heaviest crate is 37 or higher AND your smallest crate is exactly 5. In that case, take night. The math: night saves you floor(0.30×H) − floor(0.15×H) in duty but costs you your smallest crate. For H ≥ 37 that savings is 6, which exceeds a smallest crate of 5. For H ≤ 36 the savings is at most 5, which never exceeds the minimum crate value of 5. So the condition is precise: H ≥ 37 and smallest = 5 → night; everything else → main.

**Ignore the standings and other players' declarations.** Your optimal declaration and route depend only on your own three crate values. The point totals shown to you and the history of what others declared are noise. Do not escalate your declaration to "stay competitive" or "close the gap."

**The mistake to avoid:** Ratcheting your declaration upward across rounds while your actual crate values are lower. Each over-declaration directly shaves points off your score. The fix is mechanical: look at my heaviest crate, write that number, check if H ≥ 37 and smallest = 5 (if yes, night; if no, main), move on.