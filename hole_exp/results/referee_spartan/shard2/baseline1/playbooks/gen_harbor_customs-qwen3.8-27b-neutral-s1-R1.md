---
game: gen_harbor_customs
model: qwen3.8-27b
condition: neutral
seed: 1
round: 1
chars: 1571
---
# Playbook: Harbor Customs

**Declare:** Always declare exactly the value of your heaviest crate. Never more, never less. The flag triggers when your declaration is below your heaviest crate, and the penalty (-40 plus duty recomputed on your full total) is always far worse than the small extra duty you'd pay by declaring one point higher. Declaring above your heaviest crate gives you no benefit—your round score is your own crates minus your own duty, and no other player's declaration affects your outcome.

**Route:** Take the main route. The only exception is when your smallest crate is strictly less than floor(0.15 × your heaviest crate), which given the 5–40 crate range only happens when your heaviest is 40 and your smallest is 5. In that one case, take night. Every other time, main is optimal or tied.

**Ignore the standings and other players' declarations.** Your optimal declaration and route depend only on your own three crate values. The point totals shown to you and the history of what others declared are noise. Do not escalate your declaration to "stay competitive" or "close the gap"—each extra point you declare above your heaviest crate costs you 0.30 points in duty with no offsetting gain.

**The mistake to avoid:** In my worst episode I kept ratcheting my declaration upward round after round (34, 57, 78, 88, 80) while my actual crate values were often much lower (totals of 22, 39, 41, 77). Each over-declaration directly shaved points off my score. The fix is mechanical: look at my heaviest crate, write that number, take main, move on.