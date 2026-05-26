"""CLI for the public policy AX ontology-RAG PoC lab."""

from __future__ import annotations

import argparse
from typing import Any

from policy_ax.case_builder import build_evaluation_cases
from policy_ax.data_io import (
    load_json,
    project_root,
    validate_applicant_scenarios,
    validate_fund_programs,
    validate_public_policy_records,
    validate_response_candidates,
    write_json,
)
from policy_ax.evaluator import evaluate_responses
from policy_ax.ontology import validate_ontology_schema, validate_program_ontology_links
from policy_ax.reporting import write_report


def load_all() -> tuple[
    Any,
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    root = project_root()
    sources = load_json(root / "data/raw/public_policy_records.json", expected_type=list)
    programs = load_json(root / "data/raw/fund_programs.json", expected_type=list)
    scenarios = load_json(root / "data/raw/applicant_scenarios.json", expected_type=list)
    responses = load_json(root / "data/raw/response_candidates.json", expected_type=list)
    schema = load_json(root / "ontology_schema.json", expected_type=dict)
    return root, sources, programs, scenarios, responses, schema


def validate_data_command() -> None:
    _, sources, programs, scenarios, responses, _ = load_all()
    source_ids = {source["source_id"] for source in sources}
    validate_public_policy_records(sources)
    validate_fund_programs(programs, source_ids)
    validate_applicant_scenarios(scenarios)
    validate_response_candidates(
        responses,
        {program["program_id"] for program in programs},
        {scenario["scenario_id"] for scenario in scenarios},
    )
    print("OK: data validation passed")


def validate_ontology_command() -> None:
    _, sources, programs, _, _, schema = load_all()
    validate_ontology_schema(schema)
    validate_program_ontology_links(programs, schema, {source["source_id"] for source in sources})
    print("OK: ontology validation passed")


def build_cases_command() -> list[dict[str, Any]]:
    root, _, programs, scenarios, _, _ = load_all()
    cases = build_evaluation_cases(programs, scenarios)
    write_json(root / "data/processed/evaluation_cases.json", cases)
    print(f"OK: wrote {len(cases)} evaluation cases")
    return cases


def evaluate_command() -> list[dict[str, Any]]:
    root, _, _, _, responses, _ = load_all()
    cases = load_json(root / "data/processed/evaluation_cases.json", expected_type=list)
    results = evaluate_responses(responses, cases)
    print(f"OK: evaluated {len(results)} response candidates")
    return results


def report_command(results: list[dict[str, Any]] | None = None) -> None:
    root = project_root()
    cases = load_json(root / "data/processed/evaluation_cases.json", expected_type=list)
    if results is None:
        _, _, _, _, responses, _ = load_all()
        results = evaluate_responses(responses, cases)
    write_report(root / "reports/sample_poc_report.md", cases, results)
    print("OK: wrote reports/sample_poc_report.md")


def demo_command() -> None:
    validate_data_command()
    validate_ontology_command()
    build_cases_command()
    results = evaluate_command()
    report_command(results)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Public policy AX ontology-RAG PoC lab")
    parser.add_argument(
        "command",
        choices=["demo", "validate-data", "validate-ontology", "build-cases", "evaluate", "report"],
    )
    args = parser.parse_args(argv)
    if args.command == "demo":
        demo_command()
    elif args.command == "validate-data":
        validate_data_command()
    elif args.command == "validate-ontology":
        validate_ontology_command()
    elif args.command == "build-cases":
        build_cases_command()
    elif args.command == "evaluate":
        evaluate_command()
    elif args.command == "report":
        report_command()


if __name__ == "__main__":
    main()
