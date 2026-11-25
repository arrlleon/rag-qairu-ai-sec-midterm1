# Deployment Readiness Decision — Assignment 4, Deliverable E

## Decision: CONDITIONAL GO — Deployment with Restrictions

## Risks reviewed (≥ 5, per Midterm + Assignment 3 + Assignment 4 evidence)

| # | Risk | Status | Severity |
|---|---|---|---|
| 1 | Flagship English-translation confidentiality leak (judge misses it in long responses) | Unresolved | High |
| 2 | Judge-prompt / config regression (demonstrated in this assignment's monitoring experiment) | Detectable offline now, but not yet monitored automatically | Medium |
| 3 | Confabulation of a false secret (3 cases found; only 1 of 3 caught) | Partially mitigated | Medium-High |
| 4 | Same-model self-critique design (generator and judge share weights) | Unresolved, architectural | Medium |
| 5 | 50% false-refusal rate on benign questions (pre-existing, from the system prompt itself) | Unresolved | Medium |
| 6 | No real-time circuit breaker for an in-progress response (only process kill) | Unresolved | Medium |
| 7 | Memory-pressure process termination risk on the 8GB host | Unresolved | Low-Medium |

## Justification

**Experimental evidence.** The semantic guardrail added in Assignment 3
measurably cut genuine secret disclosure from 20.8% to 8.3% across 24 real
attacks, with no measured cost to legitimate task success (50% unchanged)
beyond a 19% latency increase. This assignment adds a second, independent
layer of evidence: a real (not simulated-from-scratch) degradation
experiment shows the new monitoring setup (Evidently AI + four defined
indicators) can actually detect a regression in that same mechanism, not
just describe it on paper.

**Remaining risks.** One high-severity gap is still open: the original,
flagship translation attack still discloses the secret in the full
pipeline. This alone rules out an unconditional GO.

**Monitoring results.** The monitoring indicators and the degradation
experiment (Section 6 of the technical report) show the chosen indicators
work and are sensitive to at least one realistic failure mode (a judge
prompt/config regression), but the batch is currently run manually, not on
a schedule, so detection is not yet continuous.

**Human oversight arrangements.** All request-path decisions are fully
automated (Section 3 of the report); the only defined human checkpoint is
triage of a monitoring alert. This is adequate for an offline research
prototype but not yet sufficient for unrestricted production use, since
there is no automated paging and no real-time interrupt capability.

**System limitations.** Same-model judge ceiling, small-sample monitoring
experiment (n=4 on the targeted indicator), and the unresolved flagship
leak are all limitations that a CONDITIONAL GO, not a GO, should carry
forward explicitly rather than paper over.

## Conditions for deployment

1. Restrict use to internal, non-adversarial users until the flagship
   translation leak is closed, or add a compensating control: flag any
   "translate/retell the whole chapter" style request for mandatory human
   review before the response is released.
2. Automate the Evidently monitoring batch on a schedule (e.g. nightly cron)
   instead of manual triggering.
3. Implement the refusal-reason transparency fix recommended in Assignment 3
   (distinguish "I don't know" from "this is withheld by a filter").
4. Add a basic request-level timeout as a first, minimal circuit breaker.

This system is **not claimed to be fully safe or compliant** solely because
a monitoring tool was applied; the decision above is scoped to the specific
risks actually tested and documented.
