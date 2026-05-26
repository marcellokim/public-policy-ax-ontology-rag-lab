# AX Consulting Talk Track

## 20-Second Version

공개 정책자금 문서를 자격요건, 제외조건, 예외규칙, 근거 출처, 신청 안내 요소로 나누고, RAG 답변 후보가 조건과 근거를 빠뜨리는지 failure tag로 검증하는 PoC를 만들었습니다. 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. 핵심은 고객 업무 지식을 AI 답변 검증 기준으로 바꾸는 과정입니다.

## Two-Minute Version

정책자금 안내는 사용자가 보기에는 "가능한가요" 한 문장이지만, 실제로는 업종, 상시근로자 수, 제외업종, 교육 이수, 신청 방식, 서류, 접수기간, 금리와 한도를 함께 확인해야 합니다. 저는 이 구조를 ontology-like schema로 나누고, 프로그램과 합성 시나리오를 조합해 40개 평가 케이스를 만들었습니다. 이후 응답 후보 12개를 evaluator로 검증해 missing exclusion, unsupported claim, overconfident decision 같은 failure tag를 붙였습니다. 결과는 PoC report로 만들었습니다.

## Customer Pain Point

고객은 AI가 답을 빨리 하는 것보다 틀리면 안 되는 조건을 놓치지 않는 것을 원한다. 특히 정책, 금융, 공공 도메인은 답변이 자연스러워도 근거가 없거나 예외를 놓치면 위험하다. 따라서 AX 컨설팅에서는 모델 선택보다 먼저 업무 판단 구조, 예외, 검증 기준을 고객과 합의해야 한다.

## Domain Knowledge Structure

이 프로젝트의 domain knowledge는 자금 프로그램, eligibility, exclusion, exception, required document, evidence source로 나뉜다. 이 구조를 통해 업무 담당자가 "이 답변은 어떤 조건을 근거로 했는가", "어떤 예외를 놓쳤는가", "어떤 source_id가 필요한가"를 확인할 수 있다.

## RAG Evaluation Set

RAG 평가셋은 쉬운 정답 케이스만 있으면 안 된다. 그래서 missing information scenario와 excluded sector scenario를 넣었다. 이 케이스들은 모델이 자신 있게 틀리는지 확인하는 용도다. NAVER Cloud Enterprise AX 직무에서 중요한 것은 바로 이런 고객 업무별 검증 기준을 설계하는 능력이다.

## PoC Report

보고서는 failure tag 분포와 위험 응답 예시를 담는다. 이 형태는 기술자만 보는 로그가 아니라 고객과 논의할 수 있는 컨설팅 산출물이다. 어떤 조건을 보강해야 하는지, 어떤 답변을 배포 전에 막아야 하는지, 어떤 source evidence가 필요한지 대화할 수 있다.

## NAVER Cloud Connection

공고는 Ontology, RAG, LLM을 활용한 Enterprise AX 서비스 기획과 PoC 지원을 요구한다. 이 포트폴리오는 그 업무를 작은 도메인으로 재현한다. "모델을 붙였다"가 아니라 "도메인 구조, 평가셋, 실패 유형, PoC report를 설계했다"는 점이 직무 연결 포인트다.

## Boundary

이 talk track은 공개 문서 기반 개인 PoC를 설명하기 위한 면접 자료다. 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. 고객 데이터, 개인정보, 공공기관 내부자료를 사용했다고 말하지 않는다. 면접에서는 도메인 구조화와 평가 기준 설계까지만 주장한다.
