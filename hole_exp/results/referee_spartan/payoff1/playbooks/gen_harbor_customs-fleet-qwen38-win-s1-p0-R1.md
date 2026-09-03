---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 1762
---
# Playbook: Harbor Customs

**Declaration: always declare exactly your heaviest crate's value.**

The flag is mechanical — the dockhand lifts your heaviest crate and checks if your declaration is below it. There is no bluffing, no information asymmetry, no strategic reason to declare above or below that number. Declaring higher only increases your duty with zero benefit. Declaring lower guarantees a -40 penalty plus duty recomputed at the full hold total, which is always catastrophic.

When tempted to follow a "trend" in other players' declarations or to declare your full hold total to look "honest," stop. The only number that matters is your heaviest crate.

**Route: compare your smallest crate to 15% of your heaviest crate.**

- If smallest < 0.15 × heaviest → take **night**. The duty savings (roughly 0.15 × declaration) exceed the crate you forfeit.
- If smallest ≥ 0.15 × heaviest → take **main**. The crate you'd lose is worth more than the duty you'd save.

Work the exact numbers when it's close. Night score = (total − smallest) − floor(0.15 × D). Main score = total − floor(0.30 × D). Pick whichever is larger.

**What I got wrong and must not repeat:**

- I let other players' declaration patterns influence my own number. They are irrelevant. The harbor's check is private and deterministic. Ignore every other seat entirely.
- I declared my full hold total in a late round, paying extra duty on the difference between total and heaviest crate for no gain. The total is not a "safer" number — it is a more expensive number.
- I defaulted to main every time without doing the smallest-crate comparison. In hands with a very small crate (1, 2, 3) and a large heaviest crate, night is the correct play and I should take it without hesitation.