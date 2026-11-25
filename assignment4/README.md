# Assignment 4 — Reproducibility Instructions

Continuation of Assignment 3 (`assignment 3/`), itself a continuation of the
Midterm (`midterm1/rag_system/`). This folder adds continuous monitoring,
an AI agency/autonomy assessment, a scalable-oversight workflow, and a
deployment readiness decision. No new AI system was built.

## Setup

Reuses the Midterm's existing environment for the live-model experiment,
plus `evidently` and `matplotlib` (installed into that same venv).

```bash
cd "midterm1/rag_system"
source .venv/bin/activate   # created per midterm1/rag_system/INSTALL.md
pip install evidently matplotlib
cd "../../assignment 4"
```

The report (`.docx` → `.pdf`) was built and exported with `python3`
(system Python, for `python-docx`) and Pages.app, not the venv above.

## Files

- `monitoring_degradation_experiment.py` — Part 5's controlled monitoring
  experiment. Replays the 4 raw model outputs already known (from
  Assignment 3) to genuinely leak the secret through two real judge
  configurations on the live Qwen2.5-3B model: the actual few-shot judge,
  and the earlier zero-shot judge Assignment 3 already recorded as having
  failed. Output: `monitoring_degradation_results.json`.
- `build_evidently_report.py` — Part 3's monitoring tool (Evidently AI).
  Builds a reference dataset from `assignment 3/full_evaluation_results.json`
  and a current dataset from the degradation experiment, runs a
  `DataDriftPreset` plus two explicit threshold tests (judge catch-rate
  floor, genuine-leak-rate ceiling). Outputs: `evidently_report.html`
  (dashboard) and `monitoring_metrics_summary.json` (numbers).
- `build_oversight_diagram.py` — Part 7's Oversight Workflow Diagram.
  Outputs `oversight_workflow_diagram.png`.
- `build_assignment4_report.py` — builds the technical report docx
  (`python3`, system Python with `python-docx`).
- `Zakirov_Arlan_Assignment4_Report.docx` / `.pdf` — the 2-3 page technical
  report (Appendix A, the diagram, is excluded from that page count per
  the assignment brief).
- `monitoring_indicators_table.md` — Deliverable C, standalone.
- `deployment_decision.md` — Deliverable E, standalone (CONDITIONAL GO).
- `oversight_workflow_diagram.png` — Deliverable D, standalone copy.
- `evidently_report.html`, `monitoring_degradation_results.json`,
  `monitoring_metrics_summary.json` — Deliverable B, monitoring evidence.
- `presentation/` — oral-presentation package (slides, speech script).

## Running the experiment

```bash
cd "AI Security and Risk Analysis/assignment 4"
source "../midterm1/rag_system/.venv/bin/activate"

python3 monitoring_degradation_experiment.py   # ~1-2 min, loads the 3B model once
python3 build_evidently_report.py              # seconds, pure pandas/Evidently
python3 build_oversight_diagram.py             # seconds, pure matplotlib
```

Then, with system Python (`python-docx`, not the venv):

```bash
python3 build_assignment4_report.py
```

## What is simulated vs. actually measured

Per the assignment brief's explicit instruction to distinguish simulations
from deployed functionality: the "risk scenario" judge configuration
(zero-shot prompt) is a real, executed regression test against the live
local model, not a fabricated number — but it is an **offline replay** of
a hypothetical configuration change, not a live production alert from a
deployed, continuously-running service (this system has no such serving
endpoint). The reference-window numbers are the real, previously-recorded
Assignment 3 results, not re-estimated.
