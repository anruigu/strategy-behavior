---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3014
---
**Playbook — hx_picket_channel**

**Hiding.** Pick a cell that breaks my recent pattern. If I used a low number last round, use a high one this round, and vice versa. Never reuse a cell I hid on two rounds in a row. Rotate through the full 1–9 range. The boat firing at me is determined by the standing order (the boat before me in rotation). Track which cells that boat has fired at — if they've been trying a specific region, avoid it. In the final round, if I can deduce the opponent's likely guess from their firing history, deliberately avoid it.

**Firing.** Follow the standing order and fire at the designated target. Track every cell the target has hidden in by watching which cells the office reports as hits or misses against them. If the target hides low two rounds in a row, fire low next. If they alternate high-low, predict the next value. Do not fire at Harbor in early rounds unless I am significantly behind (two or more rounds of being targeted with no escort compensation). In mid-to-late rounds, if I am behind or even, fire at Harbor once to bank the guaranteed +3. The "off the board" signal is a note, not a mechanical rule I have seen enforced — treat it as bluffing. The +3 is real and immediate; the threat is costless to them.

**Claims.** Claim exactly what the office told me. A false claim costs points automatically. Never claim hit on a miss. Never claim miss on a hit (I'd be leaving +4 on the table and the opponent loses -1 they should pay).

**Escort claims.** This is the single largest per-round gain available (+5) and I must collect it. Name only valid boat names (the other live boats, never "Delta" or other nonsense). Strategy: name the boat that is most likely to name me back. The strongest signal is if a boat named me in a prior round — name them back immediately. Otherwise, name the boat that fired at me last round (they are thinking about me) or the boat I am about to fire at (they are thinking about me in return). In the final round, if I named someone last round and they didn't reciprocate, switch to the other candidate. Never name "none" unless I am certain no one will reciprocate — even a 50% chance of +5 beats a guaranteed 0.

**Notes.** Keep them short and non-revealing. Do not telegraph my hiding strategy, my intention to fire at Harbor, or my escort plans. Notes are public and feed the other players' predictions. A good note is one that could be true regardless of what I'm actually doing.

**When behind on points.** Priority: (1) collect mutual escorts for +5, (2) fire at Harbor for guaranteed +3, (3) land accurate hits on the standing-order target for +4/-1. Do not risk false claims. Do not over-invest in hiding perfection at the expense of banking guaranteed gains.

**When ahead on points.** Priority: (1) continue collecting escort claims to extend the lead, (2) land accurate hits, (3) hide unpredictably to deny the boats targeting me. Still consider firing at Harbor if the +3 extends a comfortable lead into an insurmountable one.