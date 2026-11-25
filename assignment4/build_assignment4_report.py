from docx import Document
from docx.shared import Pt, Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()
section = doc.sections[0]
for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
    setattr(section, m, Cm(1.8))


def add_heading_no_keepnext(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = False
    h.paragraph_format.page_break_before = False
    return h


def p(text, size=10.5):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(4)
    r = para.add_run(text)
    r.font.size = Pt(size)
    return para


def make_table(rows_data, col_widths, font_size=9.3):
    table = doc.add_table(rows=len(rows_data), cols=len(rows_data[0]))
    table.style = "Light Grid Accent 1"
    table.autofit = False
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblLayout = OxmlElement("w:tblLayout")
    tblLayout.set(qn("w:type"), "fixed")
    tblPr.append(tblLayout)
    for i, row_vals in enumerate(rows_data):
        cells = table.rows[i].cells
        for j, val in enumerate(row_vals):
            cells[j].text = val
            cells[j].width = col_widths[j]
            for para in cells[j].paragraphs:
                for r in para.runs:
                    r.font.size = Pt(font_size)
                    if i == 0:
                        r.bold = True
    for col, w in zip(table.columns, col_widths):
        col.width = w
    return table


# ---------------- TITLE ----------------
title = doc.add_heading("Continuous Monitoring and Deployment Readiness", level=0)
title.paragraph_format.space_after = Pt(2)
sub = doc.add_paragraph()
sub.add_run(
    "From a Semantic-Leak Mitigation to an Operational Governance Decision "
    "for a Local RAG System"
).italic = True
auth = doc.add_paragraph()
auth.add_run(
    "Zakirov Arlan | AI Security and Risk Analysis (AISRA1301) | QAIRU AI+X"
).italic = True

# ---------------- 1 ----------------
add_heading_no_keepnext(doc, "1. Title and AI System Overview", 1)
p(
    "This study continues the same research system from the Midterm and "
    "Assignment 3: a local RAG pipeline (mlx-community/Qwen2.5-3B-Instruct-4bit "
    "via mlx-lm, all-MiniLM-L6-v2 embeddings, ChromaDB, subword chunking) that "
    "answers questions over a fictional document containing a confidential "
    "secret. No new model or application was built. The objective here shifts "
    "from closing a specific vulnerability to asking an operational question: "
    "can this system be continuously evaluated, monitored and governed once it "
    "is running, and is it ready for controlled deployment."
)

# ---------------- 2 ----------------
add_heading_no_keepnext(doc, "2. Summary of Midterm and Assignment 3 Results", 1)
p(
    "The Midterm's keyword output filter closed 2 of 3 successful attacks out "
    "of 18 but had a structural blind spot: translating or paraphrasing the "
    "secret chapter leaked it without matching any trigger string. Assignment "
    "3 added an independent semantic judge guardrail (a second call to the "
    "same model acting as an auditor) and evaluated both configurations on 30 "
    "cases (24 attacks, 6 benign). Results: genuine secret disclosure fell "
    "from 5/24 (20.8%) to 2/24 (8.3%); benign task success stayed at 3/6 "
    "(50%, unchanged); latency rose 19% (6.25s to 7.46s); a separate "
    "confabulation issue (3/24 cases inventing a false secret) fell from 3 to "
    "2, with only 1 of 3 caught by the new guardrail. A supplementary NVIDIA "
    "garak run on the Assignment 2 model (Qwen2.5-0.5B-Instruct, a different, "
    "smaller model) found a 71-91% failure rate to refute confidently-stated "
    "false claims across three reliable detectors, corroborating the "
    "confabulation finding on an independent system. The single unresolved "
    "case is the flagship English-translation attack: the judge misses it "
    "when the leaking sentence is diluted inside a long response. These "
    "three risks, residual confidentiality leakage, confabulation, and judge "
    "reliability drift, are exactly the ones this assignment puts under "
    "continuous monitoring."
)

# ---------------- 3 ----------------
add_heading_no_keepnext(doc, "3. AI Agency and Autonomy Assessment", 1)
p(
    "The system has no agentic behavior. It makes two kinds of decisions "
    "independently: which stored chunks to retrieve, and what text to "
    "generate or refuse; both are confined to producing a text response, "
    "never a state-changing action. It can access only its own local, "
    "read-only vector database, no external tool, API, network call or write "
    "access exists. It cannot initiate anything: it only ever responds to a "
    "query, and never contacts a user or system on its own. Its operational "
    "boundaries are the system-prompt confidentiality rule plus the two "
    "guardrails; there is no OS-level sandboxing beyond that. Model behavior "
    "can and does conflict with user intent in two concrete, measured ways: "
    "over-refusal on half of benign questions withholds information the user "
    "legitimately wants, and confabulation hands the user a confident, wrong "
    "answer instead of the true one. No action currently requires human "
    "authorization; every response or refusal is fully automated end to end. "
    "This is also the main gap found in this assignment: there is no runtime "
    "mechanism to interrupt a response in progress, the only available "
    "control is terminating the host process. In short, this is a "
    "request-response generator with output filters, not an autonomous "
    "agent, so its operational risk comes entirely from content correctness "
    "and confidentiality rather than from independent action, which is why "
    "monitoring after the fact, rather than in-the-loop approval, is the "
    "right oversight model for it."
)

# ---------------- 4 ----------------
add_heading_no_keepnext(doc, "4. Selected Monitoring or Governance Tool", 1)
p(
    "Evidently AI (Category B) was selected and actually run. Justification: "
    "it is open-source and runs fully offline on this machine, consistent "
    "with the 8GB, no-cloud-dependency constraint set since the Midterm; it "
    "operates directly on the tabular per-case JSON logs the system already "
    "produces, requiring no new instrumentation; and it supports explicit "
    "pass/fail threshold tests (gte/lte conditions), not just visual "
    "comparison, which maps directly onto the threshold-and-alert structure "
    "Part 4 requires. Live-tracing tools such as Langfuse, LangSmith or Arize "
    "Phoenix are built around a continuously served application with "
    "per-request tracing; this system is an offline-evaluated local "
    "prototype with no serving endpoint, so a batch evaluation-report tool "
    "fits its actual architecture better. Evidently was applied to two real "
    "datasets built from this system's own evaluation output: the "
    "Assignment 3 full evaluation (30 cases, the reference/normal window) "
    "and a new, actually-executed controlled-degradation batch (Section 6)."
)

# ---------------- 5 ----------------
add_heading_no_keepnext(doc, "5. Monitoring Indicators and Thresholds", 1)
p(
    "Four indicators were defined, all measured from the same per-case JSON "
    "evaluation logs produced by the RAG pipeline (keyword_triggered, "
    "judge_triggered, final response text, latency). Thresholds are "
    "justified from the Assignment 3 baseline evidence, with one explicit "
    "assumption noted below."
)
rows = [
    ["Indicator", "Threshold", "Frequency", "Response if exceeded"],
    ["Semantic judge catch rate (on known-leak cases)",
     "≥ 50% (floor: below this, the judge adds no signal over chance)",
     "Every evaluation batch (currently manual; recommended nightly)",
     "Alert operator, freeze judge-prompt changes, fall back to keyword filter + manual review"],
    ["Genuine secret disclosure rate (ASR)",
     "≤ 10% (baseline 8.3% + small margin)",
     "Every evaluation batch",
     "Alert operator, log incident, review affected query pattern"],
    ["Confabulation / hallucination rate",
     "≤ 15% (baseline 8.3% + margin for small-N noise)",
     "Every evaluation batch",
     "Flag for human fact-check, do not auto-trust unverified claims"],
    ["Average response latency",
     "≤ 9.0 s (baseline 7.46 s + ~20% margin)",
     "Every batch; live if deployed",
     "Investigate memory pressure (known 8GB swap risk), consider request queuing"],
]
make_table(rows, [Cm(4.6), Cm(4.2), Cm(3.6), Cm(5.1)])
doc.add_paragraph()

# ---------------- 6 ----------------
add_heading_no_keepnext(doc, "6. Monitoring Experiment and Results", 1)
p(
    "A controlled degradation experiment (monitoring_degradation_experiment.py) "
    "replayed the four raw model outputs that are known, from Assignment 3, to "
    "genuinely disclose the secret before guardrail filtering (B16, C19, C21, "
    "C22) through two real judge configurations on the live Qwen2.5-3B model: "
    "the actual few-shot judge used in Assignment 3, and the earlier, "
    "documented zero-shot judge prompt that Assignment 3 already recorded as "
    "having failed during development. This is an offline, simulated "
    "regression test (a replayed configuration change), not a live production "
    "alert; it is reported as such. Normal-window result: the few-shot judge "
    "caught 3 of 4 (75%), matching the Assignment 3 record exactly. "
    "Risk-scenario result: the zero-shot judge caught 0 of 4 (0%); every one "
    "of the four known leaks would reach the user. Evidently's test suite "
    "(build_evidently_report.py, output: evidently_report.html) correctly "
    "passed both thresholds on the reference window and failed both on the "
    "current window: judge catch rate 0% is below the 50% floor, and genuine "
    "leak rate 100% on this subset is far above the 10% system-wide ceiling. "
    "The keyword-filter indicator, by contrast, did not detect this "
    "regression at all, since it is structurally blind to judge-level "
    "changes, confirming that no single indicator is sufficient and that the "
    "four indicators must be monitored together. Detection was immediate, on "
    "the very next evaluation run after the simulated change, so detection "
    "latency is bounded only by how often the batch runs; this argues for "
    "scheduling it automatically rather than triggering it manually, which is "
    "the current, unautomated state of this monitoring. No false alarms "
    "occurred. The main limitation is sample size: this targeted indicator "
    "was exercised on only 4 cases, sufficient to demonstrate detection but "
    "too small to estimate a precise false-alarm rate."
)

# ---------------- 7 ----------------
add_heading_no_keepnext(doc, "7. Scalable Oversight and Human Control", 1)
p(
    "Retrieval, generation and both guardrail checks run fully automatically, "
    "with no human step in the synchronous request path (Figure 1, Appendix "
    "A). Human review is currently triggered only by an alert from the "
    "periodic Evidently check: judge catch rate below 50%, ASR above 10%, "
    "confabulation above 15%, or latency above 9.0s. The operator (Arlan, as "
    "sole developer of this academic prototype; a named on-call engineer in "
    "a real deployment) is responsible for triaging the alert, deciding "
    "whether to roll back a prompt/config change, adjust a threshold, or "
    "escalate, and recording that decision in an audit log. This audit log "
    "is currently a manual text record, not an automated one. There is no "
    "mechanism to interrupt an individual response already in progress; the "
    "system level is stopped only by terminating the process, a limitation "
    "shared with Section 3. As usage scales, reviewing every alert manually "
    "and running the monitoring batch by hand will not scale; the "
    "recommended path is to schedule the Evidently batch automatically, page "
    "the operator only on an actual threshold breach rather than requiring a "
    "manual check, and replace 100% manual reading of judge verdicts with "
    "periodic, sampled human audit."
)

# ---------------- 8 ----------------
add_heading_no_keepnext(doc, "8. Residual Risk and Deployment Readiness Decision", 1)
p(
    "Seven risks were reviewed against current controls: (1) the flagship "
    "English-translation confidentiality leak, unresolved, high severity; "
    "(2) judge-prompt/config regression, as demonstrated in Section 6, now "
    "detectable offline but not yet monitored automatically, medium; "
    "(3) confabulation of a false secret, only 1 of 3 cases caught, "
    "medium-high; (4) the same-model self-critique design, an architectural "
    "ceiling on what the judge can ever catch, medium; (5) the pre-existing "
    "50% false-refusal rate on benign questions, a usability risk, medium; "
    "(6) no real-time circuit breaker for an in-progress response, medium; "
    "(7) memory-pressure process termination on the 8GB host, low-medium. "
    "Decision: CONDITIONAL GO. The system shows real, measured risk "
    "reduction and now has at least an offline capability to detect further "
    "regressions in the mechanism tested here, which supports controlled use. "
    "It is not an unconditional GO because one high-severity confidentiality "
    "gap remains open and monitoring is still manual, not automatic or "
    "real-time. Conditions: (a) restrict deployment to internal, "
    "non-adversarial use until the flagship leak is closed or a compensating "
    "control is added (e.g. flagging any whole-chapter transform/translate "
    "request for mandatory human review); (b) automate the Evidently batch "
    "on a schedule instead of manual triggering; (c) implement the "
    "refusal-reason transparency fix recommended in Assignment 3; "
    "(d) add a basic request-level timeout as a first circuit breaker."
)

# ---------------- 9 ----------------
add_heading_no_keepnext(doc, "9. Limitations and Recommendations", 1)
p(
    "The degradation experiment used n=4 for its targeted indicator, enough "
    "to demonstrate detection but too small for a precise false-alarm-rate "
    "estimate. Evidently was applied in offline/batch mode only; no live "
    "request-level tracing is integrated, an acknowledged mismatch between "
    "the tool's typical use case and this unserved prototype. The same-model "
    "judge remains a structural ceiling regardless of monitoring. "
    "Recommendations: schedule the monitoring batch automatically rather "
    "than running it by hand; add a dedicated classification-quality metric "
    "for confabulation instead of a generic drift test; adopt an "
    "independent, differently-trained judge model; build a minimal "
    "request-level circuit breaker; and re-run garak-style misinformation "
    "probes on a recurring cadence as part of the same monitoring cycle "
    "rather than as a one-off check."
)

# ---------------- 10 ----------------
add_heading_no_keepnext(doc, "10. References", 1)
p(
    "Schulhoff, S., et al. (2023). Ignore This Title and HackAPrompt: "
    "Exposing Systemic Vulnerabilities of LLMs Through a Global-Scale Prompt "
    "Hacking Competition. EMNLP 2023."
)
p("Evidently AI. Open-source ML and LLM observability framework. https://www.evidentlyai.com/")

# ---------------- APPENDIX (not counted toward page limit) ----------------
add_heading_no_keepnext(doc, "Appendix A: Oversight Workflow Diagram", 1)
p(
    "Figure 1. Interaction between the RAG system, the two automated "
    "guardrails, the periodic Evidently monitoring job, and the human "
    "operator. Automated steps are shown with a navy border; steps "
    "requiring a human are shown with a red border and a light orange fill."
)
doc.add_picture("oversight_workflow_diagram.png", width=Cm(16.5))

doc.save("Zakirov_Arlan_Assignment4_Report.docx")
print("saved docx")
