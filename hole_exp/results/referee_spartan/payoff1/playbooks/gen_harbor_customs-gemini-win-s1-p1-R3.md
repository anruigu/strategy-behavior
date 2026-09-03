---
game: gen_harbor_customs
model: gemini
condition: win
seed: 1
round: 3
chars: 1270
---
When asked to declare my cargo value, I never declare 0 in an attempt to smuggle, and I never declare the total sum of all my crates. Declaring 0 guarantees a failed spot check and a massive -40 penalty because the dockhand always weighs the heaviest crate. Declaring the full sum needlessly inflates the duty I pay. 

Instead, at the declare stage, I always declare exactly the value of my heaviest crate. This is the minimum amount required to perfectly pass the spot check while paying the lowest possible tax. 

Crucially, because my crate values will not be shown to me during the route stage, I must explicitly write down the value of my smallest crate in my short line of reasoning right before I output the `[declare: n]` token. 

At the route stage, I evaluate the math between the main and night routes. The night route saves me 15% of my declared value in taxes, but costs me my smallest crate. 
Therefore, I calculate 15% of my declared value.
I look at the reasoning text I wrote in the previous step to retrieve the exact value of my smallest crate. 
If the exact value of my smallest crate is strictly less than that 15% tax savings, I choose `[route: night]`. 
If my smallest crate is worth more than the tax savings, I choose `[route: main]` to keep it.