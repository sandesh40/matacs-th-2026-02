#!/usr/bin/env python3
"""Offline demonstration of the proposal extraction prompt using mock fixtures.

No model/API is called. Facts below are compact normalized fixture fields based
on the fictional exercise; original proposal prose is intentionally not stored.
Quoted support refers only to generated fixture lines, not source proposal pages.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# The criteria are supplied as data, mirroring admin-managed configuration.
CRITERIA = [
    {"id": "electrical_licence", "description": "Bidder states it holds an Ontario electrical contractor licence"},
    {"id": "wsib_and_insurance", "description": "WSIB clearance and CAD $5M liability insurance are both stated"},
    {"id": "experience", "description": "Count of commercial installations at least 100 kW in the last five years"},
    {"id": "price", "description": "Total proposal price in CAD"},
    {"id": "timeline", "description": "Stated completion time in weeks from award"},
    {"id": "warranty", "description": "Panel and workmanship warranty years"},
    {"id": "team_and_approach", "description": "Evidence of lead, crew, safety, monitoring, and project planning"},
]

# Structured, mock-only facts. No proposal paragraphs or original wording.
SAMPLES = {
    "A": {"licence": "stated", "wsib": True, "liability_millions": 5, "installations": 14, "price_cad": 238000, "weeks": 12, "panel_years": 25, "workmanship_years": 10, "lead": True, "crew": "6 certified", "safety": True, "monitoring_months": 12, "project_planning": False},
    "B": {"licence": "subcontractor_pending", "wsib": True, "liability_millions": 5, "installations": 6, "price_cad": 189500, "weeks": 10, "panel_years": 25, "workmanship_years": 5, "lead": False, "crew": None, "safety": None, "monitoring_months": None, "project_planning": False},
    "C": {"licence": "stated", "wsib": True, "liability_millions": 5, "installations": 9, "price_cad": 244000, "weeks": 14, "panel_years": 25, "workmanship_years": 10, "lead": True, "crew": "5", "safety": None, "monitoring_months": None, "project_planning": "weekly_reporting", "instruction_like_text_present": True},
    "D": {"licence": "stated", "wsib": True, "liability_millions": 5, "installations": 11, "price_cad": 231000, "weeks": None, "panel_years": 25, "workmanship_years": 10, "lead": True, "crew": None, "safety": True, "monitoring_months": None, "project_planning": "roof_review"},
    "E": {"licence": "stated", "wsib": True, "liability_millions": 5, "installations": 8, "price_cad": 242500, "weeks": 13, "panel_years": 25, "workmanship_years": 12, "lead": True, "crew": "6", "safety": True, "monitoring_months": 24, "project_planning": "roof_assessment"},
}


def extraction_prompt() -> str:
    text = (ROOT / "PROMPTS.md").read_text(encoding="utf-8")
    section = text.split("## Proposal evidence extraction", 1)[1].split("## Optional evidence clarification", 1)[0]
    return section.split("```text", 1)[1].split("```", 1)[0].strip()


def fixture_document(proposal_id: str, facts: dict) -> str:
    """Create terse mock input lines; these are not source-document quotations."""
    return "\n".join(f"{key}={value}" for key, value in facts.items()
                     if key != "instruction_like_text_present" and value is not None)


def prompt_for(proposal_id: str, document: str) -> str:
    return (extraction_prompt()
            .replace("{{proposal_id}}", proposal_id)
            .replace("{{criteria}}", json.dumps(CRITERIA, ensure_ascii=False))
            .replace("{{document_text}}", document))


def mock_response(proposal_id: str, facts: dict) -> dict:
    doc = fixture_document(proposal_id, facts)
    rows = []

    def add(criterion_id: str, value, status="found", confidence=0.99, source_keys=()):
        matches = [line for line in doc.splitlines()
                   if any(line.startswith(f"{key}=") for key in source_keys)] if status != "not_found" else []
        # This synthetic quote cites the generated fixture line, not the original PDF.
        support = [{"page": None, "quote": line} for line in matches]
        rows.append({
            "criterion_id": criterion_id,
            "status": status,
            "value": value,
            "confidence": confidence if support else None,
            "support": support,
            "notes": None,
        })

    licence = facts["licence"]
    add("electrical_licence", licence, "found" if licence == "stated" else "ambiguous", 0.99 if licence == "stated" else 0.96, ("licence",))
    add("wsib_and_insurance", {"wsib": facts["wsib"], "liability_millions": facts["liability_millions"]}, source_keys=("wsib", "liability_millions"))
    add("experience", facts["installations"], source_keys=("installations",))
    add("price", {"currency": "CAD", "amount": facts["price_cad"]}, source_keys=("price_cad",))
    add("timeline", facts["weeks"], "found" if facts["weeks"] is not None else "not_found", 0.99 if facts["weeks"] is not None else None, ("weeks",))
    add("warranty", {"panel_years": facts["panel_years"], "workmanship_years": facts["workmanship_years"]}, source_keys=("panel_years", "workmanship_years"))
    add("team_and_approach", {k: facts[k] for k in ("lead", "crew", "safety", "monitoring_months", "project_planning")}, source_keys=("lead", "crew", "safety", "monitoring_months", "project_planning"))
    return {"proposal_id": proposal_id, "evidence": rows}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show-prompts", action="store_true", help="also print each rendered prompt (fixture input only)")
    parser.add_argument("--json", action="store_true", help="print the full mock extraction schema")
    args = parser.parse_args()

    for proposal_id, facts in SAMPLES.items():
        document = fixture_document(proposal_id, facts)
        rendered = prompt_for(proposal_id, document)
        if args.show_prompts:
            print(f"--- Rendered mock prompt for proposal {proposal_id} ---")
            print(rendered)
        result = mock_response(proposal_id, facts)
        if args.json:
            print(f"--- Mock extraction result for proposal {proposal_id} ---")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            statuses = "; ".join(f"{row['criterion_id']}={row['status']}" for row in result["evidence"])
            print(f"Proposal {proposal_id}: {statuses}")


if __name__ == "__main__":
    main()
