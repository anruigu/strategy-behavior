---
game: hf_commons_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 1142
---
When I see a posted agreement or notice promising retaliation against overfishers, I take the sustainable share (round to the game’s required precision) every season unless the stock is already collapsed.  
When the sustainable share is clearly calculable, I take that amount each season to maximize long-run total and keep the stock stable.  
When the game is finite and final seasons approach, I still take the sustainable share unless other players have already driven the stock to zero.  
When other boats’ previous-season catches are revealed and they matched the agreement, I continue to match the agreement.  
When other boats’ previous-season catches reveal clear overfishing and the stock is declining, I switch to best-response: increase my catch only if that yields a higher guaranteed final score given imminent collapse; otherwise keep the sustainable share.  
When the stock reaches zero, I take 0 thereafter (do not attempt to catch from an exhausted stock).  
Do not attempt escalation (take more than the sustainable share) purely to experiment when cooperation is holding — that did not improve my score in cooperative runs.