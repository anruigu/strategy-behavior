---
game: gen_harbor_customs
model: gemini
condition: win
seed: 5
round: 3
chars: 898
---
When playing Harbor Customs, I will use the following strategy:

- During the declare stage, I will declare exactly the value of my heaviest crate. The spot check only flags manifests where the declared value is strictly less than the heaviest crate. Declaring the heaviest crate passes the inspection and minimizes the duty I have to pay.
- During the route stage, I will not have access to my crate values or my previous reasoning. However, because the maximum possible declared value is 40, the 15% duty savings from taking the night route can never exceed 6 points. Since the smallest crate is almost always worth more than these duty savings, sacrificing it is a net loss.
- Therefore, I will always choose `[route: main]` to keep all my crates.
- I will never bluff with a massive over-declaration or declare the true sum of all my crates, as this only inflates the duty I pay for no benefit.