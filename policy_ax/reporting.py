"""Markdown reporting for policy AX PoC evaluation results."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any


def summarize_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts = Counter(result["status"] for result in results)
    tag_counts = Counter(tag for result in results for tag in result["failure_tags"])
    return {
        "responses": len(results),
        "status_counts": dict(sorted(status_counts.items())),
        "failure_tags": dict(sorted(tag_counts.items())),
    }


def _format_failure_tags(tags: list[str]) -> str:
    if not tags:
        return "`none`"
    return ", ".join(f"`{tag}`" for tag in tags)


def write_report(path: Path, cases: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    summary = summarize_results(results)
    risky = [result for result in results if result["failure_tags"]][:5]
    lines = [
        "# Public Policy AX Ontology-RAG PoC Report",
        "",
        "## Not a Government Service Evaluation",
        "",
        "이 리포트는 공개 문서 기반 개인 PoC 결과입니다. 실제 정부/소진공 서비스 평가가 아니며, 실제 정책자금 신청 자동화가 아닙니다.",
        "",
        "## Summary",
        "",
        f"- Evaluation cases: {len(cases)}",
        f"- Response candidates: {summary['responses']}",
        f"- Status counts: {summary['status_counts']}",
        "",
        "## Failure Tag Distribution",
        "",
    ]
    for tag, count in summary["failure_tags"].items():
        lines.append(f"- `{tag}`: {count}")
    lines.extend(["", "## Risky Response Examples", ""])
    for result in risky:
        notes = result.get("details", {}).get("rule_notes", [])
        lines.extend(
            [
                f"### {result['response_id']}",
                "",
                f"- Status: `{result['status']}`",
                f"- Score: `{result['score']}`",
                f"- Failure tags: {_format_failure_tags(result['failure_tags'])}",
                f"- Case: `{result['case_id']}`",
                f"- Rule note: {notes[0] if notes else 'n/a'}",
                "",
            ]
        )
    lines.extend(
        [
            "## AX Service Implications",
            "",
            "- Policy-fund guidance needs explicit eligibility, exclusion, exception, document, timing, and source requirements.",
            "- RAG evaluation sets should include missing-information and excluded-sector scenarios, not only easy eligible cases.",
            "- The safest answer pattern is judgment boundary, reason, missing information, source evidence, and official next step.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
