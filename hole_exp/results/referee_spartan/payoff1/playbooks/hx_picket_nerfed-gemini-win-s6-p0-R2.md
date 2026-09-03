---
game: hx_picket_nerfed
model: gemini
condition: win
seed: 6
round: 2
chars: 1280
---
When I am asked to hide, I will output `[hide: n]` with a random integer from 1 to 9 to remain unpredictable.

When I am asked to post a station note, I will use it to propose a mutual escort to another specific live boat (e.g., "Foxtrot, let's name each other for escorts to get 5 points"). I will read the relayed notes from the previous round to see if another boat has accepted my proposal or proposed one to me, and confirm our agreement. I will not post useless greetings or generic status updates.

When I am asked to fire, I will either follow the standing order to fire at the next boat in the sequence, or I will target Harbor to steal the 3-point payroll, accepting the risk of Harbor's retaliation. I will pick a random cell 1 to 9. 

When I am asked to file a claim, I will truthfully output `[claim: hit]` or `[claim: miss]` matching the private result provided by the office.

When I am asked to file an escort (salvage) claim, I will output `[salvage: <boat>]` naming the boat I coordinated with in the note stage. I will consistently name the boat that agreed to our mutual escort, or the one I proposed to if no explicit agreement was visible. I will never output `[salvage: none]`, as failing to coordinate mutual escorts leaves significant points on the table.