# Exploit atlas trace viewer

Read-only viewer for the completed Gemini 49-hole audit and subsequent small-model replications. Defaults to the original Gemini run; matched low-reasoning Gemini and other models remain separately labeled.

The **v3-MA · four-model cross-play** run adds all 768 scheduled MA episodes: 761 complete and seven incomplete. Open a repeated pledge-betrayal example at [the MA trace view](http://localhost:42327/#run=v3-ma-four-model&phase=nerfed&episode=bfdebd98829842f01d4d). Focal/opponent filters cover all four models, and the condition buttons switch between ordinary and nerfed opponents. Each episode links directly to its same-lineup, same-seed counterpart where one exists. Commons have an ordinary condition only.

Every MA round chart cell and action card identifies its seat, model, and ordinary/nerfed role; action cards also show the actual provider model identifier from the recorded call. The round chart shows submitted actions and referee-computed cumulative scores. Marked rounds link to the exact resolving stage and supporting actions/facts. Green denotes an observed exploit pattern, amber a candidate action, and purple the more limited code-pattern or message-association evidence. The saved `report.json` supplies the original study's markers; the viewer does not reclassify traces or claim that an association establishes intent or causality. Incomplete traces retain every saved submission and rejected response, with unscored outcomes rather than invented scores or absent-exploit labels.

MA data comes directly from `benchmark/results/v3-ma-four-model-20260909/`; no experiment files are modified. `ma.py` adapts that schema without importing or changing the original frozen single-agent evaluator. Single-agent action cards now also explicitly show the generating model.

Browse game editions and three seed rollouts, filter episodes with/without executions, inspect the task and scoring, jump to engine-annotated turns, and compare hinted episodes with their same-seed blind runs. The model's exact observation, stated reasoning, submitted action text, referee feedback, evidence facts, and optional full referee state are accessible. Hidden referee state is clearly distinguished from the model observation. No model calls are made by this server.

The annotation functions are imported from the frozen original Gemini source. All 159 original traces have been checked against their saved episode scores and first-execution turns. Attempt labels are action-pattern detections, not proof of intention. Positive paired effects are episode-level metrics and do not establish counterfactual winning. The 11 excluded policy-dependent mechanisms do not receive exploit badges. Incidental engine-side hits on hinted episodes are labeled separately from the designated target.

Current service: loopback port **42327**. Forward that port and open `http://localhost:42327`. Process metadata/logs: `benchmark/results/trace-viewer/server.json` and `server.log`.

Start or restart explicitly:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/shared/allie/home/.codex/tmp \
  /shared/allie/venvs/hole/bin/python -B benchmark/trace_viewer/server.py --port 42327
```

Use `--port 0` to let the OS allocate a free port. The chosen port is saved to the metadata file. Only static viewer files and the two explicit data API routes are served; arbitrary filesystem paths and API credentials are not exposed. Click **Refresh results** to load newly completed episodes. Episode selections are included in shareable URL fragments.

Validation passed: all 159 Gemini episode annotations agree with frozen saved scores; path traversal is rejected; headless Chromium exercised model selection, hinted/unaided switching, exploit-only filtering, same-seed navigation and mobile sizing with no JavaScript errors. Screenshots are saved beside the server metadata. Browser testing tools, dependencies, font cache and temporary profiles are stored under `/shared/allie`.

MA validation: `test_ma.py` checks every saved submission's model and seat attribution, all round marker counts, final scores, and failed-episode handling against the frozen traces. `browser_check_ma.py` exercises the live charts, marked-round navigation, matched-condition links, model filters, all seven failures, mobile sizing, and existing single-agent navigation. Browser screenshots and `ma-browser-check.json` are saved in `benchmark/results/trace-viewer/`.
