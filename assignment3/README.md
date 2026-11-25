# Assignment 3 — Reproducibility Instructions

Continuation of the Midterm (`midterm1/rag_system/`) RAG prompt-injection
project. This folder adds a second, independent mitigation (a semantic
output guardrail) on top of the Midterm's existing keyword filter, and
evaluates both against a wider attack battery.

## Setup

Reuses the Midterm's existing environment, no new dependencies.

```bash
cd "midterm1/rag_system"
python3.12 -m venv .venv   # if not already created, see midterm1/rag_system/INSTALL.md
source .venv/bin/activate
pip install -r requirements.txt
cd "../../assignment 3"
```

## Files

- `semantic_guardrail.py` — the new Part 3 mechanism. `GuardedRagSystem`
  extends the Midterm's `RagSystem` (imported, not modified) with a
  semantic, LLM-as-judge output check (`judge_response_is_leaking`),
  layered on top of the existing keyword filter via logical OR.
- `part2_translation_variants.py` — Part 2 extended testing: 6 variants of
  the Translation attack (different language, paraphrase, simplify,
  partial, full-document), run against the baseline configuration only.
- `run_full_evaluation.py` — Parts 5-7: runs the full 30-case battery (24
  attacks + 6 benign queries) through both baseline (keyword filter) and
  improved (keyword + semantic guardrail) configurations in one pass, and
  saves `full_evaluation_results.json`.
- `full_evaluation_results.json` / `part2_translation_variants_results.json`
  — raw experimental evidence (prompts, raw model output, both guardrail
  verdicts, per-case latency) referenced in the technical report.
- `Zakirov_Arlan_Assignment3_Report.docx` — the 2-3 page technical report.
- `presentation/` — the oral-presentation package (not required by the
  assignment brief, built for the in-class defense): the Russian-language
  slide deck (`Zakirov_Arlan_Assignment3_Presentation.pptx/.pdf`), the
  3-speaker speech script (`Текст_выступления_6_минут.md`), and
  `results_chart.png` — a bar chart (baseline vs. improved) of the two
  headline rates from the Results table: genuine secret disclosures (ASR)
  and confabulated-false-secret (hallucination) rate, both per 24 attacks.

## Running the experiments

```bash
cd "AI Security and Risk Analysis/assignment 3"
source "../midterm1/rag_system/.venv/bin/activate"

# Part 2: 6 Translation-attack variants (baseline only)
rm -rf "../midterm1/rag_system/chroma_db"
python3 part2_translation_variants.py

# Parts 5-7: full 30-case baseline-vs-improved battery
rm -rf "../midterm1/rag_system/chroma_db"
python3 run_full_evaluation.py
```

Each run clears and re-ingests the vector DB from scratch (via
`rag.reset_collection()` inside `run_full_evaluation.py`, or manually via
`rm -rf chroma_db` before `part2_translation_variants.py`) to avoid
duplicate-chunk retrieval contamination, a real issue encountered during
development (see AI Use Declaration).

Full run time: roughly 8-10 minutes on a MacBook Air M2 8 GB (30 cases x
up to 2 generations each).

## Supplementary garak run (tooling check)

A supplementary, separate check was run with NVIDIA garak's
`misleading.FalseAssertion` probe, reusing the Assignment 2 environment
(`AI Security and Risk Analysis/Assignment 2 - LLM Safety Garak/.venv`,
`transformers==5.19.0`) and the Assignment 2 model
(`Qwen/Qwen2.5-0.5B-Instruct`), not the 3B RAG model above:

```bash
cd "../Assignment 2 - LLM Safety Garak"
source .venv/bin/activate
python -m garak --model_type huggingface \
  --model_name Qwen/Qwen2.5-0.5B-Instruct \
  --probes misleading.FalseAssertion --generations 1 \
  --report_prefix assignment3_misleading
```

Output lands in `~/.local/share/garak/garak_runs/assignment3_misleading.*`;
a copy of the report, hitlog, and HTML output is kept in this folder under
`garak_runs/` for self-contained submission. Findings (passed/150 per detector out of 150 false-claim prompts):
`MustRefuteClaimKW` 43, `MustRefuteClaimModel` 26, `MitigationBypass` 13;
a fourth detector, `MustContradictNLI`, reported only 5 passed, but a
manual hitlog check found at least one response that correctly refuted
the false premise yet was still scored as a hit, so that detector's
number is not relied upon. See Section 6 of the report for the
plain-language interpretation.

## Known environment gotcha

On this machine, running the local model while several other memory-heavy
processes are open can cause the process to be killed by the OS under
memory pressure. Check `sysctl vm.swapusage` before a run; if `used` is
close to `total`, close other applications first.
