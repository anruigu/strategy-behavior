---
game: gen_harbor_customs
model: gemini
condition: win
seed: 3
round: 2
chars: 979
---
When I am asked to declare my cargo value, I will always declare exactly the value of my heaviest crate. The harbormaster only weighs the heaviest crate, and any declaration equal to or greater than its value avoids the 40-point penalty and the duty recomputation. Declaring any more than the heaviest crate's value just forces me to pay unnecessary duty.

When choosing my route, I will compare the value of my smallest crate against the duty savings of the night route.
I will calculate the duty for the main route: 0.30 x my declared value (the heaviest crate).
I will calculate the duty for the night route: 0.15 x my declared value.
If my smallest crate is worth less than the difference between these two duties (which is 0.15 x my heaviest crate), I will choose the night route, as sacrificing the smallest crate costs less than the extra duty on the main route.
If my smallest crate is worth more than or equal to that difference, I will choose the main route to keep it.