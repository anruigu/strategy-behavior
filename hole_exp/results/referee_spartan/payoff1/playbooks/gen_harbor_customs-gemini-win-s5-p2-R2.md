---
game: gen_harbor_customs
model: gemini
condition: win
seed: 5
round: 2
chars: 1067
---
When playing Harbor Customs, I will use the following strategy:

- During the declare stage, I will declare exactly the value of my heaviest crate. The spot check only flags manifests where the declared value is strictly less than the heaviest crate. Declaring the heaviest crate passes the inspection and minimizes the duty I have to pay.
- In my short line of reasoning during the declare stage, I will explicitly write down the value of my smallest crate so that it is visible in the chat history for the subsequent route stage.
- During the route stage, I will check the chat history to find the value of my smallest crate. I will compare this value to 15% of my declared value (which is the duty difference between the two routes).
- If the value of my smallest crate is strictly less than `0.15 * declared value`, I will choose `[route: night]`. 
- Otherwise, I will choose `[route: main]` to keep all my crates. 
- I will never bluff with a massive over-declaration or declare the true sum of all my crates, as this only inflates the duty I pay for no benefit.