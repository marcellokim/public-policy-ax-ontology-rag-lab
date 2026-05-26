import unittest

from policy_ax.data_io import load_json, project_root
from policy_ax.ontology import (
    OntologyValidationError,
    validate_ontology_schema,
    validate_program_ontology_links,
)


class OntologyTests(unittest.TestCase):
    def test_schema_is_valid(self):
        schema = load_json(project_root() / "ontology_schema.json", expected_type=dict)
        validate_ontology_schema(schema)
        self.assertGreaterEqual(len(schema["concepts"]), 30)
        self.assertGreaterEqual(len(schema["relations"]), 10)

    def test_schema_includes_validation_constraints(self):
        schema = load_json(project_root() / "ontology_schema.json", expected_type=dict)
        validate_ontology_schema(schema)
        self.assertIn("validation_constraints", schema)
        for field in (
            "dataset_boundaries",
            "allowed_values",
            "required_fields",
            "cross_file_reference_rules",
        ):
            self.assertIn(field, schema["validation_constraints"])

    def test_unknown_relation_concept_fails(self):
        schema = {
            "concepts": ["PolicyFundProgram"],
            "relations": [
                {
                    "relation": "bad",
                    "from": "PolicyFundProgram",
                    "to": "MissingConcept",
                    "required": True,
                }
            ],
            "condition_evidence": {},
            "answer_requirements": ["eligibility_judgment"],
        }
        with self.assertRaises(OntologyValidationError):
            validate_ontology_schema(schema)

    def test_program_links_have_condition_evidence(self):
        schema = load_json(project_root() / "ontology_schema.json", expected_type=dict)
        programs = load_json(project_root() / "data/raw/fund_programs.json", expected_type=list)
        sources = load_json(project_root() / "data/raw/public_policy_records.json", expected_type=list)
        validate_program_ontology_links(programs, schema, {s["source_id"] for s in sources})

    def test_program_without_condition_evidence_fails(self):
        schema = load_json(project_root() / "ontology_schema.json", expected_type=dict)
        bad_program = {
            "program_id": "bad",
            "name": "Bad",
            "channel": "direct_loan",
            "support_type": "working_capital",
            "eligibility_conditions": ["unknown_condition"],
            "exclusion_conditions": ["excluded_sector"],
            "exception_rules": [],
            "required_documents": ["business_registration"],
            "application_window": {"type": "announced_period", "source_id": "src_semas_fund_overview"},
            "loan_limit": {"amount_label": "limit", "source_id": "src_semas_fund_overview"},
            "loan_term": {"term_label": "term", "source_id": "src_semas_fund_overview"},
            "interest_rule": {"rate_label": "rate", "source_id": "src_semas_fund_overview"},
            "source_ids": ["src_semas_fund_overview"],
        }
        sources = load_json(project_root() / "data/raw/public_policy_records.json", expected_type=list)
        with self.assertRaises(OntologyValidationError):
            validate_program_ontology_links([bad_program], schema, {s["source_id"] for s in sources})

    def test_condition_evidence_unknown_source_fails(self):
        schema = load_json(project_root() / "ontology_schema.json", expected_type=dict)
        programs = load_json(project_root() / "data/raw/fund_programs.json", expected_type=list)
        source_ids = {
            s["source_id"]
            for s in load_json(project_root() / "data/raw/public_policy_records.json", expected_type=list)
        }

        bad_schema = dict(schema)
        bad_condition_evidence = dict(schema["condition_evidence"])
        bad_condition_evidence["small_business_basic"] = ["src_missing"]
        bad_schema["condition_evidence"] = bad_condition_evidence

        with self.assertRaises(OntologyValidationError):
            validate_program_ontology_links(programs, bad_schema, source_ids)

    def test_nested_program_source_ids_must_resolve(self):
        schema = load_json(project_root() / "ontology_schema.json", expected_type=dict)
        programs = load_json(project_root() / "data/raw/fund_programs.json", expected_type=list)
        source_ids = {
            s["source_id"]
            for s in load_json(project_root() / "data/raw/public_policy_records.json", expected_type=list)
        }

        bad_program = dict(programs[0])
        bad_program["application_window"] = dict(programs[0]["application_window"])
        bad_program["application_window"]["source_id"] = "src_missing_nested"

        with self.assertRaises(OntologyValidationError):
            validate_program_ontology_links([bad_program], schema, source_ids)

    def test_program_top_level_source_ids_must_resolve(self):
        schema = load_json(project_root() / "ontology_schema.json", expected_type=dict)
        programs = load_json(project_root() / "data/raw/fund_programs.json", expected_type=list)
        source_ids = {
            s["source_id"]
            for s in load_json(project_root() / "data/raw/public_policy_records.json", expected_type=list)
        }

        bad_program = dict(programs[0])
        bad_program["source_ids"] = ["src_missing_program_level"]

        with self.assertRaises(OntologyValidationError):
            validate_program_ontology_links([bad_program], schema, source_ids)

    def test_nested_program_source_fields_must_be_objects(self):
        schema = load_json(project_root() / "ontology_schema.json", expected_type=dict)
        programs = load_json(project_root() / "data/raw/fund_programs.json", expected_type=list)
        source_ids = {
            s["source_id"]
            for s in load_json(project_root() / "data/raw/public_policy_records.json", expected_type=list)
        }

        bad_program = dict(programs[0])
        bad_program["application_window"] = "not an object"

        with self.assertRaises(OntologyValidationError):
            validate_program_ontology_links([bad_program], schema, source_ids)


if __name__ == "__main__":
    unittest.main()
