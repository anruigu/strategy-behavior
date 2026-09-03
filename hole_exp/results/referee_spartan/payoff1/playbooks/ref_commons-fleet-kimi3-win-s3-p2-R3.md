---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 2772
---
- When the stock is near full and others' past catches are unknown, I take slightly above my sustainable share (roughly 15–30% above) rather than exactly at it — exact shares leave fish on the table for greedier rivals. But I do not under-shoot even this: 13.5 while rivals took 19–22 was a season-1 loss I never recovered.
- Once I observe rivals fishing clearly above their shares, I stop assuming my restraint alone can save the stock. Crucially, I escalate to *matching* the greedy rivals roughly one-for-one, not "a lighter version" of them — taking 14 while they took 15–18 still let them out-earn me as the fishery collapsed. In a scramble, equal shares of a doomed stock beat noble under-takes.
- The right escalated catch is a competitive split of what's left: if rivals will jointly take R this season from stock S, I take at least (S − RExpected)/1 share terms — i.e., aim for my third of the current stock each season once cooperation is dead, since that is my fair split whether or not the stock survives.
- Restraint only pays if others are also restrained. I check each season: is total observed take near the sustainable total? If yes, stay close to share; if no, my restraint just donates fish to them.
- When a rival makes a clearly excessive catch, I revise their future take upward permanently and plan the rest of my seasons assuming a declining stock — and I act on that *this* season, not next, because each season of half-escalation is catch I never get back.
- Each season I compute the regrowth: total take above roughly one-third of the current stock shrinks the fishery. I project next season's stock using rivals' *observed* recent takes (not their sustainable shares) plus mine before submitting.
- As the stock falls below ~30–40% of max with greedy rivals, I treat the game as a pure scramble immediately: take roughly my third of the remaining stock each season rather than anything tied to the (now tiny) sustainable share. With stock at 32, taking 12 when my third was ~10.6 was about right, but I should have reached this mode a season earlier.
- I watch the terminal math: if projected total take this season exceeds the stock, the fishery dies regardless — then I grab my full competitive share of what remains with no discount for stock survival.
- In the final season, with no regrowth to protect, there is no reason to hold back: I take as much as can still be landed — essentially the remaining stock minus what rivals will first claim, aiming for my full third or more.
- Score benchmark check: against greedy rivals on a 6-season game, ~50–60 total is realistic; landing 38 confirmed that matching at 60–70% of greedy takes is still too passive — full competitive matching from the first sign of greed is the correct escalation.