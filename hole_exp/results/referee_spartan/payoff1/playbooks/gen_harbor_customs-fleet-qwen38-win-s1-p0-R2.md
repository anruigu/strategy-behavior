---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 1923
---
# Playbook: Harbor Customs

**Declaration: always declare exactly your heaviest crate's value.**

The dockhand lifts your heaviest crate and flags you if your declaration is below it. There is no strategic reason to declare anything else. Higher costs more duty for zero benefit. Lower triggers a -40 penalty plus duty recomputed at the full hold total at 30%, which is always catastrophic.

Do not be swayed by other players' declaration patterns, round trends, or any instinct to "look honest" by declaring your full total. The check is private and mechanical. The only number that matters is your heaviest crate.

**Route: compare your smallest crate to 15% of your declared value (which equals your heaviest crate).**

- If smallest < 0.15 × heaviest → take **night**.
- If smallest ≥ 0.15 × heaviest → take **main**.

The floor function means the boundary can be off by 1 point, so when the comparison is tight (within ~1), compute both scores explicitly:
- Main score = (c1 + c2 + c3) − floor(0.30 × heaviest)
- Night score = (c1 + c2 + c3 − smallest) − floor(0.15 × heaviest)

Pick the larger.

**Practical note:** In practice the smallest crate will almost always be well above 15% of the heaviest (e.g., smallest 10–14 vs. threshold ~5–6), so main will be the correct route most of the time. Night becomes the right call only when you hold a genuinely tiny crate (1–5) alongside a large heaviest crate. When in doubt and the margin is thin, just do the arithmetic.

**What to avoid:**

- Do not default to main without checking. If you hold a crate worth 3 and your heaviest is 40, night saves you far more in duty than the 3 you forfeit.
- Do not default to night "to save duty" without checking. If your smallest is 20 and your heaviest is 38, you'd be giving up 20 to save ~5 in duty.
- Do not let the other seats' scores or declarations enter your calculation. The harbormaster's check is independent per seat.