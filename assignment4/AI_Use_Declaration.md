# AI Use Declaration — Assignment 4

Substantive AI assistance (Claude, Anthropic) was used throughout this
assignment, as follows:

- **Part 1-2 (review of prior results, autonomy assessment):** AI
  assistance drafted the summary of Midterm and Assignment 3 findings and
  the AI agency/autonomy analysis, grounded directly in the real,
  previously-recorded results from those assignments (no new claims were
  introduced without evidence).
- **Part 3 (monitoring tool selection and application):** AI assistance
  selected Evidently AI, wrote `build_evidently_report.py`, and actually
  ran it to produce `evidently_report.html` and
  `monitoring_metrics_summary.json` against real data (Assignment 3's
  evaluation output and this assignment's own degradation experiment). The
  Evidently 0.7.x API (`Dataset`, `DataDefinition`, `Report`,
  `MeanValue`/`gte`/`lte` tests) was introspected directly via Python
  before use, since it differs materially from older Evidently versions
  documented in most tutorials.
- **Part 5 (monitoring experiment):** AI assistance wrote and ran
  `monitoring_degradation_experiment.py` against the live local model
  (`mlx-community/Qwen2.5-3B-Instruct-4bit`). The four known-leak raw
  responses were reused verbatim from Assignment 3's own
  `full_evaluation_results.json` rather than regenerated, to isolate the
  judge-configuration variable from generation variance; this choice is
  disclosed in the script's own docstring and in the technical report. The
  "zero-shot judge" prompt is a reconstruction (examples section removed)
  of the prompt Assignment 3's `semantic_guardrail.py` already documents as
  having failed during development, not a new fabrication.
- **Part 7 (oversight diagram):** AI assistance built
  `build_oversight_diagram.py` with matplotlib. The first draft had a
  genuine layout bug (a text annotation overlapping an arrow and a box);
  this was caught by visual inspection of the rendered PNG and fixed before
  use, consistent with this course's established QA practice of rendering
  and checking visual deliverables rather than trusting code correctness
  alone.
- **Report and standalone deliverables:** AI assistance drafted the
  technical report, `monitoring_indicators_table.md` and
  `deployment_decision.md`, all built from the actual experimental numbers
  above; no figure in any of these documents was invented or estimated
  without a traceable source file.

All experimental results (the degradation experiment, the Evidently test
outcomes, the reused Assignment 3 baseline numbers) were produced by
actually running the code against real data or the live local model; none
were fabricated. The report explicitly distinguishes the offline, simulated
nature of the monitoring experiment from a live production alert, per the
assignment's own integrity requirement.
