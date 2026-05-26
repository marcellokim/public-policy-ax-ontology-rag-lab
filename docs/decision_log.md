# Decision Log

## Domain Choice

정책자금 도메인을 선택한 이유는 Enterprise AX에서 자주 나타나는 조건형 업무와 잘 맞기 때문이다. 사용자 질문은 짧지만 실제 답변에는 조건, 제외, 예외, 근거, 신청 안내가 모두 필요하다. 이 구조는 Ontology, RAG, LLM 평가의 필요성을 설명하기 좋다. 또한 중기부, 소진공, 국가법령정보센터 같은 공개 출처를 활용할 수 있어 포트폴리오 claim safety가 높다.

## No Live Crawling

live crawling은 넣지 않았다. 최신 접수 상태를 자동 반영한다고 말하려면 크롤링 안정성, 이용약관, robots, 변경 감지, 실패 처리까지 검토해야 한다. 이번 프로젝트의 목표는 크롤러가 아니라 도메인 구조화와 평가 설계다. 따라서 원천은 curated public-source summary로 제한했고, 실제 최신 확인은 공식 사이트에서 해야 한다고 문서에 남겼다.

## No Personal-Data Recommendation

개인정보 기반 추천은 제외했다. 정책자금 추천처럼 보이는 기능은 실제 개인정보, 사업자 정보, 민감한 재무 상태를 요구할 수 있다. 이번 포트폴리오는 합성 시나리오만 사용한다. `contains_personal_data`를 false로 고정하고 private field를 validation에서 막은 이유도 이 때문이다.

## No Policy-Application Automation

실제 정책자금 신청 자동화가 아닙니다. 신청 자동화는 인증, 제출서류, 법적 책임, 사용자 동의, 오류 대응, 공식 절차 준수 문제가 생긴다. 이 프로젝트는 신청을 대신하지 않고, 안내 응답이 조건과 근거를 빠뜨리는지 검증한다. 지원서에서는 이 차이를 분명히 말해야 한다.

## No Vector DB In Phase 1

vector DB는 Phase 2 후보다. Phase 1에서는 retrieval보다 evaluation criterion이 더 중요했다. 검색 인프라를 붙여도 자격요건과 제외조건을 평가하지 못하면 서비스 위험은 그대로 남는다. 그래서 먼저 deterministic case builder와 evaluator를 만들었다.

## Optional LLM Adapter Only

LLM adapter는 dry-run으로만 구현했다. 기본 demo와 test는 API key 없이 실행된다. 이 결정은 재현성을 높이고 결과 drift를 줄인다. 실제 LLM을 붙인다면 prompt, generated response, evaluator result, human review를 모두 저장해야 한다.

## JSON Schema Instead Of RDF/OWL

JSON schema를 선택한 이유는 구현 속도, 리뷰 가능성, 테스트 가능성이다. 정식 ontology platform을 도입하면 더 풍부한 추론이 가능하지만, 이번 포트폴리오의 목적은 고객 도메인을 구조화하고 평가셋으로 바꾸는 과정을 보여주는 것이다. 면접에서는 RDF/OWL 미사용을 약점으로 숨기지 말고 Phase 1 범위 결정으로 설명한다.

## Boundary

이 decision log는 공개 문서 기반 개인 PoC의 범위 결정을 기록한다. 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. 각 결정은 포트폴리오의 검증 가능성과 과장 방지를 위한 것이며, 실제 공공기관 서비스 성능 평가나 고객 데이터 기반 운영 개선을 주장하지 않는다.
