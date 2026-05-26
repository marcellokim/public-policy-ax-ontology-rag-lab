# Evaluator Logic Notes

## Rubric Overview

Evaluator는 응답 후보를 여섯 축으로 본다. eligibility, exclusion/exception, evidence grounding, application guidance, uncertainty handling, safe actionability다. 점수는 12점 만점이지만 점수만으로 통과시키지 않는다. failure tag가 있으면 pass가 되지 않는다. 정책 안내 도메인에서는 고득점처럼 보이는 답변도 제외조건이나 근거를 빼면 실무적으로 위험하기 때문이다.

## Failure Tag Meaning

`missing_eligibility_condition`은 자격요건 자체가 약한 답변이다. `missing_exclusion_check`는 제외조건을 확인하지 않은 답변이다. `unsupported_claim`은 근거 없이 단정하거나 "대체로 비슷"처럼 부정확한 일반화를 하는 답변이다. `overconfident_eligibility_decision`은 실제 심사나 공식 확인이 필요한데도 가능 여부를 확정하는 답변이다. `unsafe_application_instruction`은 바로 신청하라는 식으로 검증 단계를 생략하는 답변이다.

## Why Missing Exclusion Is High Risk

제외조건 누락은 단순 정보 누락보다 위험하다. 사용자가 조건 일부를 만족하더라도 제외업종이나 휴폐업 상태, 체납 여부가 있으면 안내가 달라질 수 있다. 그래서 제외업종 합성 시나리오에서 `missing_exclusion_check`가 있으면 더 강한 실패로 처리한다. 이 판단은 서비스 기획 측면에서 false positive를 줄이기 위한 것이다.

## Why Unsupported Claims Cap Status

근거 없는 주장은 자연스러운 문장이어도 운영 관점에서는 검토 대상이다. 이 프로젝트는 source_id나 근거 표현이 없는 응답에 `missing_source`를 붙이고, 단정형 표현이 섞이면 `unsupported_claim`과 `overconfident_eligibility_decision`으로 잡는다. `pass`는 좋은 문체가 아니라 근거, 조건, 안전한 다음 행동이 함께 있을 때만 허용한다.

## Example Walkthrough

`rsp_good_missing_info`는 상시근로자 수가 빠진 시나리오에 대해 "확정할 수 없습니다"라고 말하고 추가 확인을 요구한다. 이 표현은 소극적인 답변이 아니라 안전한 답변이다. 반면 `rsp_overconfident_missing_info`는 빠진 정보가 있는데도 대상이라고 단정하기 때문에 failure tag가 붙는다. 이 차이를 이해하면 evaluator의 설계 의도를 설명할 수 있다.

## Known Limits

현재 evaluator는 rule-based다. 문장 변형이 많아지면 keyword 방식의 한계가 생긴다. 실제 LLM 응답 평가로 확장하려면 semantic similarity, structured extraction, human review sample을 함께 붙여야 한다. 하지만 Phase 1에서는 rule을 명확히 드러내는 편이 면접 방어에 유리하다. 무엇을 위험으로 정의했는지 코드와 테스트로 설명할 수 있기 때문이다.

## Boundary

이 evaluator는 공개 문서 기반 개인 PoC의 샘플 응답 후보를 점검한다. 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. `status`와 `score`는 실제 신청 가능성, 실제 정부 서비스 품질, 실제 고객 운영 AI 개선 결과를 뜻하지 않는다. 면접에서는 failure tag 설계와 위험 답변 분류 범위까지만 설명한다.
