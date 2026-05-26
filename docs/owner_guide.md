# Owner Guide

## One-Minute Explanation

Public Policy AX Ontology-RAG PoC Lab은 공개 정책자금 문서를 자격요건, 제외조건, 예외규칙, 근거 출처, 신청 안내 요소로 구조화하고, RAG/LLM 응답 후보가 조건과 근거를 빠뜨리지 않는지 평가셋과 failure tag로 검증한 개인 포트폴리오다. 핵심은 실제 LLM API 호출이 아니라 고객 업무 지식을 어떻게 평가 가능한 구조로 바꿨는지다. 면접에서는 "정책자금 안내처럼 조건 누락 리스크가 큰 도메인에서, 답변 생성보다 먼저 검증 기준을 만들었다"고 설명하면 된다.

## File-By-File Guide

`data/raw/public_policy_records.json`은 공식/공개 근거 출처 요약이다. `fund_programs.json`은 정책자금 프로그램의 조건, 제외, 문서, 기간, 한도, 금리 정보를 담는다. `applicant_scenarios.json`은 개인정보 없는 합성 신청자 시나리오다. `ontology_schema.json`은 도메인 개념과 관계를 정의한다. `case_builder.py`는 프로그램과 시나리오를 조합해 평가 케이스를 만든다. `evaluator.py`는 응답 후보를 점수와 failure tag로 평가한다. `reporting.py`는 결과를 컨설팅식 보고서로 만든다.

## What I Would Open First In An Interview

첫 번째로 `reports/sample_poc_report.md`를 열어 결과물을 보여준다. 두 번째로 `ontology_schema.json`을 열어 왜 자격요건, 제외조건, 예외규칙을 분리했는지 설명한다. 세 번째로 `policy_ax/evaluator.py`와 `tests/test_evaluator.py`를 열어 과신 답변, 근거 누락, 신청 안내 과장 표현을 어떻게 잡았는지 보여준다. 마지막으로 `docs/ax_service_design_note.md`를 열어 기술 구현을 AX 서비스 기획 언어로 연결한다.

## How The Demo Works

`make demo`는 데이터 검증, ontology 검증, 평가 케이스 생성, 응답 후보 평가, 보고서 생성을 순서대로 수행한다. 네트워크, API key, live crawling이 필요 없다. 이 점은 약점이 아니라 의도된 boundary다. 지원서에는 "실제 운영 연동"이 아니라 "도메인 구조화와 평가 설계"라고 써야 한다.

## How To Explain The Limits

실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. 실제 개인정보 기반 추천도 아니다. 이 프로젝트의 범위는 공개 문서 기반 평가셋과 failure tag 설계다. LLM API, vector DB, Streamlit dashboard는 Phase 2 후보로 남겼지만, 이번 지원에서 핵심 설득력은 현재 검증 가능한 코드와 문서에 있다.

## Forbidden Claims

금지 표현은 "실제 서비스 운영", "공식 평가", "신청 처리 자동화", "고객 데이터 기반 개선"이다. 허용 표현은 "공개 문서 기반 개인 PoC", "합성 시나리오", "RAG 평가셋", "failure tag 기반 응답 검증", "AX 서비스 기획 관점의 도메인 구조화"다. 강하게 말해야 하지만 과장하면 바로 리스크가 된다.
