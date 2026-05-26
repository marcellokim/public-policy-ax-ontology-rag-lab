import unittest

from policy_ax.case_builder import build_evaluation_cases
from policy_ax.data_io import load_json, project_root
from policy_ax.evaluator import evaluate_response, evaluate_responses


class EvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = project_root()
        cls.programs = load_json(root / "data/raw/fund_programs.json", expected_type=list)
        cls.scenarios = load_json(root / "data/raw/applicant_scenarios.json", expected_type=list)
        cls.responses = load_json(root / "data/raw/response_candidates.json", expected_type=list)
        cls.cases = build_evaluation_cases(cls.programs, cls.scenarios)

    def find_response(self, response_id):
        return next(response for response in self.responses if response["response_id"] == response_id)

    def find_case(self, response):
        return next(
            case
            for case in self.cases
            if case["scenario_id"] == response["scenario_id"]
            and case["program_id"] == response["program_id"]
        )

    def test_good_response_passes(self):
        response = self.find_response("rsp_good_credit_vulnerable")
        result = evaluate_response(response, self.find_case(response))

        self.assertEqual(result["status"], "pass")
        self.assertGreaterEqual(result["score"], 10)
        self.assertEqual(result["failure_tags"], [])

    def test_missing_exclusion_gets_tagged(self):
        response = self.find_response("rsp_missing_exclusion_credit")
        result = evaluate_response(response, self.find_case(response))

        self.assertIn("missing_exclusion_check", result["failure_tags"])

    def test_unsupported_claim_caps_status(self):
        response = self.find_response("rsp_unsupported_credit")
        result = evaluate_response(response, self.find_case(response))

        self.assertIn("unsupported_claim", result["failure_tags"])
        self.assertNotEqual(result["status"], "pass")

    def test_fake_source_id_does_not_satisfy_grounding(self):
        response = dict(self.find_response("rsp_good_credit_vulnerable"))
        case = self.find_case(response)
        text = response["text"]
        for source_id in case["expected_source_ids"]:
            text = text.replace(source_id, "src_fake")
        response["response_id"] = "rsp_fake_source"
        response["text"] = text
        response["expected_failure_tags"] = ["unsupported_claim"]

        result = evaluate_response(response, case)

        self.assertIn("missing_source", result["failure_tags"])
        self.assertIn("unsupported_claim", result["failure_tags"])
        self.assertNotEqual(result["status"], "pass")

    def test_fake_source_id_with_expected_prefix_does_not_satisfy_grounding(self):
        response = dict(self.find_response("rsp_good_credit_vulnerable"))
        case = self.find_case(response)
        text = response["text"]
        for source_id in case["expected_source_ids"]:
            text = text.replace(source_id, f"{source_id}_fake")
        response["response_id"] = "rsp_fake_source_with_prefix"
        response["text"] = text
        response["expected_failure_tags"] = ["unsupported_claim"]

        result = evaluate_response(response, case)

        self.assertIn("missing_source", result["failure_tags"])
        self.assertIn("unsupported_claim", result["failure_tags"])
        self.assertNotEqual(result["status"], "pass")

    def test_hyphenated_fake_source_id_does_not_satisfy_grounding(self):
        response = dict(self.find_response("rsp_good_credit_vulnerable"))
        case = self.find_case(response)
        text = response["text"]
        for source_id in case["expected_source_ids"]:
            text = text.replace(source_id, f"{source_id}-fake")
        response["response_id"] = "rsp_hyphenated_fake_source"
        response["text"] = text
        response["expected_failure_tags"] = ["unsupported_claim"]

        result = evaluate_response(response, case)

        self.assertIn("missing_source", result["failure_tags"])
        self.assertIn("unsupported_claim", result["failure_tags"])
        self.assertNotEqual(result["status"], "pass")

    def test_period_suffixed_fake_source_id_does_not_satisfy_grounding(self):
        response = dict(self.find_response("rsp_good_credit_vulnerable"))
        case = self.find_case(response)
        text = response["text"]
        for source_id in case["expected_source_ids"]:
            text = text.replace(source_id, f"{source_id}.fake")
        response["response_id"] = "rsp_period_suffixed_fake_source"
        response["text"] = text
        response["expected_failure_tags"] = ["unsupported_claim"]

        result = evaluate_response(response, case)

        self.assertIn("missing_source", result["failure_tags"])
        self.assertIn("unsupported_claim", result["failure_tags"])
        self.assertNotEqual(result["status"], "pass")

    def test_source_id_with_korean_particle_still_satisfies_grounding(self):
        response = dict(self.find_response("rsp_good_credit_vulnerable"))
        case = self.find_case(response)
        text = response["text"]
        for source_id in case["expected_source_ids"]:
            text = text.replace(source_id, f"{source_id}와")
        response["text"] = text

        result = evaluate_response(response, case)

        self.assertNotIn("missing_source", result["failure_tags"])
        self.assertEqual(result["status"], "pass")

    def test_source_id_with_sentence_punctuation_still_satisfies_grounding(self):
        response = dict(self.find_response("rsp_good_credit_vulnerable"))
        case = self.find_case(response)
        text = response["text"]
        for source_id in case["expected_source_ids"]:
            text = text.replace(source_id, f"{source_id}.")
        response["text"] = text

        result = evaluate_response(response, case)

        self.assertNotIn("missing_source", result["failure_tags"])
        self.assertEqual(result["status"], "pass")

    def test_overconfident_missing_info_gets_tagged(self):
        response = self.find_response("rsp_overconfident_missing_info")
        result = evaluate_response(response, self.find_case(response))

        self.assertIn("overconfident_eligibility_decision", result["failure_tags"])
        self.assertIn("missing_followup_question", result["failure_tags"])

    def test_safe_missing_info_response_passes(self):
        response = self.find_response("rsp_good_missing_info")
        result = evaluate_response(response, self.find_case(response))

        self.assertEqual(result["status"], "pass")
        self.assertNotIn("overconfident_eligibility_decision", result["failure_tags"])
        self.assertNotIn("unsafe_application_instruction", result["failure_tags"])

    def test_batch_evaluation_preserves_all_responses(self):
        results = evaluate_responses(self.responses, self.cases)

        self.assertEqual(len(results), len(self.responses))
        self.assertEqual(
            [result["response_id"] for result in results],
            [response["response_id"] for response in self.responses],
        )
        self.assertGreaterEqual(len({tag for r in results for tag in r["failure_tags"]}), 8)

    def test_batch_evaluation_matches_expected_statuses(self):
        results = evaluate_responses(self.responses, self.cases)

        self.assertEqual(
            {result["response_id"]: result["status"] for result in results},
            {response["response_id"]: response["expected_status"] for response in self.responses},
        )

    def test_expected_pass_responses_have_no_failure_tags(self):
        results = evaluate_responses(self.responses, self.cases)
        pass_results = [
            result
            for result in results
            if self.find_response(result["response_id"])["expected_status"] == "pass"
        ]

        self.assertTrue(pass_results)
        self.assertTrue(all(not result["failure_tags"] for result in pass_results))

    def test_result_includes_useful_details(self):
        response = self.find_response("rsp_wrong_channel_youth")
        result = evaluate_response(response, self.find_case(response))

        self.assertIn("details", result)
        self.assertIn("matched_expected_failure_tags", result["details"])
        self.assertIn("rule_notes", result["details"])


if __name__ == "__main__":
    unittest.main()
