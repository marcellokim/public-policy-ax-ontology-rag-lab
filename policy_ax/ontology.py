"""Ontology-like schema validation for the public policy AX lab."""

from __future__ import annotations

from typing import Any


class OntologyValidationError(ValueError):
    """Raised when ontology schema or program links are invalid."""


def validate_ontology_schema(schema: dict[str, Any]) -> None:
    required = ["concepts", "relations", "condition_evidence", "answer_requirements"]
    missing = [field for field in required if field not in schema]
    if missing:
        raise OntologyValidationError(f"schema missing fields: {', '.join(missing)}")

    concepts = schema["concepts"]
    if not isinstance(concepts, list) or len(concepts) < 30:
        raise OntologyValidationError("schema must define at least 30 concepts")
    if len(set(concepts)) != len(concepts):
        raise OntologyValidationError("schema concepts must be unique")
    concept_set = set(concepts)

    relations = schema["relations"]
    if not isinstance(relations, list) or len(relations) < 10:
        raise OntologyValidationError("schema must define at least 10 relations")

    seen_relations: set[tuple[str, str, str]] = set()
    for relation in relations:
        if not isinstance(relation, dict):
            raise OntologyValidationError(f"relation must be object: {relation}")
        for field in ("relation", "from", "to", "required"):
            if field not in relation:
                raise OntologyValidationError(f"relation missing {field}: {relation}")
        if relation["from"] not in concept_set or relation["to"] not in concept_set:
            raise OntologyValidationError(f"relation references unknown concept: {relation}")
        signature = (relation["relation"], relation["from"], relation["to"])
        if signature in seen_relations:
            raise OntologyValidationError(f"duplicate relation: {signature}")
        seen_relations.add(signature)

    if "eligibility_judgment" not in schema["answer_requirements"]:
        raise OntologyValidationError("answer_requirements must include eligibility_judgment")

    _validate_condition_evidence(schema["condition_evidence"])
    _validate_validation_constraints(schema)


def validate_program_ontology_links(
    programs: list[dict[str, Any]],
    schema: dict[str, Any],
    source_ids: set[str],
) -> None:
    validate_ontology_schema(schema)
    condition_evidence = schema["condition_evidence"]

    for program in programs:
        program_id = program.get("program_id", "<unknown>")
        eligibility_conditions = _required_condition_list(program, "eligibility_conditions", program_id)
        exclusion_conditions = _required_condition_list(program, "exclusion_conditions", program_id)
        exception_rules = program.get("exception_rules", [])
        if not isinstance(exception_rules, list):
            raise OntologyValidationError(f"{program_id} exception_rules must be list")
        program_sources = program.get("source_ids", [])
        if not isinstance(program_sources, list) or not program_sources:
            raise OntologyValidationError(f"{program_id} source_ids must be non-empty list")
        unknown_program_sources = set(program_sources) - source_ids
        if unknown_program_sources:
            raise OntologyValidationError(
                f"{program_id} has unknown source_ids: {sorted(unknown_program_sources)}"
            )

        for condition_id in eligibility_conditions + exclusion_conditions + exception_rules:
            if condition_id not in condition_evidence:
                raise OntologyValidationError(f"{program_id} condition lacks evidence mapping: {condition_id}")
            unknown_sources = set(condition_evidence[condition_id]) - source_ids
            if unknown_sources:
                raise OntologyValidationError(f"{condition_id} maps to unknown sources: {sorted(unknown_sources)}")

        for nested in ("application_window", "loan_limit", "loan_term", "interest_rule"):
            nested_value = program.get(nested)
            if not isinstance(nested_value, dict):
                raise OntologyValidationError(f"{program_id} {nested} must be object")
            source_id = nested_value.get("source_id")
            if source_id not in source_ids:
                raise OntologyValidationError(f"{program_id} {nested} has unknown source_id: {source_id}")


def _required_condition_list(program: dict[str, Any], field: str, program_id: str) -> list[str]:
    if field not in program:
        raise OntologyValidationError(f"{program_id} missing {field}")
    conditions = program[field]
    if not isinstance(conditions, list) or not conditions:
        raise OntologyValidationError(f"{program_id} has no {field}")
    return conditions


def _validate_condition_evidence(condition_evidence: Any) -> None:
    if not isinstance(condition_evidence, dict):
        raise OntologyValidationError("condition_evidence must be object")
    for condition_id, evidence_sources in condition_evidence.items():
        if not isinstance(condition_id, str) or not condition_id:
            raise OntologyValidationError("condition_evidence keys must be non-empty strings")
        if not isinstance(evidence_sources, list) or not evidence_sources:
            raise OntologyValidationError(f"condition_evidence must map to non-empty source list: {condition_id}")


def _validate_validation_constraints(schema: dict[str, Any]) -> None:
    if "validation_constraints" not in schema:
        return

    constraints = schema["validation_constraints"]
    if not isinstance(constraints, dict):
        raise OntologyValidationError("validation_constraints must be object")
    required = [
        "dataset_boundaries",
        "allowed_values",
        "required_fields",
        "cross_file_reference_rules",
    ]
    missing = [field for field in required if field not in constraints]
    if missing:
        raise OntologyValidationError(f"validation_constraints missing fields: {', '.join(missing)}")
