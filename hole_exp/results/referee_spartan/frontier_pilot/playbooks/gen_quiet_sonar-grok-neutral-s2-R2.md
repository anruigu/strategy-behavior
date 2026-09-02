---
game: gen_quiet_sonar
model: grok
condition: neutral
seed: 2
round: 2
chars: 993
---
When hide is put to me I never open on 5 or 7; I pick 1, 2, 3, 4 or 9.
When later hides are put to me I stay off every cell that appeared in the most recent fire tuple, especially the last number (Harbor’s shot at me) and the 5/6/7/8 cluster that keeps repeating.
I do not reuse a hide that just sat inside a fired cluster.
Harbor’s first shot at me is 7; after that Harbor (and the others) cycle 5, 8, 5, 6, so from round 2 onward I hide only on 1, 3, 4 or 9 and I never sit on 5, 6, 7 or 8.
When fire is put to me I never lock onto 5 every round and I never fire the same cell twice.
After a miss I strike that cell off Foxtrot’s remaining set and I shoot a different unused cell from the order 2, 3, 4, 6, 8, 9, 1, 7; I advance one step of that list each fire stage and I do not restart at 2.
Repeating the same mid-board shot after it already missed is what I stop doing.
When claim is put to me I output exactly the private result the referee just gave me; I never invent a hit or a miss.