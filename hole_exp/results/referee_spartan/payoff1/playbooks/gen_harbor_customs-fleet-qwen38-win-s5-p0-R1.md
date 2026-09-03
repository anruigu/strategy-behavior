---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 2045
---
# Playbook: Harbor Customs

**Declaration rule — always declare exactly your heaviest crate's value.** This is the minimum value that avoids the spot-check flag, and it minimizes the duty you pay. Declaring above your heaviest crate buys you nothing; you simply hand the harbor extra points as duty. Declaring below your heaviest crate gets you flagged, which costs you -40 and recomputes duty on your true total — a double punishment. There is no strategic reason to deviate from "declare = heaviest crate" in any round, any position, any round number.

**Route rule — default to main.** Compute: if your smallest crate is less than roughly 15% of your heaviest crate, night may be marginally better (you save on duty and you're "giving up" a crate that was worth little anyway). In practice this almost never triggers given the 5–40 range. When in doubt, main. The duty difference between routes is small (15% of a 30–40 value is 5–6 points) and you keep all three crates on main.

**Do not try to "match a trend" or "close a gap" by inflating your declaration.** I did this repeatedly — declaring 120 when my heaviest crate was 25 or 30 — and it just paid the harbor extra duty with zero upside. My score is driven by my actual crate values minus duty. The only lever I control is minimizing duty, which means minimizing my declaration.

**Do not declare below your heaviest crate to "save" on duty.** The flag penalty (-40) plus the recomputed duty at 30% of true total will always cost far more than the duty savings you'd have gained. This is a strict dominated strategy.

**Position is irrelevant to my declaration.** Whether I'm leading or last, my optimal declaration is the same: my heaviest crate. I cannot affect others' scores, and my own score only depends on my crates, my duty, and my penalty.

**Summary of the single decision each round:**
1. Look at my three crate values.
2. Declare the largest one.
3. Choose main route (unless smallest < ~0.15 × largest, in which case consider night).
4. Done. No further reasoning needed.