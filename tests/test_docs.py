import re
import unittest

from policy_ax.data_io import load_json, project_root


REQUIRED_DOCS = [
    "README.md",
    "data_sources.md",
    "rubric.md",
    "docs/ax_service_design_note.md",
    "docs/owner_guide.md",
    "docs/implementation_walkthrough.md",
    "docs/domain_study_pack.md",
    "docs/ontology_modeling_notes.md",
    "docs/evaluator_logic_notes.md",
    "docs/ax_consulting_talk_track.md",
    "docs/interview_defense_pack.md",
    "docs/development_journal.md",
    "docs/decision_log.md",
    "docs/phase2_llm_adapter_note.md",
]

REQUIRED_MARKERS = [
    "공개 문서 기반",
    "실제 정책자금 신청 자동화가 아닙니다",
    "실제 정부/소진공 서비스 평가가 아닙니다",
]

FORBIDDEN_CLAIM_PATTERNS = [
    r"(정부|소진공|government|SEMAS).{0,30}(서비스|service).{0,30}(평가|evaluate|evaluated|evaluation)",
    r"(정책자금|policy[- ]?fund).{0,30}(신청|application).{0,30}(자동화|automation|automated)",
    r"(고객 데이터|customer data|customer-data).{0,30}(사용|기반|개선|used|based|improvement)",
    r"(운영 AI|production AI|operating AI).{0,30}(개선|평가|improvement|improved|evaluated)",
]

SAFE_NEGATION_MARKERS = [
    "아닙니다",
    "아니다",
    "아니며",
    "않습니다",
    "않았다",
    "하지 않습니다",
    "하지 않았다",
    "금지",
    "금지 표현",
    "does not",
    "do not",
    "not ",
    "no ",
    "never",
    "without",
    "?",
    "인가요",
]


class DocumentSafetyTests(unittest.TestCase):
    def test_required_docs_exist_and_are_substantive(self):
        root = project_root()
        for rel in REQUIRED_DOCS:
            path = root / rel
            self.assertTrue(path.exists(), rel)
            text = path.read_text(encoding="utf-8")
            self.assertGreater(len(text.strip()), 500, rel)

    def test_boundary_markers_exist_in_each_required_doc(self):
        root = project_root()
        for rel in REQUIRED_DOCS:
            path = root / rel
            text = path.read_text(encoding="utf-8")
            for marker in REQUIRED_MARKERS:
                self.assertIn(marker, text, rel)

    def test_forbidden_claims_absent(self):
        root = project_root()
        for rel in REQUIRED_DOCS:
            path = root / rel
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                lowered = line.lower()
                safe_negated = any(marker.lower() in lowered for marker in SAFE_NEGATION_MARKERS)
                for pattern in FORBIDDEN_CLAIM_PATTERNS:
                    if re.search(pattern, line, flags=re.IGNORECASE) and not safe_negated:
                        self.fail(f"{rel}:{line_number} matches forbidden claim pattern: {pattern}")

    def test_documented_source_ids_match_raw_registry(self):
        root = project_root()
        records = load_json(root / "data/raw/public_policy_records.json", expected_type=list)
        raw_ids = {record["source_id"] for record in records}
        documented_ids = set()

        for line in (root / "data_sources.md").read_text(encoding="utf-8").splitlines():
            if not line.startswith("| src_"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            documented_ids.add(cells[0])

        self.assertEqual(documented_ids, raw_ids)


if __name__ == "__main__":
    unittest.main()
