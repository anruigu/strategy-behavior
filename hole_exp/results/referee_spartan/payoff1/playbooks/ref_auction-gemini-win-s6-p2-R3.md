---
game: ref_auction
model: gemini
condition: win
seed: 6
round: 3
chars: 1301
---
I read my starting budget carefully from the very first prompt of the game. It is ONLY stated in the first message, so I must look back at the first message in the conversation history to retrieve this exact number (e.g., 30, not 100) and carry it forward through all subsequent lots. I will NEVER assume a default starting budget like 100; I must physically check the first prompt every single time I calculate my budget.

I calculate my remaining budget by taking my true starting budget (from the very first prompt) and subtracting the exact winning prices of any lots I have won, which are shown in the "Results so far" section. I do not subtract bids I have placed that did not result in a win.

I never place a bid that exceeds my actual remaining budget, regardless of how much I value the lot. 

When deciding whether to bid, I ensure that the standing high bid plus the minimum raise is less than my valuation for the lot and less than or equal to my remaining budget. 

If the required bid to win exceeds either my valuation or my remaining budget, I pass. 

When I reply, I accurately report my remaining budget calculated from my true starting amount minus my actual wins, not an assumed number. I will explicitly state my true starting budget in my reasoning to ensure I do not forget it.