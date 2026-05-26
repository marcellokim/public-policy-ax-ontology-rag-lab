# Public Policy AX Ontology-RAG PoC Report

## Not a Government Service Evaluation

이 리포트는 공개 문서 기반 개인 PoC 결과입니다. 실제 정부/소진공 서비스 평가가 아니며, 실제 정책자금 신청 자동화가 아닙니다.

## Summary

- Evaluation cases: 40
- Response candidates: 12
- Status counts: {'fail': 1, 'needs_review': 6, 'pass': 5}

## Failure Tag Distribution

- `missing_eligibility_condition`: 2
- `missing_exclusion_check`: 6
- `missing_followup_question`: 1
- `missing_required_document`: 2
- `missing_source`: 7
- `overconfident_eligibility_decision`: 2
- `unsafe_application_instruction`: 7
- `unsupported_claim`: 4
- `wrong_fund_channel`: 1

## Risky Response Examples

### rsp_missing_exclusion_credit

- Status: `needs_review`
- Score: `4`
- Failure tags: `missing_exclusion_check`, `missing_source`, `unsafe_application_instruction`
- Case: `case_scn_retail_credit_training__fund_credit_vulnerable`
- Rule note: eligibility_accuracy: partial eligibility statement

### rsp_unsupported_credit

- Status: `needs_review`
- Score: `3`
- Failure tags: `missing_eligibility_condition`, `missing_exclusion_check`, `missing_source`, `overconfident_eligibility_decision`, `unsafe_application_instruction`, `unsupported_claim`
- Case: `case_scn_retail_credit_training__fund_credit_vulnerable`
- Rule note: missing_eligibility_condition: no meaningful eligibility condition

### rsp_wrong_channel_youth

- Status: `needs_review`
- Score: `5`
- Failure tags: `missing_exclusion_check`, `missing_required_document`, `missing_source`, `unsafe_application_instruction`, `unsupported_claim`, `wrong_fund_channel`
- Case: `case_scn_youth_hiring_food_service__fund_youth_employment_linked`
- Rule note: eligibility_accuracy: partial eligibility statement

### rsp_missing_excluded_sector

- Status: `fail`
- Score: `4`
- Failure tags: `missing_exclusion_check`, `missing_source`, `unsafe_application_instruction`, `unsupported_claim`
- Case: `case_scn_real_estate_excluded__fund_general_management_stability`
- Rule note: eligibility_accuracy: partial eligibility statement

### rsp_missing_document_distress

- Status: `needs_review`
- Score: `5`
- Failure tags: `missing_exclusion_check`, `missing_required_document`, `missing_source`, `unsafe_application_instruction`
- Case: `case_scn_distress_manufacturing__fund_temporary_business_distress`
- Rule note: eligibility_accuracy: partial eligibility statement

## AX Service Implications

- Policy-fund guidance needs explicit eligibility, exclusion, exception, document, timing, and source requirements.
- RAG evaluation sets should include missing-information and excluded-sector scenarios, not only easy eligible cases.
- The safest answer pattern is judgment boundary, reason, missing information, source evidence, and official next step.
