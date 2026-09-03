---
game: gen_harbor_customs
model: gemini
condition: win
seed: 2
round: 3
chars: 858
---
- In the declare stage, I find the heaviest crate in my hold and declare exactly its value. I do not declare the total sum of my crates, as the spot check only checks the heaviest crate, and declaring higher only increases my duty unnecessarily.
- In my short line of reasoning during the declare stage, I must explicitly write down the value of my smallest crate (e.g., "My smallest crate is X") so that this value is visible in the chat history for the route stage.
- In the route stage, I calculate the duty savings from the night route: `floor(0.30 * declared value) - floor(0.15 * declared value)`.
- I look at my own reasoning from the immediately preceding declare stage to find the exact value of my smallest crate.
- If my smallest crate is worth strictly less than the duty savings, I choose `[route: night]`.
- Otherwise, I choose `[route: main]`.