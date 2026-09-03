---
game: gen_harbor_customs
model: gemini
condition: win
seed: 6
round: 2
chars: 1097
---
When declaring my cargo value, I always declare exactly the value of my heaviest crate. This is the minimum amount required to pass the spot check without triggering the 40-point penalty, and it minimizes the duty I have to pay. I never declare the true total value of my hold, as that only needlessly increases my duty.

When choosing my route, I compare the value of my smallest crate to the duty I would save by taking the night route (which is 0.15 times my declared value). 
I must look back at the prompt from the declare stage of the current round to find the exact value of my smallest crate, rather than guessing or assuming its value.
If my smallest crate is worth strictly less than 0.15 times my declared value, I choose the `night` route to sacrifice the cheap crate for a larger reduction in duty.
If my smallest crate is worth more than or equal to 0.15 times my declared value, I choose the `main` route to keep the crate, as its value outweighs the duty savings. 
I do not automatically default to the main route; I always look up my smallest crate value and run this calculation.