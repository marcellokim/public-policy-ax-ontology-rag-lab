# Data Sources

This project uses curated summaries from official/public sources. It does not crawl live sites during the default demo.

| Source ID | Publisher | Title | URL | Use In Project |
| --- | --- | --- | --- | --- |
| src_mss_2026_integrated_support | 중소벤처기업부 | 2026년 소상공인 지원사업 통합 공고 | https://www.mss.go.kr/site/smba/ex/bbs/View.do?bcIdx=1064370&cbIdx=86 | Support-business context and official framing |
| src_mss_2026_policy_fund_revision | 중소벤처기업부 | 2026년 소상공인 정책자금 융자계획 변경 공고 | https://www.mss.go.kr/site/smba/ex/bbs/View.do?bcIdx=1067383&cbIdx=310&parentSeq=1067383 | Policy fund categories and updated fund evidence |
| src_semas_policy_home | 소상공인시장진흥공단 | 소상공인정책자금 공식 사이트 | https://ols.semas.or.kr/ols/man/SMAN010M/page.do | User flow, direct/proxy loan context, result lookup, certificate issuance |
| src_semas_fund_overview | 소상공인시장진흥공단 | 정책자금 한눈에보기 | https://ols.semas.or.kr/ols/man/SMAN018M/page.do | Fund names, channel, limits, terms, rates, requirements |
| src_semas_excluded_sectors | 소상공인시장진흥공단 | 정책자금 지원 제외업종 | https://ols.semas.or.kr/ols/pfa/SPFA207P/page.do | Excluded sectors and exception handling |
| src_law_small_business_criteria | 국가법령정보센터 | 소상공인기본법 및 시행령 소상공인 기준 | https://www.law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lspttninfSeq=164825 | Legal small-business definition and employee-count criteria by sector |

## Boundary

The records in `data/raw/` are curated public-source summaries for a portfolio PoC. They are not legal advice, financial advice, actual application approval, or an evaluation of a government production service.

이 프로젝트는 공개 문서 기반 개인 PoC입니다. 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. 위 source_id는 근거 추적을 위한 공개 출처 요약이며, 최신 접수 가능 여부나 실제 승인 가능성을 대신 판단하지 않습니다.
