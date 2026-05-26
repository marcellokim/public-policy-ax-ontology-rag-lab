"""Optional dry-run LLM adapter.

The default project path never calls external APIs. This module documents the
future integration boundary and provides deterministic sample behavior.
"""

from __future__ import annotations


def build_prompt(question: str, source_ids: list[str]) -> str:
    sources = ", ".join(source_ids)
    return (
        "당신은 공개 정책자금 문서 기반 안내 응답 초안을 작성합니다.\n"
        "실제 신청 승인처럼 단정하지 마세요.\n"
        "개인정보를 요구하지 마세요.\n"
        f"질문: {question}\n"
        f"사용 가능한 근거 source_id: {sources}\n"
        "답변에는 판단, 근거, 빠진 정보, 안전한 다음 행동을 포함하세요."
    )


def generate_sample_response(question: str, source_ids: list[str]) -> str:
    prompt = build_prompt(question, source_ids)
    return (
        "샘플 응답: 이 응답은 외부 LLM API를 호출하지 않았습니다. "
        "실제 연동 전에는 아래 prompt를 사용하고, 생성 결과는 evaluator로 검증해야 합니다.\n\n"
        f"{prompt}"
    )
