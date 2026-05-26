"""Data loading and validation for the public policy AX lab."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class DataValidationError(ValueError):
    """Raised when curated project data violates the portfolio schema."""


PRIVATE_FIELD_NAMES = {
    "person_name",
    "applicant_name",
    "owner_name",
    "phone",
    "phone_number",
    "email",
    "address",
    "resident_registration_number",
    "rrn",
    "business_registration_number",
}

ALLOWED_CHANNELS = {"direct_loan", "proxy_loan"}
ALLOWED_EXPECTED_STATUSES = {"pass", "needs_review", "fail"}


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path, expected_type: type | None = None) -> Any:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DataValidationError(f"missing json file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DataValidationError(f"invalid json in {path}: {exc}") from exc

    if expected_type is not None and not isinstance(data, expected_type):
        raise DataValidationError(f"{path} must contain {expected_type.__name__}")
    return data


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require_fields(record: dict[str, Any], required: list[str], label: str) -> None:
    if not isinstance(record, dict):
        raise DataValidationError(f"{label} must be object")
    missing = [field for field in required if field not in record or record[field] in ("", None)]
    if missing:
        raise DataValidationError(f"{label} missing required fields: {', '.join(missing)}")


def private_field_paths(value: Any, path: str = "") -> list[str]:
    if isinstance(value, dict):
        matches: list[str] = []
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if key in PRIVATE_FIELD_NAMES:
                matches.append(child_path)
            matches.extend(private_field_paths(child, child_path))
        return matches
    if isinstance(value, list):
        matches = []
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]" if path else f"[{index}]"
            matches.extend(private_field_paths(child, child_path))
        return matches
    return []


def reject_private_fields(record: dict[str, Any], label: str) -> None:
    private = sorted(private_field_paths(record))
    if private:
        raise DataValidationError(f"{label} contains private fields: {', '.join(private)}")


def require_list(record: dict[str, Any], field: str, label: str, *, allow_empty: bool = True) -> None:
    if not isinstance(record.get(field), list):
        raise DataValidationError(f"{label} field must be list: {field}")
    if not allow_empty and not record[field]:
        raise DataValidationError(f"{label} field must be non-empty list: {field}")


def validate_public_policy_records(records: list[dict[str, Any]]) -> None:
    seen: set[str] = set()
    required = [
        "source_id",
        "title",
        "publisher",
        "url",
        "retrieved_at",
        "content_summary",
        "claim_boundary",
    ]
    for record in records:
        require_fields(record, required, "public policy record")
        source_id = record["source_id"]
        reject_private_fields(record, f"public policy record {source_id}")
        if source_id in seen:
            raise DataValidationError(f"duplicate source_id: {source_id}")
        seen.add(source_id)
        if not str(record["url"]).startswith("https://"):
            raise DataValidationError(f"source url must be https: {source_id}")


def validate_fund_programs(programs: list[dict[str, Any]], source_ids: set[str]) -> None:
    seen: set[str] = set()
    required = [
        "program_id",
        "name",
        "channel",
        "support_type",
        "eligibility_conditions",
        "exclusion_conditions",
        "required_documents",
        "application_window",
        "loan_limit",
        "loan_term",
        "interest_rule",
        "source_ids",
    ]
    for program in programs:
        require_fields(program, required, "fund program")
        program_id = program["program_id"]
        reject_private_fields(program, f"fund program {program_id}")
        if program_id in seen:
            raise DataValidationError(f"duplicate program_id: {program_id}")
        seen.add(program_id)

        if program["channel"] not in ALLOWED_CHANNELS:
            raise DataValidationError(f"invalid channel for {program_id}: {program['channel']}")

        for field in ("eligibility_conditions", "exclusion_conditions", "required_documents", "source_ids"):
            require_list(program, field, program_id, allow_empty=False)
        if "exception_rules" in program:
            require_list(program, "exception_rules", program_id)

        unknown_sources = sorted(set(program["source_ids"]) - source_ids)
        if unknown_sources:
            raise DataValidationError(f"{program_id} has unknown source_ids: {unknown_sources}")


def validate_applicant_scenarios(scenarios: list[dict[str, Any]]) -> None:
    seen: set[str] = set()
    required = [
        "scenario_id",
        "description",
        "data_classification",
        "is_synthetic",
        "contains_personal_data",
        "sector",
        "employee_count",
        "years_in_operation",
        "credit_score_band",
        "completed_trainings",
        "youth_employment",
        "business_distress",
        "excluded_sector_flag",
        "missing_fields",
    ]
    required_non_empty = [field for field in required if field != "employee_count"]

    for scenario in scenarios:
        require_fields(scenario, required_non_empty, "applicant scenario")
        if "employee_count" not in scenario:
            raise DataValidationError(f"scenario missing employee_count: {scenario.get('scenario_id')}")

        scenario_id = scenario["scenario_id"]
        label = f"scenario {scenario_id}"
        reject_private_fields(scenario, label)
        if scenario_id in seen:
            raise DataValidationError(f"duplicate scenario_id: {scenario_id}")
        seen.add(scenario_id)

        require_list(scenario, "completed_trainings", scenario_id)
        require_list(scenario, "missing_fields", scenario_id)

        if scenario["data_classification"] != "synthetic_sample":
            raise DataValidationError(f"invalid data_classification: {scenario_id}")
        if scenario["is_synthetic"] is not True:
            raise DataValidationError(f"scenario must be synthetic: {scenario_id}")
        if scenario["contains_personal_data"] is not False:
            raise DataValidationError(f"scenario must not contain personal data: {scenario_id}")
        if scenario["employee_count"] is None and "employee_count" not in scenario["missing_fields"]:
            raise DataValidationError(f"employee_count is null but not listed missing: {scenario_id}")


def validate_response_candidates(
    responses: list[dict[str, Any]],
    program_ids: set[str],
    scenario_ids: set[str],
) -> None:
    seen: set[str] = set()
    required = [
        "response_id",
        "scenario_id",
        "program_id",
        "text",
        "candidate_type",
        "expected_status",
        "expected_failure_tags",
    ]
    for response in responses:
        require_fields(response, required, "response candidate")
        response_id = response["response_id"]
        reject_private_fields(response, f"response candidate {response_id}")
        if response_id in seen:
            raise DataValidationError(f"duplicate response_id: {response_id}")
        seen.add(response_id)

        if response["program_id"] not in program_ids:
            raise DataValidationError(f"unknown program_id in response: {response['program_id']}")
        if response["scenario_id"] not in scenario_ids:
            raise DataValidationError(f"unknown scenario_id in response: {response['scenario_id']}")
        if response["expected_status"] not in ALLOWED_EXPECTED_STATUSES:
            raise DataValidationError(f"invalid expected_status: {response['expected_status']}")
        if response["candidate_type"] != "sample_response":
            raise DataValidationError(f"invalid candidate_type: {response['candidate_type']}")
        require_list(response, "expected_failure_tags", response_id)
        if response.get("contains_personal_data") is not None and response["contains_personal_data"] is not False:
            raise DataValidationError(f"response must not contain personal data: {response_id}")
