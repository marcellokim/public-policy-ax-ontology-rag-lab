import unittest

from policy_ax.case_builder import build_evaluation_cases
from policy_ax.data_io import load_json, project_root


class CaseBuilderTests(unittest.TestCase):
    def setUp(self):
        root = project_root()
        self.programs = load_json(root / "data/raw/fund_programs.json", expected_type=list)
        self.scenarios = load_json(root / "data/raw/applicant_scenarios.json", expected_type=list)

    def test_builds_at_least_40_cases(self):
        cases = build_evaluation_cases(self.programs, self.scenarios)

        self.assertGreaterEqual(len(cases), 40)

    def test_case_contains_answer_requirements_and_sources(self):
        case = build_evaluation_cases(self.programs, self.scenarios)[0]

        self.assertIn("case_id", case)
        self.assertIn("program_id", case)
        self.assertIn("program_name", case)
        self.assertIn("scenario_id", case)
        self.assertIn("scenario_description", case)
        self.assertIn("question", case)
        self.assertIn("answer_requirements", case)
        self.assertIn("source_ids", case)
        self.assertIn("expected_source_ids", case)
        self.assertIn("eligibility_judgment", case["answer_requirements"])

    def test_missing_info_case_requires_followup(self):
        cases = build_evaluation_cases(self.programs, self.scenarios)
        missing_cases = [
            case for case in cases if case["scenario_id"] == "scn_missing_employee_count"
        ]

        self.assertTrue(missing_cases)
        self.assertTrue(
            any("missing_information" in case["answer_requirements"] for case in missing_cases)
        )
        self.assertTrue(any("상시근로자 수" in case["question"] for case in missing_cases))
        self.assertTrue(all(case["has_missing_information"] for case in missing_cases))

    def test_case_order_and_ids_are_stable(self):
        first = build_evaluation_cases(self.programs, self.scenarios)
        second = build_evaluation_cases(list(reversed(self.programs)), list(reversed(self.scenarios)))

        self.assertEqual([case["case_id"] for case in first], [case["case_id"] for case in second])
        self.assertEqual(first[0]["case_id"], "case_scn_distress_manufacturing__fund_credit_vulnerable")

    def test_answer_requirements_are_deduplicated_and_stable(self):
        programs = [
            {
                **self.programs[0],
                "program_id": "fund_duplicate_requirement_check",
                "exception_rules": ["disaster_or_distress_exception_review"],
            }
        ]
        cases = build_evaluation_cases(programs, self.scenarios)

        for case in cases:
            self.assertEqual(case["answer_requirements"], sorted(set(case["answer_requirements"])))

    def test_source_lists_are_not_aliased(self):
        case = build_evaluation_cases(self.programs, self.scenarios)[0]

        self.assertEqual(case["source_ids"], case["expected_source_ids"])
        self.assertIsNot(case["source_ids"], case["expected_source_ids"])


if __name__ == "__main__":
    unittest.main()
