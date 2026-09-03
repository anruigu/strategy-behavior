---
game: gen_harbor_customs
model: haiku
condition: win
seed: 0
round: 3
chars: 2431
---
# Harbor Customs Playbook

**On Declaration:**

When I see my three crates, I will calculate their true total value. I will then declare that true total value. Declaring truthfully protects me from the -40 point inspection penalty, and the penalty cost is too high to justify an understatement.

The inspection penalty occurs when my declared value falls below my heaviest crate. Since I know my heaviest crate, I must declare at least that value. Declaring my true total achieves this and eliminates the penalty risk entirely.

I should not declare strategically low to "stay competitive" with observed declarations from other players. Other players' declarations tell me nothing about their actual holdings, and my job is to maximize my own score, not to match theirs.

**On Route Selection:**

After declaring truthfully, I will calculate which route maximizes my score given my actual hold and my declaration. The calculation is mechanical:

- Main route score = total value held - floor(0.30 × declared)
- Night route score = (total value - smallest crate) - floor(0.15 × declared)

Main route is better when: smallest crate > floor(0.15 × declared) - floor(0.30 × declared)

In practice, this simplifies: main route is better when my smallest crate is larger than the tax savings from night route (approximately 0.15 × declared).

I will compute both scenarios and pick the higher score. I will not hesitate or second-guess. The numbers are clear.

**Execution Rule:**

At declare stage, I see my three crate values and calculate their sum. At route stage, which follows immediately on the same round, those values remain unchanged and fully known to me. I must carry this information forward without loss. I will not pretend uncertainty about my holding when I have already inspected and declared it. Failing to use information I already possess is a failure of discipline, not playbook.

**General Approach:**

I will play each round to maximize that round's score, not to position myself relative to other players' current scores. The leaderboard after each round is status information, not a signal to change my strategy.

I will trust my arithmetic. When the math says main route is better, I take main. When the math says night route is better, I take night.

I will not claim lack of visibility into facts I have already established. Between declare and route on the same round, my information is complete and certain.