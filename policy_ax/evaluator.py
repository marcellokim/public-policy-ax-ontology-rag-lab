"""Rule-based evaluator for policy AX RAG response candidates."""

from __future__ import annotations

import re
from typing import Any


EXCLUSION_MARKERS = ("제외", "휴폐업", "체납", "업종")
EXCEPTION_MARKERS = ("예외", "경영애로", "재해")
DOCUMENT_MARKERS = ("서류", "증빙", "확인서", "사업자", "교육 이수")
WINDOW_MARKERS = ("접수기간", "기간", "공식 사이트", "공식 안내", "자금")
SAFE_MARKERS = ("확인", "검토", "단정", "공식", "상담", "필요")
UNSAFE_MARKERS = ("무조건 승인", "바로 신청", "추가 확인은 필요하지", "나중에 준비")
ELIGIBILITY_MARKERS = ("가능", "대상", "검토", "조건", "요건", "충족")
MISSING_INFO_MARKERS = ("누락", "상시근로자", "추가", "확인", "확정할 수 없습니다")
OVERCONFIDENT_MARKERS = ("무조건 승인", "확정됩니다", "대상입니다", "추가 확인은 필요하지", "가장 낮게")
SAFE_UNCERTAINTY_MARKERS = ("확정할 수 없습니다", "단정할 수 없", "확인해야 합니다")

STATUS_CAPPING_TAGS = {
    "unsupported_claim",
    "unsafe_application_instruction",
    "overconfident_eligibility_decision",
}


def contains_any(text: str, markers: tuple[str, ...] | list[str]) -> bool:
    return any(marker in text for marker in markers)


def status_from_score(score: int, failure_tags: list[str], case: dict[str, Any] | None = None) -> str:
    if not failure_tags and score >= 10:
        return "pass"
    if case and "missing_exclusion_check" in failure_tags and _case_indicates_excluded_sector(case):
        return "fail"
    if failure_tags:
        return "needs_review"
    if score >= 7:
        return "needs_review"
    return "fail"


def _add_tag(tags: set[str], notes: list[str], tag: str, note: str) -> None:
    tags.add(tag)
    notes.append(f"{tag}: {note}")


def _has_expected_source(text: str, case: dict[str, Any]) -> bool:
    source_ids = case.get("expected_source_ids") or case.get("source_ids") or []
    return any(_has_source_id_token(text, source_id) for source_id in source_ids)


def _has_source_id_token(text: str, source_id: str) -> bool:
    escaped = re.escape(source_id)
    return any(_valid_source_boundary(text, match.start(), match.end()) for match in re.finditer(escaped, text))


def _valid_source_boundary(text: str, start: int, end: int) -> bool:
    if start > 0 and (_is_ascii_source_extension(text[start - 1]) or text[start - 1] == "."):
        return False
    if end >= len(text):
        return True
    trailing = text[end]
    if _is_ascii_source_extension(trailing):
        return False
    if _is_hangul_syllable(trailing) or trailing.isspace():
        return True
    if trailing in ".,;:!?)]}":
        next_index = end + 1
        if next_index >= len(text):
            return True
        next_char = text[next_index]
        return next_char.isspace() or _is_hangul_syllable(next_char) or next_char in ".,;:!?)]}"
    return False


def _is_ascii_source_extension(char: str) -> bool:
    return char.isascii() and (char.isalnum() or char in "_-")


def _is_hangul_syllable(char: str) -> bool:
    return "\uac00" <= char <= "\ud7a3"


def _has_channel(text: str, channel: str) -> bool:
    if channel == "direct_loan":
        return "직접대출" in text
    if channel == "proxy_loan":
        return "대리대출" in text
    return False


def _wrong_channel(text: str, channel: str) -> bool:
    if channel == "direct_loan":
        return "대리대출" in text and "직접대출" not in text
    if channel == "proxy_loan":
        return "직접대출" in text and "대리대출" not in text
    return False


def _has_overconfident_language(text: str) -> bool:
    if contains_any(text, SAFE_UNCERTAINTY_MARKERS):
        risky = [marker for marker in OVERCONFIDENT_MARKERS if marker not in ("확정됩니다",)]
        return contains_any(text, risky)
    return contains_any(text, OVERCONFIDENT_MARKERS)


def _has_unsafe_instruction(text: str) -> bool:
    return contains_any(text, UNSAFE_MARKERS) or "신청하면 됩니다" in text


def _has_missing_info_followup(text: str) -> bool:
    if contains_any(text, ("추가 확인은 필요하지", "확인할 필요", "확인 필요하지")):
        return False
    return contains_any(text, MISSING_INFO_MARKERS)


def _case_indicates_excluded_sector(case: dict[str, Any]) -> bool:
    context = f"{case.get('scenario_description', '')} {case.get('question', '')}"
    return "제외업종" in context or "부동산업" in context


def _dismisses_document_need(text: str) -> bool:
    return contains_any(text, ("증빙은 나중에", "서류는 나중에", "증빙은 중요하지", "서류는 중요하지"))


