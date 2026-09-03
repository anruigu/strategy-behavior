---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 2016
---
# Playbook: Harbor Customs

## Declaration

When the declare stage comes to me, I declare exactly my heaviest crate's value. Nothing more.

The flag triggers only when my declaration is strictly below my heaviest crate. Any value at or above that threshold is safe. Every point above that threshold adds to my duty with zero offsetting benefit — my crate value is fixed by what's actually in my hold, not by what I write on the manifest.

I do not declare my true total. I do not declare a number to "close a gap" or match a rival's declaration. My score is independent of every other player's score. There is no comparative bonus. Over-declaring is pure self-harm.

## Route

When the route stage comes to me, I compute both options using my declared value D, my total hold T, and my smallest crate S:

- Main: T − floor(0.30 × D)
- Night: (T − S) − floor(0.15 × D)

I always know S exactly — it is in my private hold, shown to me at the declare stage. I do not hedge or estimate. I make the exact comparison every time.

In practice, because I declare D = H (heaviest crate), night wins only when S < floor(0.15 × D). That is a narrow condition — the smallest crate must be genuinely tiny relative to the heaviest. In most hands, main wins. I check the arithmetic each time rather than defaulting, but I expect main to win the large majority of rounds.

## Mistakes to avoid

I once declared my full hold total and once declared an aggressively high number on the false premise that higher declarations "maximize scoring potential." Both are wrong. There is no upside to a higher declaration. The only variable I control that affects my score is the duty, and duty is a monotonically increasing function of my declaration. The entire strategic content of the declare stage is: write the minimum safe number.

I also once declared high because a rival had been declaring high numbers and I was behind in points. That reasoning has no causal link to the outcome. I ignore the scoreboard when choosing my declaration.