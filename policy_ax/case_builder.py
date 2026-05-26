"""Evaluation case construction for policy-fund RAG responses."""

from __future__ import annotations

from typing import Any


DEFAULT_REQUIREMENTS = [
    "eligibility_judgment",
    "eligibility_reason",
    "exclusion_check",
    "required_documents",
    "application_window",
    "loan_channel",
    "source_citation",
    "safe_next_action",
]

EXCLUDED_SECTOR_SOURCE_ID = "src_semas_excluded_sectors"


def build_question(program: dict[str, Any], scenario: dict[str, Any]) -> str:
    """Build an evaluation prompt without asserting final eligibility."""
    if "employee_count" in scenario.get("missing_fields", []):
        return (
            f"{scenario['description']}입니다. 상시근로자 수가 없을 때 "
            f"{program['name']} 가능 여부를 어떻게 확인해야 하나요?"
        )
    return (
        f"{scenario['description']}입니다. 이 사업자가 {program['name']}을 "
        "검토할 때 지원 가능성, 제외조건, 필요서류, 근거를 어떻게 안내해야 하나요?"
    )


def answer_requirements_for(program: dict[str, Any], scenario: dict[str, Any]) -> list[str]:
    """Return deterministic answer requirements for a program-scenario pair."""
    requirements = list(DEFAULT_REQUIREMENTS)

    if program.get("exception_rules"):
        requirements.append("exception_check")
    if program.get("loan_limit") or program.get("loan_term"):
        requirements.append("loan_limit_or_term")
    if scenario.get("missing_fields"):
        requirements.append("missing_information")

    return sorted(set(requirements))


def _sorted_records(records: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return sorted(records, key=lambda record: record[key])


def _source_ids_for(program: dict[str, Any], scenario: dict[str, Any]) -> list[str]:
    source_ids = set(program.get("source_ids", []))
    if scenario.get("excluded_sector_flag"):
        source_ids.add(EXCLUDED_SECTOR_SOURCE_ID)
    return sorted(source_ids)


def build_evaluation_cases(
    programs: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build deterministic evaluation prompts for every scenario-program pair."""
    cases: list[dict[str, Any]] = []

    for scenario in _sorted_records(scenarios, "scenario_id"):
        missing_fields = sorted(set(scenario.get("missing_fields", [])))
        for program in _sorted_records(programs, "program_id"):
            source_ids = _source_ids_for(program, scenario)
            cases.append(
                {
                    "case_id": f"case_{scenario['scenario_id']}__{program['program_id']}",
                    "program_id": program["program_id"],
                    "program_name": program["name"],
                    "scenario_id": scenario["scenario_id"],
                    "scenario_description": scenario["description"],
                    "question": build_question(program, scenario),
                    "answer_requirements": answer_requirements_for(program, scenario),
                    "source_ids": list(source_ids),
                    "expected_source_ids": list(source_ids),
                    "has_missing_information": bool(missing_fields),
                    "missing_fields": missing_fields,
                    "expected_channel": program["channel"],
                    "expected_documents": list(program["required_documents"]),
                    "expected_exclusion_conditions": list(program["exclusion_conditions"]),
                    "expected_eligibility_conditions": list(program["eligibility_conditions"]),
                }
            )

    return cases
