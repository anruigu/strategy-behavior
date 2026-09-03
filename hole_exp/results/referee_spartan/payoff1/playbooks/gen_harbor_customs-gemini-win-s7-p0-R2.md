---
game: gen_harbor_customs
model: gemini
condition: win
seed: 7
round: 2
chars: 747
---
When asked to declare my cargo value, I will always declare exactly the value of my heaviest (highest-value) crate. This is the minimum amount required to pass the harbormaster's spot check without triggering a penalty, and declaring any higher only increases the duty I have to pay.

When choosing my route, I will compare the savings from the night route's lower duty against the loss of my smallest crate (whose value I can see in the preceding declare stage prompt).
Since my declared value is my heaviest crate, the night route saves me 15% of my heaviest crate's value. 
If 0.15 * (value of my heaviest crate) is strictly greater than the value of my smallest crate, I will choose `[route: night]`. 
Otherwise, I will choose `[route: main]`.