# AI Use Declaration — Assignment 3

Substantive AI assistance (Claude, Anthropic) was used throughout this
assignment, as follows:

- **Part 1-2 (baseline review, extended testing design):** AI assistance
  was used to review the Midterm's own results and propose which
  residual vulnerability to investigate further (the Translation-attack
  blind spot), and to design 6 attack variants testing whether the
  vulnerability was specific to the word "translate" or broader. The
  choice of mechanism and variants was discussed and confirmed before
  implementation; all 6 variants were actually executed against the live
  local model, not assumed.
- **Part 3 (mechanism implementation):** AI assistance wrote the
  `semantic_guardrail.py` module (a new file, not an edit to the
  Midterm's existing `rag_core.py`). The first, zero-shot version of the
  judge prompt was tested and found to fail on an unambiguous case; this
  failure is reported honestly in the technical report rather than
  hidden, and the revised few-shot prompt that fixed it on short texts
  (but not on longer responses) is the one actually used in the final
  evaluation.
- **Parts 5-7 (experimental evaluation):** AI assistance wrote and ran
  `run_full_evaluation.py` against the real local model
  (`mlx-community/Qwen2.5-3B-Instruct-4bit`), producing
  `full_evaluation_results.json`. All reported numbers (ASR, false-refusal
  rate, latency) were computed directly from that file, not estimated or
  invented. A real duplicate-document-ingestion bug was found and fixed
  mid-development (the vector database was not cleared between two
  successive runs, corrupting one sanity-check result) before the final
  battery was run on a clean database.
- **Part 3 tooling check (supplementary):** AI assistance ran NVIDIA
  garak's `misleading.FalseAssertion` probe against the Assignment 2
  model (`Qwen/Qwen2.5-0.5B-Instruct`, reusing that assignment's
  environment) as a real, executed check, not a simulated one. Before
  reporting any number from it, a manual hitlog review was done to
  confirm detector polarity; this uncovered that one of the four
  detectors (`MustContradictNLI`) scored at least one correct refutation
  as a failure, so that specific detector's figure is reported as
  unreliable rather than included in the headline numbers.
- **Parts 8-9 (interpretability, human-AI interaction) and the final
  report:** AI assistance drafted the written analysis and the technical
  report text, structured around the actual experimental findings above.

All experimental results in the report were produced by actually running
the code against the live local model; none were fabricated, estimated,
or extrapolated from the Midterm's prior results.
