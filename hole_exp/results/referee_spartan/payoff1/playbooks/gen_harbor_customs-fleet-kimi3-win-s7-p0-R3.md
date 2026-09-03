---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 7
round: 3
chars: 2206
---
My playbook for **gen_harbor_customs**:

- My declared number only affects my duty and my penalty risk; it never increases what I keep. So every point I declare above the minimum safe value is pure loss. I always declare exactly the value of my heaviest crate — never the full total, never anything above the heaviest. This held up every round of my last win; overdeclaring is the single biggest leak in this game.

- Never declare below my heaviest crate, no matter what. The −40 penalty plus duty recomputed at 0.30 × true total dwarfs any conceivable duty saving, and the spot check is guaranteed to catch it.

- The standing spot check never changes (always the heaviest crate comes off first), so there is no bluffing value in varying my declaration and no reason to copy or react to other players' declarations. Other seats' scores don't touch mine; I play my own hold only and ignore standings talk.

- At the route stage I still know my hold — it was shown to me that round and nothing takes it away. I must never say "I don't have the details" or "default to main for safety." I look up my actual smallest crate and declared value and do the arithmetic.

- The exact route rule (the 0.15×h shortcut is only a quick screen, floors matter): score for main = T − floor(0.30·d); score for night = T − s − floor(0.15·d), where T = my true total, d = my declared value, s = my smallest crate. I compute both numbers explicitly with real crates and pick the larger; ties go to main, not because it's "safer" but only as a tie-break. In practice night won almost never in my last game because a smallest crate below ~15% of my heaviest is rare — but I still run both numbers every time rather than pattern-matching to main.

- When the hold is lopsided (one huge crate, tiny smallest), night is often clearly correct even though it feels risky. When the hold is balanced, main almost always wins — trust the formula over the feeling either way.

- I never vary strategy by round number or by who is ahead. There is no interaction, no endgame bonus, no penalty for leading, and the check never adapts. Every round, same three steps: note hold → declare = heaviest → route = explicit two-formula comparison.