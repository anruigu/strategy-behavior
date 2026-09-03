---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 1927
---
# Playbook: Harbor Customs

## Declaration

Declare exactly the value of my heaviest crate. No more, no less.

- Declaring above my heaviest: I pay extra duty for nothing. The declared number does not add to my score; it only feeds the duty formula.
- Declaring below my heaviest: the flag fires. I get −40 and my duty is recomputed at 0.30 × my true total. Catastrophic.
- Declaring exactly my heaviest: safe (the flag triggers only on strictly less than), and minimises duty.

There is no strategic reason to deviate. My score depends only on my own crates, my declaration, and my route. Other players' scores are irrelevant to my optimal move.

## Route

Use the formula mechanically. Do not second-guess it.

Let H = my heaviest crate, s = my smallest crate.

- Main score = (sum of all three) − floor(0.30 × H)
- Night score = (sum of all three − s) − floor(0.15 × H)

The difference (main − night) = s − [floor(0.30×H) − floor(0.15×H)].

**Decision rule:** Compute D = floor(0.30×H) − floor(0.15×H). If D > s, go night. Otherwise go main.

In practice, D tends to land in the 3–12 range while s tends to be 8–20, so main wins the vast majority of the time. Night only wins when my hold is extremely skewed (a smallest crate of 3 or 4 next to a large heaviest crate).

**Do not override the formula with intuition.** Write down D and s, compare them, pick the route. No narrative reasoning allowed.

## Standing warning

In a previous game I chose night in a round where D was 4 and s was 18, losing 14 points for no reason. The formula is the decision. If you catch yourself narrating a reason to pick night when D < s, stop. Pick main.

## Quick reference at the table

1. Read my three crate values. Identify H (heaviest) and s (smallest).
2. Declare H.
3. Compute D = floor(0.30 × H) − floor(0.15 × H).
4. If D > s → night. Otherwise → main.
5. Ignore the standings column. Ignore what others declared. Ignore my rank.