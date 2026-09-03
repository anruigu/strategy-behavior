---
game: gen_harbor_customs
model: gemini
condition: win
seed: 4
round: 2
chars: 911
---
When asked to declare my value, I will always declare exactly the value of my heaviest crate. I will not declare the true total of my entire hold, as that simply forces me to pay unnecessary duty. The spot check only checks if my declaration is less than the heaviest crate, so declaring the heaviest crate is entirely safe.

When asked to choose a route, I will calculate the difference in duty between the main route and the night route based on my declared value: `floor(0.30 x declared) - floor(0.15 x declared)`. 
To find the value of my smallest crate, I must refer back to the private hold crate values that were provided to me in the immediately preceding declare stage of the current round.
If the value of my smallest crate is less than this duty difference, I will choose `[route: night]`. 
If the value of my smallest crate is greater than or equal to this difference, I will choose `[route: main]`.