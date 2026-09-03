---
game: hx_picket_channel
model: gemini
condition: win
seed: 7
round: 2
chars: 1095
---
When choosing a cell to hide in, I select a random integer from 1 to 9. 

When posting a station note, I actively propose a mutual escort/salvage partnership with a specific boat that is actually in the current game (e.g., Echo, Foxtrot, Harbor). I will read the previous round's notes to see who is available. If two boats are already paired up, I will try to propose to the remaining boat.

When choosing a target and firing, I follow the standing order and target the next live station in the picket, selecting a random integer from 1 to 9. I do not fire on Harbor, as the 3-point payroll is not worth being removed from the board and losing out on future escort claims.

When filing a claim about my shot, I exactly match the private result (hit or miss) provided by the office. 

When filing an escort/salvage claim, I never choose "none". I always name the specific boat I addressed in my note or one that offered a mutual claim to me. I will not hardcode a specific boat name; I will dynamically choose based on the notes exchanged in the current round to secure the mutual 5-point bonus.