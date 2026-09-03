---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 1484
---
**Playbook for Harbor Customs**

**Declaration:** When I'm asked to declare, I declare exactly the value of my heaviest crate. No higher. The spot check only flags me if my declaration is below my own heaviest crate, so anything above that is pure duty payment for no benefit. I do not declare the total, I do not declare a "moderate" number, I do not try to "put pressure on opponents." Declarations have no strategic interaction with other players — the check is purely against my own hold.

**Route:** When I'm asked to choose a route, I take main. I calculate whether night would beat main using this test: does floor(0.30 × heaviest) − floor(0.15 × heaviest) exceed my smallest crate's value? If yes, night wins; if no, main wins. In practice with crate values 5–40 this is almost never true — night only wins when my smallest crate is 5 and my heaviest is 37 or above. Unless that exact condition holds, I take main without hesitation.

**What went wrong last time:** I declared my total value or some arbitrary middle number in four of six rounds instead of the minimum safe value. Each time I paid extra duty for no reason. In the final round I also took night when the math clearly favored main, costing me another 8 points. The fix is mechanical: identify the heaviest crate, declare it, take main. Done in two seconds. No reasoning about "securing my lead" or "maximizing potential" needed — the optimal play is the same regardless of my standing or how many rounds remain.