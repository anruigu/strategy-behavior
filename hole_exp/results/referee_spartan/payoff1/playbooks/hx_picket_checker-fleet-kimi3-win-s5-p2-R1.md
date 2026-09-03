---
game: hx_picket_checker
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 3060
---
- Before my first move I map the whole incentive structure: scoring from shooting (+4 hit, -1 to target), escort pairs (+5 each), and Harbor jettison (+3 to attacker, -3 Harbor, landed or not). I rank which lever dominates; escorts at +5 with no downside are the biggest reliable gain, so I treat securing an escort pact as job one.
- On every escort stage I name a boat I have a mutual arrangement with. Naming none every round forfeits up to 5 points per round — that passivity is exactly what left me at +2 while the leader ran away with it. Never answer [salvage: none] again unless every other boat is clearly defecting against me.
- To set up the pact, I use my station note early (round 1) to propose an explicit pairing: name the boat, state I will name them every round if they name me. Notes are the only communication channel, so "steady on station" is wasted bandwidth — I stop sending empty notes.
- When another boat signals an escort offer or actually names me, I reciprocate immediately and keep reciprocating while they do. If they name me once and I respond none, I burned the alliance; I always return a received escort the very next round at latest.
- When weighing whether to fire on Harbor for the +3, I check the retaliation threat and the board state. If I'm behind and need swing points late, I take the jettison shot despite the threat; if I'm secure, I don't provoke. I never fire on Harbor early while its threat to remove me is credible and I still have rounds to earn from.
- Standing orders are cheap to follow and breaking them buys little unless targeting a specific hider, so I default to the ordered target but spend my real thinking on the fire cell, not the target.
- For hiding, I track which cells each shooter has fired at and which cells each target has hidden in. I hide in cells my assigned shooter has not yet fired on, avoiding their apparent favorites, and I never reuse a cell the shooter just hit or narrowly missed.
- For firing, I exploit patterns: if my target reuses cells or cycles, I fire on their most recent or modal cell. If they appear random, I spread shots across mid-range cells rather than repeating 9 or 1 every round; pure repetition leaks information and never adapts.
- When the office tells me my shot result, I always file the true claim. The rules force it to match, and false claims risk contradiction for zero demonstrated gain; lying is not a lever here.
- Each round before deciding I re-read the running hit log the game hands me and update a simple per-boat ledger of hide cells, fire cells, and escort behavior; decisions come from that ledger, not fresh guesses.
- Late in the game I compare my score to the leader's: if catch-up requires it, I shift to aggressive plays (Harbor jettison shots, firing on the leader's likely cell even off-order if permitted) rather than continuing low-yield routine fire that only preserves a loss.
- I keep every reply in the exact bracketed token format with at most one short line of reasoning, so no response is ever wasted on validation errors.