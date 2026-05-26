# Ontology Modeling Notes

## Why JSON Schema Instead Of RDF/OWL In Phase 1

Phase 1에서는 RDF/OWL 대신 JSON 기반 ontology-like schema를 선택했다. 이유는 지원 직무에서 보여줘야 할 핵심이 ontology tool 사용 능력 자체보다 고객 업무 지식을 개념, 관계, 근거, 평가 조건으로 나누는 사고방식이기 때문이다. JSON은 리뷰와 테스트가 쉽고, Python standard library만으로 검증할 수 있다. 면접에서는 "정식 semantic web 구현이 아니라 PoC 단계의 도메인 구조화"라고 정확히 말해야 한다.

## Concept Boundaries

주요 concept는 `PolicyFundProgram`, `EligibilityCondition`, `ExclusionCondition`, `ExceptionRule`, `RequiredDocument`, `EvidenceSource`, `ApplicantScenario`, `ResponseCandidate`, `EvaluationCase`, `FailureTag`다. 각 concept는 실제 서비스 설계에서 역할이 다르다. 프로그램은 상품 단위이고, 조건은 판단 기준이며, 근거는 설명 가능성을 만든다. FailureTag는 운영자가 위험 답변을 분류하는 언어다.

## Relation Boundaries

Relation은 program이 eligibility condition을 가지는지, exclusion condition을 가지는지, source evidence와 연결되는지, response가 case를 대상으로 하는지 같은 연결을 표현한다. 이 연결이 없으면 RAG 답변이 어떤 근거를 빠뜨렸는지 평가하기 어렵다. Relation boundary를 세우는 목적은 모델이 좋은 문장을 만들도록 하는 것이 아니라 업무 검토자가 빠진 조건을 찾을 수 있게 하는 것이다.

## Evidence Mapping

각 fund program은 top-level `source_ids`와 nested field source_ids를 가진다. 신청기간, 한도, 기간, 금리처럼 바뀔 수 있는 항목도 source_id와 묶었다. `ontology.py`는 이 source_id가 실제 public policy record에 존재하는지 확인한다. 이 구조 덕분에 보고서에서 "근거 없는 주장"과 "근거 출처가 있는 안내"를 분리할 수 있다.

## Alternatives Considered

처음부터 graph database, vector DB, RDF triple store를 붙일 수 있지만, 이번 지원 포트폴리오에서는 오히려 범위가 흐려질 수 있다. 도메인 원천과 평가 기준이 약한 상태에서 인프라를 붙이면 데모는 커져도 설명력은 약해진다. 그래서 Phase 1은 JSON, unittest, Markdown report로 좁혔다.

## What I Would Improve Next

다음 단계는 실제 검색 계층을 붙이는 것이다. public document chunk를 만들고, vector DB나 keyword retrieval을 비교한 뒤, LLM 생성 응답을 evaluator에 통과시키는 flow를 만들 수 있다. 다만 기본 demo는 계속 network-free로 유지해야 한다. 그래야 포트폴리오의 재현성과 claim boundary가 유지된다.

## Boundary

이 ontology-like 모델은 공개 문서 기반 개인 PoC를 위한 구조화 방식이다. 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. RDF/OWL 기반 운영 ontology나 공공기관 내부 지식그래프를 구축했다고 주장하지 않는다. 현재 claim은 JSON schema, source mapping, validation test로 확인되는 범위에 한정한다.
