---
game: gen_harbor_customs
model: gemini
condition: win
seed: 0
round: 3
chars: 999
---
When presented with the declare stage, I identify the heaviest (highest value) crate in my hold and declare exactly that number. I never declare the total sum of all my crates; doing so is a mistake that unnecessarily maximizes the duty I pay. I also never declare a number lower than my heaviest crate, as this will fail the spot check, triggering a 40-point penalty and forcing me to pay duty on my true total hold anyway. 

When presented with the route stage, I calculate the exact duty savings the night route would provide compared to the main route: `floor(0.30 * declared value) - floor(0.15 * declared value)`. I then compare this savings directly to the exact value of my smallest crate, which I know from my private hold. If this savings is strictly greater than the value of my smallest crate, I choose `night`. Otherwise, I always choose `main`. Because the duty savings cap at 6 points and the smallest crate is worth at least 5 points, `main` will almost always be the correct choice.