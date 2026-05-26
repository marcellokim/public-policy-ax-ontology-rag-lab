# Interview Defense Pack

## Is This Actual Government-Service Evaluation?

아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. 이 프로젝트는 공개 문서 기반 개인 PoC입니다. 정부 또는 공공기관의 운영 시스템을 테스트하거나 성능을 측정한 것이 아니라, 공개 정책자금 문서를 작은 도메인 모델과 평가셋으로 재구성했습니다. 이 boundary를 먼저 말해야 신뢰가 생깁니다.

## Is This Really RAG Without An LLM API?

Phase 1에서는 RAG generation이 아니라 RAG evaluation design에 초점을 뒀습니다. 검색된 근거를 바탕으로 생성된 답변이 있다고 가정했을 때, 어떤 answer requirements와 source evidence를 만족해야 하는지 검증합니다. 그래서 LLM API를 호출하지 않아도 평가셋, failure tag, report는 의미가 있습니다. `llm_adapter.py`는 Phase 2 연동 경계를 보여주는 dry-run 모듈입니다.

## Why No Vector DB?

vector DB를 넣으면 그럴듯해 보이지만, 이번 프로젝트의 핵심 리스크는 retrieval infrastructure가 아니라 도메인 조건 누락입니다. 정책자금 안내에서는 제외조건, 예외규칙, 서류, 신청 방식이 빠지는 순간 위험합니다. 그래서 먼저 구조화된 JSON, deterministic case builder, rule-based evaluator를 만들었습니다. 다음 단계에서는 vector DB를 붙여 검색 결과가 이 평가 기준을 통과하는지 검증할 수 있습니다.

## Why JSON Instead Of RDF/OWL?

RDF/OWL을 쓰지 않은 이유는 PoC 단계에서 검증 가능성과 설명 가능성을 우선했기 때문입니다. JSON schema는 면접관이 바로 읽을 수 있고, unittest로 source mapping과 relation consistency를 검증할 수 있습니다. "정식 ontology platform을 구축했다"가 아니라 "ontology-like domain structuring을 구현했다"고 말해야 합니다.

## What Did You Understand And Own?

제가 직접 설명해야 할 핵심은 네 가지입니다. 첫째, 정책자금 도메인의 조건/제외/예외 구조입니다. 둘째, 왜 쉬운 eligible case만으로는 RAG 평가가 부족한지입니다. 셋째, failure tag가 고객 업무 리스크를 어떻게 드러내는지입니다. 넷째, 실제 정책자금 신청 자동화가 아닙니다라는 boundary입니다. 이 네 가지를 코드와 문서로 연결해 설명하면 됩니다.

## What Would You Build Next?

다음 단계는 공식 문서 chunking, retrieval comparison, LLM response generation, human review loop, dashboard입니다. 다만 모든 확장은 기본 원칙을 유지해야 합니다. 개인정보를 넣지 않고, 공식 근거를 남기고, 생성 답변은 evaluator와 사람 검토를 통과해야 하며, 실제 신청 승인처럼 단정하지 않아야 합니다.
