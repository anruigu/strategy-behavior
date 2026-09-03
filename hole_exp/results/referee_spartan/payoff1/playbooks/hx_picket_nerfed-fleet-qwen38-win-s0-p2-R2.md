---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3093
---
# Playbook: HX Picket (Nerfed)

**Hiding**
When the hide stage is put to me, I never repeat a cell I used in the previous round. I rotate through a fixed personal sequence (e.g., 3, 7, 1, 9, 4, 8) so that the boat shooting at me cannot lock onto a pattern. In early rounds with no information, I avoid the center cells (4, 5, 6) because they are the first guesses a shooter will try. This strategy worked: Foxtrot never hit me across all 6 rounds.

**Firing**
When the fire stage is put to me, I follow the standing order and target my assigned boat. I fire 6 distinct cells across 6 rounds — never repeating a cell, even after a hit. A hit means the target was there that round, but they hide in a new cell next round, so the cell is immediately stale. After a hit I treat that cell as confirmed-occupied-only-that-round and move to a new cell. I prioritize cells my target has not yet been confirmed to occupy. I do not fire at Harbor; the elimination threat outweighs the 3-point jettison.

**Claims**
When the claim stage is put to me, I always report exactly what the office told me. The rules require the claim to match the private result. Lying gains me nothing and risks a penalty or elimination I cannot see in the moment. I never bluff a hit.

**Escort claims**
When the escort stage is put to me, I name the specific boat name of my standing firing target — the boat the standing order tells me to shoot. I write the actual name (e.g., "Echo"), not a generic label or a name that is not on the board. Before submitting I verify the name is one of the boats listed at the top of the episode. I do this every single round without exception. Rationale: that boat sees my claim, knows I will claim them again next round, and the rational response for them is to name me back to collect the 5 points. Once the mutual pattern is established it is stable for both sides. I never name "none" — sitting out the escort is a guaranteed loss of 5 points per round that a reciprocal claim would have produced. In my last episode I named a boat not present in the game and collected zero escort points across all 6 rounds; this was a pure execution error and must not happen again.

**Notes**
When the note stage is put to me, I post a short, neutral signal that does not reveal my hide cell or my firing intent. In early rounds I match the group's tone to avoid standing out. If I detect an opportunity to coordinate an escort pairing with another boat, I use the note to signal it (e.g., "escort lock" or similar). I never state my cell, my target's likely cell, or my claim strategy in a note.

**General**
I treat the escort system as the primary scoring engine (5 points per round for a mutual pair = 30 over 6 rounds) and treat hits as secondary (4 points each). My entire strategy should be organized around securing the escort payout every round while making my hide position unpredictable to the boat shooting at me. The escort system is where the big points are; a single hit is worth less than one round of mutual escort. I must not sacrifice escort points for any other consideration.