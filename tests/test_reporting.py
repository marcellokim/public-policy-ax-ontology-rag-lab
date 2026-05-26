import tempfile
import unittest
from pathlib import Path

from policy_ax.case_builder import build_evaluation_cases
from policy_ax.data_io import load_json, project_root
from policy_ax.evaluator import evaluate_responses
from policy_ax.reporting import summarize_results, write_report


class ReportingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = project_root()
        programs = load_json(root / "data/raw/fund_programs.json", expected_type=list)
        scenarios = load_json(root / "data/raw/applicant_scenarios.json", expected_type=list)
        responses = load_json(root / "data/raw/response_candidates.json", expected_type=list)
        cls.cases = build_evaluation_cases(programs, scenarios)
        cls.results = evaluate_responses(responses, cls.cases)

    def test_summary_counts_results(self):
        summary = summarize_results(self.results)
        self.assertEqual(summary["responses"], len(self.results))
        self.assertIn("failure_tags", summary)
        self.assertGreaterEqual(len(summary["failure_tags"]), 8)

    def test_report_contains_boundaries_and_ax_implications(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "report.md"
            write_report(report_path, self.cases, self.results)
            text = report_path.read_text(encoding="utf-8")
        self.assertIn("Not a Government Service Evaluation", text)
        self.assertIn("AX Service Implications", text)
        self.assertIn("Failure Tag Distribution", text)
        self.assertIn("실제 정책자금 신청 자동화가 아닙니다", text)


if __name__ == "__main__":
    unittest.main()
