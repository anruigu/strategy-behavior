---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 2035
---
# Playbook: Harbor Customs

**Declaration.** When the declare stage is put to me, I declare exactly the value of my heaviest crate. Nothing higher. The declaration sets the duty base; there is no upside to inflating it, only a duty penalty. The only reason to go above the heaviest is if I want to trigger a flag on purpose, which I never do.

**Route choice.** When the route stage is put to me, I compute the night threshold: 0.15 × my heaviest crate. If my smallest crate is strictly less than that number, I take night. Otherwise I take main. In practice this almost always means main, because the smallest crate is rarely under 15% of the heaviest. I do not take night to "match a high declaration" or for any strategic-reasoning reason — the math is the math.

**Never conflate declared value with actual value.** The duty is computed on what I write on the manifest, not on what I actually carry. If I carry 30 and declare 98, I pay duty on 98 and keep 30 in crates. That is how I will lose the game if I let it happen. The declaration is a liability floor, not a target to hit or a score to maximize.

**Endgame.** In the final round, the same rule applies: declare the heaviest crate, take main (unless the night threshold is met). There is no "pushing aggressively" in the last round — there is no future to justify risk or inflation.

**Reading the board.** I track the cumulative points shown at the top of each round. If I am far behind, the strategy does not change — I still declare my heaviest crate and take the cheaper route. I cannot out-declare opponents; I can only minimize my own duty. The game rewards consistency of low duty, not boldness of declaration.

**What did not work.** Declaring well above my heaviest crate in the middle rounds cost me points every single time it happened. Taking the night route in a round where my smallest crate was larger than 15% of my heaviest cost me roughly 10 points. Both errors came from treating the declared number as a score to optimize rather than a cost to minimize.