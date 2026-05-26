# Policy AX RAG Response Rubric

Each response is scored on six axes from 0 to 2.

| Axis | 0 | 1 | 2 |
| --- | --- | --- | --- |
| eligibility_accuracy | Makes wrong or unsupported eligibility judgment | Mentions some eligibility requirements but misses material requirements | Correctly handles the material eligibility requirements for the case |
| exclusion_and_exception_handling | Does not check exclusions or exceptions | Mentions exclusions but misses an applicable exception or risk | Checks exclusions and relevant exception rules |
| evidence_grounding | Gives no source ID or unsupported claim | Provides partial source grounding | Grounds material claims in official/public source IDs |
| application_guidance_completeness | Misses required channel, window, document, limit, rate, or term information | Includes partial application guidance | Includes the guidance fields required by the question |
| uncertainty_and_missing_info | Overclaims when applicant information is missing | Notes uncertainty without concrete follow-up | Identifies missing information and asks a specific follow-up question |
| safe_actionability | Gives unsafe application instruction or final approval language | Gives generic next step | Gives safe next step without pretending to approve applications |

## Status Bands

- 10-12: pass
- 7-9: needs_review
- 0-6: fail

If a response has `unsupported_claim`, `unsafe_application_instruction`, or `overconfident_eligibility_decision`, the maximum status is `needs_review`.

## Failure Tags

- `missing_eligibility_condition`
- `missing_exclusion_check`
- `missing_exception_rule`
- `wrong_fund_channel`
- `stale_or_missing_application_window`
- `missing_required_document`
- `missing_loan_limit_or_term`
- `unsupported_claim`
- `missing_source`
- `overconfident_eligibility_decision`
- `unsafe_application_instruction`
- `missing_followup_question`

## Boundary

이 rubric은 공개 문서 기반 개인 PoC의 응답 후보를 점검하기 위한 기준입니다. 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. 점수와 status는 이 저장소의 샘플 응답 품질을 비교하기 위한 내부 검증값이며, 실제 신청 자격이나 공공기관 서비스 성능을 의미하지 않습니다.
