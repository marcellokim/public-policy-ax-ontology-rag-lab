# Development Journal

## 2026-05-26 Design

NAVER Cloud Ontology 기반 Enterprise AX 서비스 기획 및 구축 지원 직무에 맞춰 포트폴리오 도메인을 다시 잡았다. 처음에는 실제 LLM API, vector DB, live crawling, Streamlit dashboard까지 넣을 수 있는지 검토했지만, 지원서에서 가장 강한 설득 포인트는 "고객 도메인을 구조화하고 PoC 검증 기준으로 바꾸는 능력"이라고 판단했다. 그래서 공개 정책자금 문서 기반의 ontology-like schema와 RAG evaluation set을 핵심으로 정했다.

## 2026-05-26 Implementation

구현은 Python standard library, JSON, Markdown, unittest, Makefile로 제한했다. 데이터 원천은 공식/공개 문서 요약으로 정리했고, fund program, applicant scenario, response candidate를 분리했다. 이후 ontology validation, case builder, evaluator, reporting CLI 순서로 붙였다. `make demo`는 데이터 검증부터 보고서 생성까지 한 번에 실행된다. 외부 LLM API 호출은 dry-run adapter로만 남겼다.

## Data Decisions

합성 신청자 시나리오는 개인정보를 포함하지 않는다. `data_classification`, `is_synthetic`, `contains_personal_data` 필드를 둔 이유는 면접에서 데이터 boundary를 방어하기 위해서다. 실제 신청자, 고객사, 내부 시스템, 비공개 자료는 쓰지 않았다. 공개 문서 기반 PoC라는 표현을 유지한다.

## Testing Decisions

테스트는 기능 검증과 claim safety를 모두 본다. data IO 테스트는 필수 필드와 private field를 막는다. ontology 테스트는 concept/relation/source mapping을 본다. evaluator 테스트는 expected status alignment와 pass 응답의 failure tag 부재를 확인한다. document safety 테스트는 필수 문서 존재, boundary marker, 금지 claim 부재를 확인한다.

## Verification Log

중간 검증에서 `make demo`는 40개 evaluation cases와 12개 response candidates를 처리했다. 보고서는 failure tag 분포와 위험 응답 예시를 생성했다. 최종 검증은 Task 11에서 다시 기록한다. 현재 해석은 명확하다. 이 프로젝트는 deterministic public-document-based AX PoC이며, 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다.

Command:

```bash
make clean && make demo && make test
```

Result:

- Data validation passed.
- Ontology validation passed.
- Evaluation cases generated.
- Response candidates evaluated.
- Sample PoC report generated.
- Unit and document-safety tests passed.

Interpretation:

The project can be explained as a deterministic public-document-based AX PoC. It should not be described as live policy-fund application automation, government-service evaluation, or production AI improvement.
