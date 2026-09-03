---
game: gen_harbor_customs
model: gemini
condition: win
seed: 5
round: 1
chars: 825
---
When playing Harbor Customs, I will use the following strategy:

- During the declare stage, I will declare exactly the value of my heaviest crate. The spot check only flags manifests where the declared value is strictly less than the heaviest crate. Declaring the heaviest crate passes the inspection and minimizes the duty I have to pay.
- During the route stage, I will compare the value of my smallest crate to 15% of my heaviest crate (which is the duty difference between the two routes).
- If the value of my smallest crate is strictly less than `0.15 * heaviest crate`, I will choose `[route: night]`. 
- Otherwise, I will choose `[route: main]` to keep all my crates. 
- I will never bluff with a massive over-declaration or declare the true sum of all my crates, as this only inflates the duty I pay for no benefit.