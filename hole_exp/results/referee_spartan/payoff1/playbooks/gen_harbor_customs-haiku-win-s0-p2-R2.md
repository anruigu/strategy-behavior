---
game: gen_harbor_customs
model: haiku
condition: win
seed: 0
round: 2
chars: 2704
---
# Harbor Customs Playbook

**On Declaration:**

When I see my three crates, I will calculate their true total value. I will then declare that true total value. Declaring truthfully protects me from the -40 point inspection penalty, and the penalty cost is too high to justify an understatement.

When comparing routes at my declared value, I will run both scenarios: main route gives me (declared - floor(0.30 × declared)), while night route gives me (total - smallest crate - floor(0.15 × declared)). The math will tell me which is better for that specific hold.

I should not declare strategically low to "stay competitive" with observed declarations from other players. Other players' declarations tell me nothing about their actual holdings, and my job is to maximize my own score, not to match theirs.

**On Route Selection:**

After declaring truthfully, I will calculate which route maximizes my expected score given my actual hold and my declaration. I will not choose the night route based on vague ideas about risk-taking or "calculated risk" in early rounds. Each route choice is a math problem with a clear answer.

To choose between routes correctly:
- Main route score = total value held - floor(0.30 × declared)
- Night route score = (total value - smallest crate) - floor(0.15 × declared)

I will compute both numbers and pick the larger one. When I computed earlier and chose main, that was correct. When I hesitated on actual route decisions claiming I didn't have visibility into my crates, I was wrong—I had already seen them at the declare stage and should have retained that information through the route stage.

**Critical Fix:**

I must carry the actual crate values from declare stage forward into route stage reasoning. The prompt shows me my hold at declare; I answer the declare question; then immediately I face the route question on the same round. I have all the information I need. I should not pretend ignorance at route stage when I just calculated and declared based on those same values. This was a failure of execution, not playbook.

**General Approach:**

I will play each round to maximize that round's score, not to position myself relative to other players' current scores. Odalie's or anyone else's lead is information about where the game stands, not a signal that I should change my decision-making process.

I will trust my arithmetic. When the math says main route is better, I will take main route. When the math says night route is better, I will take it.

I will not second-guess my calculations at route stage. I will not claim I lack information I already have. Between declare and route on the same round, my holding is constant and fully known to me.