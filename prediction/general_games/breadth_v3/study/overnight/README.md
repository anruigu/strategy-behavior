# Inputs for a separate overnight learner run

Each arm has 288 episode labels; the depth and breadth arms share 96 episodes.
`*-episodes.jsonl` contains individual binary/continuous labels; `*-pooled.jsonl`
contains all-label means/counts for identical complete visible inputs. All rows
are training data. Mechanics summaries are predictor context; hidden native
state and holdout outcomes are not included.

Choose a model and compute budget before starting an additional training job.
These exports do not launch GPU training. Use family-held-out validation within
the training pool. Keep all identical visible inputs together, and use
count-aware losses for pooled means. Do not treat a fractional win mean as a
hard classification category. Match training compute as well as label budgets
when comparing neural learners.

The six holdout families are reserved for the primary study. If their outcomes
have been inspected, a newly tuned learner needs an untouched evaluation set
for a prospective claim, or a clearly labeled retrospective evaluation here.
