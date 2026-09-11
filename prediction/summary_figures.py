"""Render the fixed primary transfer comparator from saved evaluation scores only."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from .diagnostics import _plotting, _save_figure
from .io_utils import now, write_json

METHOD = "combined_logistic_both"
BASELINE = "pair"
TARGETS = ("action0", "cooperation", "coordination")
TARGET_LABELS = ("Action 0", "Mutual\ncooperation", "Coordination")
RETROSPECTIVE = (
    ("family", "New shapes\nHeld-out family"),
    ("random_group", "New shapes\nRandom groups"),
    ("interpolation", "New shapes\nPayoff interpolation"),
    ("extrapolation", "New shapes\nPayoff extrapolation"),
    ("pair", "Known shapes\nHeld-out pair"),
    ("model", "Known shapes\nHeld-out model"),
)
FUTURE = (
    ("prospective", "New games\nFull numerical", "prospective/evaluation-numerical"),
    ("prospective_pair", "New games\nHeld-out pair", "prospective/evaluation-pair"),
    ("prospective_model", "New games\nHeld-out model", "prospective/evaluation-model"),
    ("prospective_controls", "Known shapes\nPayoff / text controls", "controls/evaluation"),
)


def _safe_output(path):
    path = Path(path).resolve()
    if not path.is_relative_to(Path("/shared/allie")):
        raise ValueError("Figure outputs must remain under /shared/allie")
    return path


def _read_snapshot(path, snapshots):
    path = Path(path).resolve()
    if str(path) not in snapshots:
        raw = path.read_bytes()
        snapshots[str(path)] = {"sha256": hashlib.sha256(raw).hexdigest(), "payload": json.loads(raw)}
    return snapshots[str(path)]["payload"]


def _index(items, fields, name):
    if not isinstance(items, list):
        raise ValueError(f"{name} must be a list")
    result = {}
    for row in items:
        if not isinstance(row, dict) or any(field not in row for field in fields):
            raise ValueError(f"Missing key in {name}: {fields}")
        key = tuple(row[field] for field in fields)
        if key in result:
            raise ValueError(f"Duplicate key in {name}: {key}")
        result[key] = row
    return result


def _finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def extract_cell(summary, split, target):
    """Validate and copy saved all-method common-support results, without rescoring."""
    if summary.get("pair_baseline_context") != "ordered (focal model, opponent model); held-pair splits remain unordered":
        raise ValueError("Source does not declare the required ordered context baseline")
    scores = _index(summary.get("scores"), ("split","target","method"), "scores")
    comparisons = _index(summary.get("comparisons_to_pair"), ("split","target","method","baseline"), "comparisons_to_pair")
    supports = _index(summary.get("support"), ("split","target"), "support")
    if (split,target) not in supports:
        raise ValueError(f"Expected split/target missing from saved support: {split}/{target}")
    support = supports[split,target]
    for method in (METHOD, BASELINE):
        if method not in support.get("all_rows_by_method",{}):
            raise ValueError(f"Required fixed method missing from original evaluation: {method}")
        if (split,target,method) not in scores:
            raise ValueError(f"Required saved score key missing: {split}/{target}/{method}")
    score, baseline = scores[split,target,METHOD], scores[split,target,BASELINE]
    common = support.get("common_rows")
    if type(common) is not int or common < 0:
        raise ValueError("Common-support row count must be a nonnegative integer")
    for field in ("rows","groups","episodes","opportunities"):
        if type(score.get(field)) is not int or score[field] < 0 or score[field] != baseline.get(field):
            raise ValueError("Method and baseline do not share saved evaluation support: "+field)
    if score["rows"] != common:
        raise ValueError("Saved score is not on the original all-method common support")
    cell = {"split":split,"target":target,"method":METHOD,"baseline":BASELINE,
            "groups":score["groups"],"episodes":score["episodes"],"rows":score["rows"],
            "opportunities":score["opportunities"],"saved_method_score":score,
            "saved_baseline_score":baseline,"saved_support":support,
            "all_common_support_methods":sorted(support["all_rows_by_method"])}
    comparison = comparisons.get((split,target,METHOD,BASELINE))
    if not common:
        if comparison is not None:
            raise ValueError("Zero common support cannot have a saved improvement")
        return {**cell,"status":"no_common_support","improvement":None,"interval":None,"interval_label":"CI NA"}
    if comparison is None or comparison.get("positive_means_improvement") is not True:
        raise ValueError("Saved paired comparison is absent or uses an unexpected sign")
    delta = comparison.get("improvement",{}).get("event_brier")
    a,b = baseline.get("event_brier"),score.get("event_brier")
    if not all(_finite(v) for v in (delta,a,b)) or not all(0 <= v <= 1 for v in (a,b)):
        raise ValueError("Brier scores/improvement must be finite and scores in [0,1]")
    if not math.isclose(delta,a-b,rel_tol=1e-9,abs_tol=1e-10):
        raise ValueError("Stored improvement disagrees with the two stored Brier scores")
    interval = comparison.get("intervals",{}).get("event_brier")
    if interval is None or interval.get("lower") is None or interval.get("upper") is None:
        interval_label = "CI NA"
    else:
        lower,upper = interval["lower"],interval["upper"]
        if not _finite(lower) or not _finite(upper) or lower > upper:
            raise ValueError("Saved paired interval is invalid")
        interval_label = "CI > 0" if lower > 0 else "CI < 0" if upper < 0 else "CI spans 0"
    return {**cell,"status":"available","improvement":delta,"interval":interval,
            "interval_label":interval_label,"saved_comparison":comparison}


def build_overview(run_root):
    root = Path(run_root).resolve()
    snapshots, panels = {}, []
    panel_specs = [
        ("pilot","Pilot grouped validation",
         [(split,label,"pilot/evaluation") for split,label in RETROSPECTIVE]),
        ("development","Development grouped validation",
         [(split,label,"development/evaluation") for split,label in RETROSPECTIVE]),
        ("prospective","Prospective frozen forecasts",list(FUTURE)),
    ]
    for name,title,specs in panel_specs:
        rows = []
        for split,label,relative in specs:
            folder = root/relative
            path = folder/"scores.json"
            entry = {"split":split,"label":label,"source_path":str(path),"cells":[]}
            state = "pending"
            if path.exists():
                if name == "prospective":
                    audit_path = folder/"audit.json"
                    if not audit_path.exists():
                        state = "awaiting_audit"
                    else:
                        audit = _read_snapshot(audit_path,snapshots)
                        entry["audit_path"] = str(audit_path)
                        entry["audit_issues"] = audit.get("issues",[])
                        if audit.get("prospective_verified") is not True:
                            state = "unverified"
                        elif audit.get("requested_split") != split or audit.get("effective_split") != split:
                            raise ValueError("Prospective audit has the wrong split: "+str(audit_path))
                        else:
                            state = "available"
                else:
                    state = "available"
            if state == "available":
                summary = _read_snapshot(path,snapshots)
                entry["uncertainty"] = summary.get("uncertainty")
                entry["weighting"] = summary.get("weighting")
                entry["cells"] = [extract_cell(summary,split,target) for target in TARGETS]
            else:
                entry["cells"] = [{"split":split,"target":target,"method":METHOD,"baseline":BASELINE,
                                  "status":state,"improvement":None,"groups":None,
                                  "interval":None,"interval_label":"CI NA"} for target in TARGETS]
            entry["status"] = state
            rows.append(entry)
        panels.append({"name":name,"title":title,"rows":rows})
    return {
        "schema":"primary-transfer-figure-v1","created_utc":now(),"run_root":str(root),
        "method":METHOD,"baseline":BASELINE,"metric":"event_brier",
        "direction":"saved ordered-context baseline Brier minus saved fixed-method Brier; positive is better",
        "targets":list(TARGETS),"panels":panels,
        "input_sha256":{path:snapshot["sha256"] for path,snapshot in snapshots.items()},
        "support_policy":"Original all-method common support from each saved evaluation; no pairwise rescore or winner selection.",
        "group_count":"G counts canonical payoff-shape groups in the saved score; affine controls can have several numerical game variants per G.",
        "interval_indicator":"CI > 0 / CI < 0 / CI spans 0 describes the saved paired 95% percentile interval; CI NA means unavailable.",
        "limitations":[
            "Descriptive intervals are unadjusted for multiple targets/splits and do not refit models.",
            "Known-shape pair/model holdouts do not test generalization to new payoff shapes.",
            "Prospective pair/model tests also use new games; controls reuse source shapes.",
            "Canonical coordinates may be undefined for tied diagonals, reducing interpolation/extrapolation support.",
            "Pending or unverified evaluations are gray; gray NA means zero common support, not zero improvement.",
            "Grouped validation and prospective results may use different method rosters and hence different all-method common support.",
        ],
    }


def _draw_panel(ax, panel, plt, color_limit, compact=False):
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("primary_improvement",["#b73b3b","#fffdf8","#167349"])
    cmap.set_bad("#e5e7eb")
    values = np.full((len(panel["rows"]),len(TARGETS)),np.nan)
    for i,row in enumerate(panel["rows"]):
        for j,cell in enumerate(row["cells"]):
            value = cell["improvement"]
            if value is not None:
                values[i,j] = value
                label = f"{value:+.3f}\nG{cell['groups']} · {cell['interval_label']}"
                color = "white" if abs(value) > color_limit*.68 else "#18212a"
            else:
                label = {"pending":"Pending","awaiting_audit":"Awaiting audit",
                         "unverified":"Unverified","no_common_support":"NA\nG0 · no support"}[cell["status"]]
                color = "#58616b"
            ax.text(j,i,label,ha="center",va="center",fontsize=9 if compact else 12,
                    fontweight="normal",color=color,linespacing=1.6)
    im = ax.imshow(np.ma.masked_invalid(values),vmin=-color_limit,vmax=color_limit,cmap=cmap,aspect="auto")
    ax.set_xticks(range(len(TARGETS)),TARGET_LABELS,fontsize=9 if compact else 12)
    ax.xaxis.tick_top()
    ax.tick_params(axis="both",length=0,pad=8)
    ax.set_yticks(range(len(panel["rows"])),[r["label"] for r in panel["rows"]],fontsize=9 if compact else 11)
    ax.set_xticks(np.arange(-.5,len(TARGETS),1),minor=True)
    ax.set_yticks(np.arange(-.5,len(panel["rows"]),1),minor=True)
    ax.grid(which="minor",color="white",linewidth=2)
    ax.tick_params(which="minor",bottom=False,left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    available = sum(c["status"]=="available" for r in panel["rows"] for c in r["cells"])
    ax.set_title(f"{panel['title']}\n{available}/{len(panel['rows'])*len(TARGETS)} displayed cells available",
                 fontsize=12 if compact else 15,pad=45 if compact else 55)
    return im


def render_figures(derivation,out,color_limit=.35):
    if not _finite(color_limit) or color_limit <= 0:
        raise ValueError("Color limit must be finite and positive")
    plt = _plotting()
    panels,files = derivation["panels"],[]
    title = "Primary transfer: combined logistic + model/opponent identity"
    subtitle = "Paired Brier improvement over ordered-context baseline · green better / red worse"
    foot = ("G = canonical game-shape groups; original all-method common support. "
            "CI > 0 / < 0 / spans 0 describes the saved paired 95% interval; CI NA = unavailable.\n"
            "Intervals are descriptive, unadjusted for multiplicity, and conditional on fixed fitted forecasts. "
            f"Colors saturate at ±{color_limit:g}; printed values are exact to rounding.")
    fig,axes = plt.subplots(1,3,figsize=(19,7.3),gridspec_kw={"wspace":.62})
    for ax,panel in zip(axes,panels):
        im = _draw_panel(ax,panel,plt,color_limit,compact=True)
    fig.suptitle(title+"\n"+subtitle,fontsize=16,y=.99)
    fig.subplots_adjust(left=.105,right=.94,top=.72,bottom=.16)
    cax = fig.add_axes((.957,.23,.012,.40))
    fig.colorbar(im,cax=cax,extend="both",label="Δ Brier (baseline − method)")
    fig.text(.5,.025,foot,ha="center",fontsize=9)
    stem = "primary-transfer-overview"
    _save_figure(fig,out,stem)
    plt.close(fig)
    files.extend(f"{stem}.{suffix}" for suffix in ("png","svg","pdf"))
    for panel in panels:
        fig,ax = plt.subplots(figsize=(10.3,7.6 if len(panel["rows"])==6 else 6.5))
        im = _draw_panel(ax,panel,plt,color_limit)
        fig.suptitle("Fixed primary method: combined_logistic_both\n"+subtitle,fontsize=12,y=.99)
        fig.subplots_adjust(left=.25,right=.87,top=.71,bottom=.19)
        cax = fig.add_axes((.90,.24,.025,.39))
        fig.colorbar(im,cax=cax,extend="both",label="Δ Brier (baseline − method)")
        fig.text(.5,.035,foot.replace(" CI >","\nCI >"),ha="center",fontsize=8)
        stem = "primary-transfer-"+panel["name"]
        _save_figure(fig,out,stem)
        plt.close(fig)
        files.extend(f"{stem}.{suffix}" for suffix in ("png","svg","pdf"))
    return files


def run(run_root,out=None,color_limit=.35):
    root = Path(run_root).resolve()
    out = _safe_output(out or root/"report-figures")
    derivation = build_overview(root)
    derivation["plot_source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    derivation["color_limit"] = color_limit
    out.mkdir(parents=True,exist_ok=True)
    derivation["figures"] = render_figures(derivation,out,color_limit)
    for path,expected in derivation["input_sha256"].items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=expected:
            raise ValueError("A saved score/audit source changed during rendering: "+path)
    write_json(out/"derivation.json",derivation)
    return derivation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root",type=Path,required=True)
    parser.add_argument("--out",type=Path)
    parser.add_argument("--color-limit",type=float,default=.35)
    args = parser.parse_args()
    result = run(args.run_root,args.out,args.color_limit)
    print(json.dumps({"figures":result["figures"],"input_files":len(result["input_sha256"]),
                      "method":result["method"],"out":str(args.out or args.run_root/"report-figures")}))


if __name__=="__main__":
    main()
