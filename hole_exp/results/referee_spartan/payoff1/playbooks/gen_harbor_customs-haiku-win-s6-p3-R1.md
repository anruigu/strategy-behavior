---
game: gen_harbor_customs
model: haiku
condition: win
seed: 6
round: 1
chars: 1704
---
# Harbor Customs Playbook

**On the declare stage:**

When I see my three crates, I immediately identify my heaviest crate. I declare at least that value to avoid the spot check penalty, which costs -40 points and recomputes my duty at 0.30x. The penalty is catastrophic enough that safety is mandatory.

When choosing my actual declaration above the minimum, I calculate both route options:
- Main route: score = true total - floor(0.30 × declared)
- Night route: score = (true total - smallest crate) - floor(0.15 × declared)

I pick whichever route gives the higher score, then declare the value that maximizes it.

When I'm significantly ahead late in the game, I do not play conservatively just because I'm winning. I still optimize for actual points, not for "safety margins." My final round showed I left points on the table by declaring too low when I had strong crates.

**On the route stage:**

I commit to my route choice during the declare stage calculation, not during the route stage. By the time route is presented, I already know which one is better for my declared value.

I do not second-guess based on psychology or patterns. The math is what matters. Every time I've chosen "main route" because it "feels safer" or "is more predictable," I should have been optimizing the arithmetic instead.

**General discipline:**

I track that other players seem to cluster in the 45-72 declaration range. This is useful context but not a decision rule. My declaration is driven by my crates and the spot check floor, not by what others might do.

I notice I often default to main route reflexively. This is a leak. Force yourself to calculate night route every time, even when main feels "right."