# MATACS Technical Assessment

**Candidate:** Sandesh Goindani  
**Reference:** MATACS-TH-2026-02  
**Time spent:** Approximately 35 minutes  

## Submission files

- [Process flow diagram](diagram/process-flow.png)
- [Design write-up](WRITEUP.md)
- [AI prompts](PROMPTS.md)
- [Expected ranking](ranking.json)
- [Optional offline mock prototype](prototype/run_mock.py)

## Optional prototype

Run `python3 prototype/run_mock.py` to render the extraction prompt and print a concise mock result for A–E. Add `--show-prompts` to print each rendered prompt, or `--json` to print the full mock schema. This is an offline demonstration: it calls no model or API, and its structured fixture facts and generated support lines are mock data, not source quotations.

## AI use

I used ChatGPT to help interpret the brief, explore scoring options, and draft the design and prompt. I corrected an early AI-assisted scoring draft after manually recalculating the weighted totals, which changed the provisional scores for A and C. I also treated C's embedded rank-first sentence as untrusted proposal text, not as evaluation evidence or an authorized instruction.

