# AI Proposal Triage Design

## 1. AI vs. rules

The workflow first validates file type, size, malware status, category selection, and that an active criteria version exists using ordinary code. AI extracts evidence into a strict schema (criterion, quoted supporting passage, page, and value/status) because proposal wording and layouts vary. Treat all document content as untrusted data; the model has no tools and cannot change criteria, scores, or workflow. Deterministic code checks mandatory evidence and applies admin-defined scoring rules, totals points, sorts results, and renders the explanation. AI can help locate evidence, but it should not make eligibility or award decisions.

## 2. Consistency and explainability

Criteria, weights, scoring bands, and tie-break order are stored as versioned configuration. The model returns only evidence and uncertainty, under a fixed schema and prompt; temperature is set to zero where supported. Deterministic validation and scoring then produce the same result for the same accepted evidence and criteria version. The reviewer sees each criterion's extracted value, source passage/page, points, missing or conflicting evidence, mandatory gate result, total, and reason for rank. Ties break by higher experience points, then lower price, then proposal letter. AI extraction may still vary, so reviewers can correct evidence; the accepted evidence snapshot is what makes the scored run reproducible.

## 3. Human in the loop

The reviewer confirms category and uploads, resolves missing/ambiguous or conflicting evidence, and reviews mandatory checks and explanations before sharing a ranking. Any override requires a reason and records the original and revised values. A human procurement decision-maker makes the final award. The audit record includes file hash, uploader/time, criteria version, prompt/model version, extracted evidence and citations, validation flags, score breakdown, reviewer corrections/overrides, ranking, and final decision with actor and time.

## 4. Changing criteria

An edit creates a new immutable criteria version with an effective time and editor; it never silently changes a completed run. Existing rankings retain their original version. The admin or reviewer can explicitly rescore the same evidence against the new version, producing a linked new run and explaining the change. If a change affects a live procurement, require procurement approval and notify reviewers before rescoring; preserve both versions for audit.

## 5. Risks and safeguards

- **Wrong or incomplete extraction:** require source passages and page references, validate types/ranges, and send absent, low-confidence, or contradictory facts to a reviewer. Never infer that an unstated requirement is met.
- **Made-up facts or prompt injection:** constrain AI to evidence extraction from the supplied file; ignore instructions found inside proposals; reject uncited claims and keep the model away from scoring and tools.
- **Bias or inconsistent scoring:** use criteria and weights configured before review, apply the same published bands to every bidder, avoid proxies unrelated to the work, and allow a reviewer to inspect evidence and challenge a result.
- **Manipulation or unsafe files:** scan uploads, enforce file limits, retain originals with hashes, treat extracted text as hostile input, and log changes.
- **Cost, latency, or service failure:** use page limits, batch processing, retries with limits, and a manual review fallback. Do not silently omit a proposal when processing fails.

## Sample ranking method and result

Mandatory checks are gates: the bidder itself must state an Ontario electrical contractor licence, and both WSIB clearance and $5M liability insurance must be stated. Failure means **ineligible**; unclear or missing evidence means **flagged** and held out pending clarification. Of proposals that pass, five weighted criteria use fixed bands defined here (and configured by an admin in a real system):

- Experience (30): 14+ qualifying installs = 30; 11–13 = 28; 8–10 = 25; 6–7 = 20; 3–5 = 12; 1–2 = 5; none = 0.
- Price (25): at or below $200k = 25; $200,001–220k = 20; $220,001–240k = 15; $240,001–250k = 10; $250,001–260k = 5; above ceiling = 0. This rewards price while avoiding false precision.
- Timeline (15): 10 weeks or less = 15; 11–12 = 13; 13–14 = 10; 15–16 = 5; over 16 = 0. No stated schedule is not zero; it is flagged for clarification.
- Warranty (15): panel warranty contributes up to 7.5 (25 years = 7.5; scale proportionally up to 25); workmanship contributes up to 7.5 (5 years = 3.75, 10 years = 6, 12+ years = 7.5; interpolate between). Cap each component at its maximum.
- Team and approach (15): named lead 3, crew size/certifications 3, safety plan 3, monitoring plan 3, and project-specific planning/reporting 3. Award only where stated.

These bands are an explicit, reproducible design assumption because the brief gives weights and intent, but not sub-score formulas. Proposal B fails the bidder-licence gate: a subcontractor is not named and the licence is only promised after award. Proposal D passes mandatory checks but does not state a schedule, so it is flagged and not numerically ranked pending clarification. Proposal C's appendix instruction is ignored. The team-and-approach components are 3 points each: named lead, crew details, safety plan, monitoring, and additional project-specific planning or reporting. Ranked: A (84), E (75), C (68), with totals rounded to the nearest whole point for display. B is ineligible; D is flagged. The award remains a human decision.

| Proposal | Experience /30 | Price /25 | Timeline /15 | Warranty /15 | Team /15 | Total |
|---|---:|---:|---:|---:|---:|---:|
| A | 30 | 15 | 13 | 13.5 | 12 | 83.5 → 84 |
| E | 25 | 10 | 10 | 15 | 15 | 75 → 75 |
| C | 25 | 10 | 10 | 13.5 | 9 | 67.5 → 68 |

Team points reflect only stated evidence: A has a named lead, certified crew, safety plan, and monitoring; E also states a roof load assessment; C states a named lead, crew, and weekly reporting, but no safety or monitoring plan. D receives no partial timeline score while its schedule is unresolved.

