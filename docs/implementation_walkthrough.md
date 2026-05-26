# Implementation Walkthrough

## make demo Overview

`make demo`는 포트폴리오의 재현 가능한 실행 경로다. 실행 순서는 `validate-data`, `validate-ontology`, `build-cases`, `evaluate`, `report`다. 이 순서가 중요한 이유는 생성형 AI 프로젝트를 말할 때 흔히 결과 화면부터 보여주지만, 정책 안내 도메인에서는 원천 데이터와 조건 구조가 먼저 검증되어야 하기 때문이다. 이 프로젝트는 공개 문서 기반이며, 실행 중 외부 네트워크나 API key를 요구하지 않는다.

## Step 1: Data Validation

`data_io.py`는 public record, fund program, applicant scenario, response candidate를 검증한다. 특히 private field 이름을 막고, 합성 시나리오에는 `data_classification`, `is_synthetic`, `contains_personal_data`를 요구한다. 이 검증 덕분에 포트폴리오 설명에서 개인정보를 쓰지 않았다고 말할 수 있다. 단순 JSON load가 아니라 지원서 리스크를 줄이는 방어 코드다.

## Step 2: Ontology Validation

`ontology.py`는 schema의 concept, relation, source mapping이 서로 맞는지 확인한다. 프로그램 안의 조건, 제외, 예외, 문서, 신청기간, 한도, 금리 항목이 존재하는 source_id와 연결되어야 한다. 이 단계는 ontology-like라는 표현을 방어한다. RDF/OWL을 쓰지는 않았지만, 개념과 관계, 근거 연결을 명시적으로 검증하기 때문이다.

## Step 3: Evaluation Case Build

`case_builder.py`는 8개 프로그램과 5개 시나리오를 조합해 40개 평가 케이스를 만든다. 케이스에는 질문, answer requirements, expected source IDs, missing fields, expected channel이 들어간다. 좋은 케이스는 답변 생성을 위한 프롬프트가 아니라 평가 기준이다. 특히 missing information과 excluded sector 케이스를 넣어 쉬운 성공 사례에만 맞춘 평가를 피했다.

## Step 4: Response Evaluation

`evaluator.py`는 후보 응답을 점수와 failure tag로 평가한다. `pass`는 failure tag가 없고 점수가 충분할 때만 나온다. "확정할 수 없습니다" 같은 안전한 유보 표현은 penalize하지 않고, "바로 신청하면 됩니다" 같은 과한 행동 지시는 unsafe로 잡는다. 이 차이가 프로젝트의 핵심 이해 포인트다.

## Step 5: Report Generation

`reporting.py`는 결과 요약, failure tag 분포, 위험 응답 예시, AX service implication을 Markdown으로 만든다. 보고서는 기술 데모가 아니라 컨설팅 산출물처럼 읽히도록 설계했다. 고객 업무 담당자에게 어떤 답변 유형이 위험하고 어떤 조건을 보강해야 하는지 보여주는 형식이다.

## How To Debug A Failed Run

데이터 오류는 `data/raw/*.json`의 필수 필드와 source_id를 먼저 본다. ontology 오류는 `ontology_schema.json`의 concept_id와 program field의 source_ids를 맞춘다. evaluator 오류는 `tests/test_evaluator.py`의 expected_status와 response text를 비교한다. 보고서 오류는 `make clean` 후 `make demo`를 다시 실행해 generated file이 새로 만들어졌는지 확인한다.

## Boundary

이 walkthrough는 공개 문서 기반 개인 PoC의 로컬 실행 과정을 설명한다. 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. `make demo`는 샘플 데이터를 검증하고 보고서를 만드는 명령이며, 실제 신청서 제출, 실시간 크롤링, 외부 LLM 호출, 공공기관 운영 시스템 평가를 수행하지 않는다.
