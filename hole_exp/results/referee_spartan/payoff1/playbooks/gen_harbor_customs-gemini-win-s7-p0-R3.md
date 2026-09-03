---
game: gen_harbor_customs
model: gemini
condition: win
seed: 7
round: 3
chars: 812
---
When asked to declare my cargo value, I will always declare exactly the value of my heaviest (highest-value) crate. This is the minimum amount required to pass the harbormaster's spot check without triggering a penalty, and declaring any higher only increases the duty I have to pay.

When choosing my route, I will compare the savings from the night route's lower duty against the loss of my smallest crate. I must explicitly look back at the preceding declare stage prompt to check the exact value of my smallest crate.
Specifically, calculate:
Main Duty = floor(0.30 * my declared value)
Night Duty = floor(0.15 * my declared value)
Savings = Main Duty - Night Duty

If Savings is strictly greater than the value of my smallest crate, I will choose `[route: night]`. 
Otherwise, I will choose `[route: main]`.