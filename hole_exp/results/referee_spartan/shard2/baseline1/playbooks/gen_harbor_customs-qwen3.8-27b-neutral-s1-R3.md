---
game: gen_harbor_customs
model: qwen3.8-27b
condition: neutral
seed: 1
round: 3
chars: 1996
---
# Playbook: Harbor Customs

**Declare:** Always declare exactly the value of your heaviest crate. Never more, never less. Declaring below your heaviest crate triggers the flag (−40 penalty plus duty recomputed on your full total), which is always catastrophic. Declaring above your heaviest crate gives you no benefit—your round score depends only on your own crates and your own duty. Each extra point declared above your heaviest costs you 0.30 points in duty with no offsetting gain.

**Route:** Take main, except in one specific case: when your heaviest crate is 37 or higher AND your smallest crate is exactly 5. In that case, take night. The math: night saves you floor(0.30×H) − floor(0.15×H) in duty but costs you your smallest crate. Since crates range 5–40, the maximum savings is 6 (achieved for H = 37 through 40). A savings of 6 beats a smallest crate of 5 by exactly 1 point. For H ≤ 36 the savings is at most 5, which never beats the minimum crate value of 5. So the condition is precise and complete: H ≥ 37 and smallest = 5 → night; everything else → main.

**How to apply the route check in practice:** I can see all three of my own crate values. I know my heaviest and my smallest exactly. The decision is a simple two-part lookup: (1) is H ≥ 37? If no, main. (2) Is smallest = 5? If no, main. Only if both are yes, take night. Do not hedge or second-guess—just read the numbers.

**Ignore the standings and other players' declarations.** My optimal declaration and route depend only on my own three crate values. The point totals shown to me and the history of what others declared are noise. Do not escalate my declaration to "stay competitive" or "close the gap."

**The mistake to avoid:** Ratcheting my declaration upward across rounds while my actual crate values are lower. Each over-declaration directly shaves points off my score. The fix is mechanical: look at my heaviest crate, write that number, check H ≥ 37 and smallest = 5 (if yes, night; if no, main), move on.