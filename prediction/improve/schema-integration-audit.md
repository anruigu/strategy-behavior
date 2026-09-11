The current post-training driver is compatible with the artifact schemas written by the numerical and transformer workers. A synthetic integration test passed on 2026-09-10 in 7.9 seconds. No empirical fitting, scoring, model loading, API calls, or job submissions were performed.

[test_schema_integration.py](test_schema_integration.py) exercises the actual baseline artifact writers with their optimizer mocked, the transformer head/artifact/forecast/completion writers, and the original prompted-forecast join writer. Their outputs pass `Work.audit_training`, `Work.score_development`, and `Work.apply_gate` without schema adapters. It covers:

- Ten list-form folds, twenty transformer fits, and twenty-four fresh numerical export sidecars.
- Completion hash maps; nested transformer forecast contracts and their checkpoint input hashes; baseline forecast sidecars; scalar source/output hashes in the original Kimi join manifest.
- All twenty-two development forecast paths, nine numerical candidates across retrospective folds, and development-only Kimi coverage.
- All twelve gate contrasts with the scorer's exact interval fields and baseline-minus-method direction. Equal synthetic probabilities produce an inconclusive decision permitting the fixed fresh cohort.
- Scoring and gate resume without recomputation, plus rejection after a saved head's bytes change. Existing driver tests separately exercise remote-to-local evidence-path mapping.

One conditional limitation remains: `train_job --resume` can reuse completed fits from an earlier Fleet job, preserving their original job IDs. `Work.audit_training` currently requires every fit's ID to match the selected job. A future retry after partial training would therefore fail closed unless the driver accepts explicitly verified prior-job lineage. The current SciPy failure occurred before fitting, so this does not block the selected retry.

Reproduce the synthetic integration check from the project root:

```bash
PYTHONPATH=/shared/allie/strategy-behavior/prediction/vendor OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR=/shared/allie/home/.codex/tmp /shared/allie/venvs/hole/bin/python -B -m unittest prediction.improve.test_schema_integration -v
```

This checks artifact interoperability, not Fleet dependency installation or successful GPU optimization. Runtime completion remains the remote worker's responsibility.
