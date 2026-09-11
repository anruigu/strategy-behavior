# Behavioral dataset viewer

Open **[localhost:42329](http://localhost:42329)**. The bound port and process are recorded in `state/server.json`.

The **[fixed-budget breadth check](http://localhost:42329/general/breadth)** shows 18 study families, including six entirely held-out families, and all 624 fresh episodes. Compare 288-label depth/breadth cohorts (96 episodes are shared), inspect actual games and exact actor prompts, and switch among win, invalidity and native-score prediction results. It includes pooled 4/8/16-shot controls, family-level intervals, repeated-label variation, descriptive interface/calibration findings, and audited costs. These cohorts are separate from the earlier general-game releases.

The **[replicated general-game study](http://localhost:42329/general/replicated)** expands the catalog to 16 families / 57 configurations, adding Ultimatum, Two-Thirds Average, Secretary and Memory. It separates 144 historical episodes from 320 fresh training and 272 prospective test episodes. Inspect live collection/forecast progress, repeated-trial variability, parameter responses, operational-label coverage and the 120/248/440-episode learning curves against 4/8/16-shot prompting. Learning results use fixed study cohorts; catalog/cohort filters change the observed distributions. Refresh loads the latest saved checkpoints. Full native snapshots are evaluator views, distinct from exact player messages. The original pilot and Gameable views remain available.

Use the dataset switch to open **[General Games](http://localhost:42329/general)**: 12 native TextArena families, 49 parameter configurations and 196 seeded instances. Its cohort selector separates the balanced 96-episode coverage pilot, the 48-episode parameter sweep, and all 144 collected episodes (779 focal actions). Catalog counts remain separate from observed behavior counts. Configurations without model episodes still expose their native rules and seeded openings.

The **[Validation checks](http://localhost:42329/general#checks)** section reports parameter effects, model differences, audited label reliability, four-shot versus learned prediction, and representation ablations. Select a parameter family, prediction holdout, or target to inspect results. Unsupported targets stay unmeasured. These checks use fixed study cohorts and do not inherit catalog filters. The native sample explorer shows exact model inputs and marks full before/after snapshots as evaluator views that may contain hidden information.

The [pilot assessment panel](http://localhost:42329/#assessment-section) adds
the five research checks, matched-effect plots, label-audit results, and the
family-held-out few-shot/learned-predictor comparison. It appears in the global
overview; selecting one family hides this whole-pilot analysis. Its report and
both figure PDFs can be downloaded directly.

The overview shows the 6,056-instance design, family coverage, parameter distributions, six evaluation splits, and live-model behavior, action frequencies, score distributions, and condition-specific mechanism execution. Click a family bar or use the family dropdown to focus the plots. Parameter histograms count base games once; paired controls are shown separately.

The sample explorer lets you search and filter all game instances, inspect their actual player rules and structured representation, navigate paired interventions, and open live or scripted episodes. Every turn exposes the exact player input, raw response, observable labels, before/after research states, and local counterfactual. Scripted witnesses carry a separate provenance badge and never contribute to the live-behavior plots. Discovery and unsupported behavior labels remain unknown.

The sample URL preserves family, game, episode, tab, and turn. **Export sample** downloads the selected game or trace as JSON. Overview data refreshes every 20 seconds during collection; use Refresh to load current counts manually. The viewer reads saved artifacts and has no inference calls or write API.

**Report ↓** downloads the dataset summary. Footer links download the standalone
design and behavior figures as PDF; PNG/SVG versions are also available in the
pilot's `export/` directory. The pilot is **144/144 complete, with 864 decisions**.
The viewer combines 77 retained FLT episodes with the 67-episode OpenRouter
continuation, with live completion counts and separate
provider labels in plots and trajectory samples. Each episode uses one provider;
the switch followed prior completion, so provider groups are not randomized.

```bash
TMPDIR=/shared/allie/home/.codex/tmp PYTHONDONTWRITEBYTECODE=1 \
  /shared/allie/venvs/hole/bin/python -B \
  prediction/scaleup/viewer/server.py --port 42329
```

Use `--dataset` and `--run` for another compatible build/collection, or `--port 0` for an available port. It binds to loopback. All browser checks, screenshots, logs, and state remain under this directory's `state/` folder.

```bash
/shared/allie/venvs/hole/bin/python -B -m pytest \
  prediction/scaleup/viewer/test_viewer.py -q \
  --basetemp=/shared/allie/home/.codex/tmp/scaleup-viewer-pytest
/shared/allie/venvs/hole/bin/python -B prediction/scaleup/viewer/browser_check.py
```

Serving requires only the Python standard library. The browser check reuses the existing shared Chromium binary and Playwright installation from `prediction/dataset_viewer/.deps`.
