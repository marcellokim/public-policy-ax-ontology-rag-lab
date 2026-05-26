import tempfile
import unittest
from pathlib import Path

from policy_ax.data_io import (
    DataValidationError,
    load_json,
    project_root,
    validate_applicant_scenarios,
    validate_fund_programs,
    validate_public_policy_records,
    validate_response_candidates,
)


class DataIOTests(unittest.TestCase):
    def test_project_root_points_to_lab(self):
        root = project_root()
        self.assertEqual(root.name, "public-policy-ax-ontology-rag-lab")
        self.assertTrue((root / "data").exists())

    def test_load_json_rejects_non_array(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text('{"not": "array"}', encoding="utf-8")
            with self.assertRaises(DataValidationError):
                load_json(path, expected_type=list)

    def test_public_policy_records_are_valid(self):
        records = load_json(project_root() / "data/raw/public_policy_records.json", expected_type=list)
        validate_public_policy_records(records)
        self.assertGreaterEqual(len(records), 6)

    def test_public_record_without_url_fails(self):
        with self.assertRaises(DataValidationError):
            validate_public_policy_records([
                {
                    "source_id": "src_bad",
                    "title": "Bad",
                    "publisher": "No publisher",
                    "url": "",
                    "retrieved_at": "2026-05-26",
                    "content_summary": "summary",
                    "claim_boundary": "boundary",
                }
            ])

    def test_public_records_reject_private_fields(self):
        with self.assertRaises(DataValidationError):
            validate_public_policy_records([
                {
                    "source_id": "src_bad",
                    "title": "Bad",
                    "publisher": "No publisher",
                    "url": "https://example.com",
                    "retrieved_at": "2026-05-26",
                    "content_summary": "summary",
                    "claim_boundary": "boundary",
                    "email": "owner@example.com",
                }
            ])

    def test_fund_programs_are_valid(self):
        source_ids = {
            r["source_id"]
            for r in load_json(project_root() / "data/raw/public_policy_records.json", expected_type=list)
        }
        programs = load_json(project_root() / "data/raw/fund_programs.json", expected_type=list)
        validate_fund_programs(programs, source_ids)
        self.assertGreaterEqual(len(programs), 8)

    def test_fund_programs_reject_private_fields(self):
        with self.assertRaises(DataValidationError):
            validate_fund_programs(
                [
                    {
                        "program_id": "fund_bad",
                        "name": "bad",
                        "channel": "direct_loan",
                        "support_type": "loan",
                        "eligibility_conditions": ["small_business_basic"],
                        "exclusion_conditions": ["excluded_sector"],
                        "required_documents": ["application_form"],
                        "application_window": "public notice",
                        "loan_limit": "unknown",
                        "loan_term": "unknown",
                        "interest_rule": "unknown",
                        "source_ids": ["src_1"],
                        "business_registration_number": "000-00-00000",
                    }
                ],
                {"src_1"},
            )

    def test_applicant_scenarios_reject_private_fields(self):
        with self.assertRaises(DataValidationError):
            validate_applicant_scenarios([
                {
                    "scenario_id": "bad",
                    "description": "bad",
                    "data_classification": "synthetic_sample",
                    "is_synthetic": True,
                    "contains_personal_data": False,
                    "sector": "retail",
                    "employee_count": 1,
                    "years_in_operation": 1,
                    "credit_score_band": "normal",
                    "completed_trainings": [],
                    "youth_employment": False,
                    "business_distress": False,
                    "excluded_sector_flag": False,
                    "missing_fields": [],
                    "phone_number": "010-0000-0000",
                }
            ])

    def test_applicant_scenarios_reject_nested_private_fields(self):
        with self.assertRaises(DataValidationError):
            validate_applicant_scenarios([
                {
                    "scenario_id": "bad",
                    "description": "bad",
                    "data_classification": "synthetic_sample",
                    "is_synthetic": True,
                    "contains_personal_data": False,
                    "sector": "retail",
                    "employee_count": 1,
                    "years_in_operation": 1,
                    "credit_score_band": "normal",
                    "completed_trainings": [],
                    "youth_employment": False,
                    "business_distress": False,
                    "excluded_sector_flag": False,
                    "missing_fields": [],
                    "metadata": {
                        "contact": {
                            "email": "owner@example.com",
                        },
                    },
                }
            ])

    def test_applicant_scenarios_reject_non_synthetic_metadata(self):
        scenarios = [
            {
                "scenario_id": "bad",
                "description": "bad",
                "data_classification": "real_applicant",
                "is_synthetic": False,
                "contains_personal_data": True,
                "sector": "retail",
                "employee_count": 1,
                "years_in_operation": 1,
                "credit_score_band": "normal",
                "completed_trainings": [],
                "youth_employment": False,
                "business_distress": False,
                "excluded_sector_flag": False,
                "missing_fields": [],
            }
        ]
        with self.assertRaises(DataValidationError):
            validate_applicant_scenarios(scenarios)

    def test_applicant_scenarios_reject_non_object_records(self):
        with self.assertRaises(DataValidationError):
            validate_applicant_scenarios(["not a dict"])

    def test_applicant_scenarios_are_valid(self):
        scenarios = load_json(project_root() / "data/raw/applicant_scenarios.json", expected_type=list)
        validate_applicant_scenarios(scenarios)
        self.assertGreaterEqual(len(scenarios), 5)

    def test_response_candidates_are_valid(self):
        programs = load_json(project_root() / "data/raw/fund_programs.json", expected_type=list)
        scenarios = load_json(project_root() / "data/raw/applicant_scenarios.json", expected_type=list)
        responses = load_json(project_root() / "data/raw/response_candidates.json", expected_type=list)
        validate_response_candidates(
            responses,
            {p["program_id"] for p in programs},
            {s["scenario_id"] for s in scenarios},
        )
        self.assertGreaterEqual(len(responses), 12)

    def test_response_candidates_require_sample_response_type(self):
        responses = [
            {
                "response_id": "rsp_bad",
                "scenario_id": "scn_1",
                "program_id": "fund_1",
                "text": "bad",
                "candidate_type": "real_customer_response",
                "expected_status": "needs_review",
                "expected_failure_tags": [],
            }
        ]
        with self.assertRaises(DataValidationError):
            validate_response_candidates(responses, {"fund_1"}, {"scn_1"})

    def test_response_candidates_reject_private_fields(self):
        responses = [
            {
                "response_id": "rsp_bad",
                "scenario_id": "scn_1",
                "program_id": "fund_1",
                "text": "bad",
                "candidate_type": "sample_response",
                "expected_status": "needs_review",
                "expected_failure_tags": [],
                "email": "applicant@example.com",
            }
        ]
        with self.assertRaises(DataValidationError):
            validate_response_candidates(responses, {"fund_1"}, {"scn_1"})

    def test_response_candidates_require_failure_tags_list(self):
        responses = [
            {
                "response_id": "rsp_bad",
                "scenario_id": "scn_1",
                "program_id": "fund_1",
                "text": "bad",
                "candidate_type": "sample_response",
                "expected_status": "needs_review",
                "expected_failure_tags": "unsupported_claim",
            }
        ]
        with self.assertRaises(DataValidationError):
            validate_response_candidates(responses, {"fund_1"}, {"scn_1"})


if __name__ == "__main__":
    unittest.main()
