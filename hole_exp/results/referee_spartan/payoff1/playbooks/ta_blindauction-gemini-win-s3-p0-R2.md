---
game: ta_blindauction
model: gemini
condition: win
seed: 3
round: 2
chars: 1250
---
When an opponent sends a private note proposing to divide the lots, I evaluate the split and, if it is mutually beneficial, I reply with an explicit agreement.
Before formulating my bid, I will explicitly review the private notes sent and received in the history to verify if there is an active agreement for the current lot. I will not assume there is no agreement without carefully checking the prior turns.
When I agree to a bidding pact where I promise to bid nothing on specific lots, I actually submit `[bid: 0]` on those lots. I do not agree to bid 0 and then submit a competitive bid, as this breaks trust and ruins the strategy.
When it is my turn to win a lot under an agreed division (where the opponent promised to bid 0), I submit `[bid: 1]` to win the lot for the lowest possible cost while avoiding a 0-0 tie.
When the published auction results reveal that the opponent bid on a lot they promised to concede, I immediately treat the agreement as void.
When there is no active or trusted agreement, I bid strictly less than my value for the lot to ensure a profit. 
When I am unsure of the format, I remember this is a first-price auction where I pay exactly what I bid; I never bid my exact value or guess about second-price mechanics.