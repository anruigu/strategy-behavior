---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2185
---
My playbook for **gen_harbor_customs**:

- My declared number only affects my duty and my penalty risk; it never increases what I keep. So every point I declare above the minimum safe value is pure loss. I always declare exactly the value of my heaviest crate — never the full total, never anything above the heaviest. Declaring my true hold total was my biggest leak; that mistake cost me duty every time I did it.

- Never declare below my heaviest crate, no matter what. The −40 penalty plus restructured duty dwarfs any conceivable duty saving.

- The standing spot check never changes (always the heaviest crate), so there is no bluffing value in varying my declaration and no reason to copy or react to other players' declarations. Other seats' scores don't touch mine; I play my own hold only and ignore standings talk.

- At the route stage I still know my hold — it was shown to me that round and nothing takes it away. I must never say "I don't have the details" or "default to main for safety." I look up my actual smallest crate value from the round's hold and do the arithmetic. Let h = my declared (heaviest) value and s = my smallest crate. Night beats main exactly when losing s costs less than the duty saved: I take night only when s < 0.15 × h (roughly when my smallest crate is under 15% of my declared value). Otherwise I take main. A "steadier option" instinct that skips this calculation is a mistake.

- Sanity check before submitting: score for main = total − floor(0.3·d); score for night = total − s − floor(0.15·d). I compute both numbers explicitly with my real crates and pick the larger; ties go to main only because it avoids the confiscation bookkeeping, not because it is safer.

- When the hold is lopsided (one huge crate, tiny smallest), night is often clearly correct even though it feels risky. When the hold is balanced, main almost always wins on the math despite the higher duty rate — trust the formula over the feeling.

- I never vary strategy by round number or by who is "ahead." There is no interaction, no endgame bonus, and no penalty for leading. Every round, same two calculations: declare = heaviest; route = whichever formula wins.