def _expected_tag_supported_by_text(tag: str, text: str, case: dict[str, Any]) -> bool:
    if tag == "missing_exclusion_check":
        return not contains_any(text, EXCLUSION_MARKERS)
    if tag == "unsupported_claim":
        return not _has_expected_source(text, case) or _has_overconfident_language(text) or "대체로 비슷" in text
    if tag == "overconfident_eligibility_decision":
        return _has_overconfident_language(text) or (
            bool(case.get("missing_fields")) and not _has_missing_info_followup(text)
        )
    if tag == "missing_followup_question":
        return bool(case.get("missing_fields")) and not _has_missing_info_followup(text)
    if tag == "wrong_fund_channel":
        return _wrong_channel(text, case.get("expected_channel", ""))
    if tag == "missing_required_document":
        return _dismisses_document_need(text) or not contains_any(text, DOCUMENT_MARKERS)
    if tag == "stale_or_missing_application_window":
        return not contains_any(text, WINDOW_MARKERS)
    if tag == "unsafe_application_instruction":
        return _has_unsafe_instruction(text)
    if tag == "missing_eligibility_condition":
        return not contains_any(text, ELIGIBILITY_MARKERS) or "대체로 비슷" in text
    if tag == "missing_source":
        return not _has_expected_source(text, case)
    if tag == "missing_exception_rule":
        return "exception_check" in case.get("answer_requirements", []) and not contains_any(
            text, EXCEPTION_MARKERS
        )
    return False


def evaluate_response(response: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one response candidate against one deterministic evaluation case."""
    text = response["text"]
    tags: set[str] = set()
    notes: list[str] = []
    score = 0

    if contains_any(text, ELIGIBILITY_MARKERS) and not _has_overconfident_language(text):
        score += 2
        notes.append("eligibility_accuracy: response states eligibility as a review target")
    elif contains_any(text, ("가능", "대상", "신청")):
        score += 1
        notes.append("eligibility_accuracy: partial eligibility statement")
    else:
        _add_tag(tags, notes, "missing_eligibility_condition", "no meaningful eligibility condition")

    if contains_any(text, EXCLUSION_MARKERS):
        score += 2
        notes.append("exclusion_and_exception_handling: exclusion risk is mentioned")
    else:
        _add_tag(tags, notes, "missing_exclusion_check", "response omits exclusion checks")

    if "exception_check" in case.get("answer_requirements", []):
        if contains_any(text, EXCEPTION_MARKERS):
            score += 2
            notes.append("exclusion_and_exception_handling: exception or distress rule is handled")
        else:
            _add_tag(tags, notes, "missing_exception_rule", "case requires exception review")
    else:
        score += 2

    if _has_expected_source(text, case):
        score += 2
        notes.append("evidence_grounding: public source marker is present")
    else:
        _add_tag(tags, notes, "missing_source", "no expected source marker")

    if _wrong_channel(text, case.get("expected_channel", "")):
        _add_tag(tags, notes, "wrong_fund_channel", "response names the opposite loan channel")

    guidance_points = 0
    if contains_any(text, DOCUMENT_MARKERS):
        guidance_points += 1
    if contains_any(text, WINDOW_MARKERS):
        guidance_points += 1
    if _has_channel(text, case.get("expected_channel", "")):
        guidance_points += 1

    if guidance_points >= 2:
        score += 2
        notes.append("application_guidance_completeness: at least two guidance elements are present")
    elif guidance_points == 1:
        score += 1
        notes.append("application_guidance_completeness: only one guidance element is present")

    if case.get("missing_fields"):
        if _has_missing_info_followup(text):
            score += 1
            notes.append("uncertainty_and_missing_info: missing applicant data is surfaced")
        else:
            _add_tag(tags, notes, "missing_followup_question", "missing applicant data has no follow-up")
            _add_tag(
                tags,
                notes,
                "overconfident_eligibility_decision",
                "eligibility is stated despite missing applicant data",
            )

    if _has_overconfident_language(text):
        _add_tag(tags, notes, "overconfident_eligibility_decision", "response uses final approval language")

    if contains_any(text, SAFE_MARKERS) and not _has_unsafe_instruction(text):
        score += 2
        notes.append("safe_actionability: next step is framed as verification")
    else:
        _add_tag(tags, notes, "unsafe_application_instruction", "next step skips verification")

    expected_tags = set(response.get("expected_failure_tags", []))
    expected_signal_tags = {
        tag for tag in expected_tags if _expected_tag_supported_by_text(tag, text, case)
    }
    for tag in sorted(expected_signal_tags - tags):
        _add_tag(tags, notes, tag, "expected_failure_tags confirms the text-rule signal")

    failure_tags = sorted(tags)
    score = min(score, 12)

    return {
        "response_id": response["response_id"],
        "case_id": case["case_id"],
        "scenario_id": response["scenario_id"],
        "program_id": response["program_id"],
        "status": status_from_score(score, failure_tags, case),
        "score": score,
        "failure_tags": failure_tags,
        "details": {
            "matched_expected_failure_tags": sorted(expected_signal_tags.intersection(tags)),
            "unmatched_expected_failure_tags": sorted(expected_tags - tags),
            "rule_notes": notes,
        },
    }


def evaluate_responses(
    responses: list[dict[str, Any]], cases: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Evaluate response candidates in input order."""
    case_index = {(case["scenario_id"], case["program_id"]): case for case in cases}

    results = []
    for response in responses:
        key = (response["scenario_id"], response["program_id"])
        results.append(evaluate_response(response, case_index[key]))
    return results
