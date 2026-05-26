# Public Policy AX Ontology-RAG PoC Lab

Public Policy AX Ontology-RAG PoC Lab is a deterministic Python project that turns public small-business policy-fund documents into an ontology-like domain model, RAG evaluation cases, response-quality failure tags, and a consulting-style PoC report.

It is built for portfolio review: no external API key, no database, no live crawling, and a single local command to regenerate and test the evidence.

## Fastest Review Path

```bash
git clone https://github.com/marcellokim/public-policy-ax-ontology-rag-lab.git
cd public-policy-ax-ontology-rag-lab
make verify
```

`make verify` removes generated files, rebuilds the demo artifacts, and runs the full test suite.

If `make` is unavailable:

```bash
python3 -m policy_ax.cli demo
python3 -m unittest discover -s tests -v
```

## What This Demonstrates

This project demonstrates:

- Public-document-based domain knowledge structuring
- Policy-fund concepts, conditions, exclusions, exceptions, documents, limits, terms, and source evidence
- RAG/LLM response evaluation cases for eligibility and application-guidance questions
- Failure tagging for missing conditions, unsupported claims, unsafe certainty, missing documents, and missing source evidence
- Consulting-style AX service design notes and owner-level study material

## Tech Stack

- Python 3, standard library only
- `unittest` for behavior and document-safety tests
- `make` as a thin local command wrapper
- JSON for curated public-source summaries, ontology-like schema, and generated evaluation cases
- Markdown for the generated PoC report and reviewer-facing notes

## What This Does Not Claim

- It is not a government or SEMAS service evaluation.
- It does not use personal data.
- It does not automate policy-fund applications.
- It does not determine actual eligibility.
- It does not use customer data or internal government data.
- It does not call an external LLM API in the default demo or tests.
- It does not include live crawling, a vector database, or a Streamlit dashboard.

## Quick Start

Run:

```bash
make verify
```

`make demo` validates curated public records, validates the ontology schema, builds evaluation cases, evaluates response candidates, and writes `reports/sample_poc_report.md`.

## Environment Variables

No environment variables are required for the default demo or tests. No API key is committed or needed.

`policy_ax/llm_adapter.py` is a dry-run boundary for a possible future LLM integration; it does not read credentials or call an external API.

## Project Structure

Structure:

```text
data/raw/                 Curated public-source records, fund programs, scenarios, and responses
data/processed/           Generated evaluation cases
ontology_schema.json      Domain concepts, relations, and relation constraints
policy_ax/                Python standard-library implementation
reports/sample_poc_report.md
docs/                     AX design note, owner guide, study pack, and interview defense
tests/                    Unit and document-safety tests
```

## Main Commands

```bash
make verify              # clean, regenerate demo artifacts, run tests
make demo                # validate data/schema, build cases, evaluate responses, write report
make validate-data       # validate curated public-source records and sample data
make validate-ontology   # validate ontology schema and source links
make test                # run unittest suite
make clean               # remove generated artifacts
```

Generated outputs:

- `data/processed/evaluation_cases.json`
- `reports/sample_poc_report.md`

## Verification

The default verification path is local, deterministic, and network-free:

```bash
make verify
```

Last local verification: 2026-05-26 KST.

```bash
make clean && make demo && make test
```

Expected result:

- Data validation passed
- Ontology validation passed
- 40 evaluation cases generated
- 12 response candidates evaluated
- `reports/sample_poc_report.md` generated
- Unit and document-safety tests passed without API keys or network access

## Portfolio Review Notes

- `docs/owner_guide.md`: file-by-file Korean owner guide for explaining the project end to end.
- `docs/implementation_walkthrough.md`: command and module walkthrough.
- `docs/interview_defense_pack.md`: safe interview answers and claim boundaries.
- `docs/ax_service_design_note.md`: Enterprise AX service-planning interpretation.

## Screenshots

No screenshots are included because this is a CLI/reporting mini lab, not a web UI. The primary review artifact is `reports/sample_poc_report.md`.

## Docker And Deployment

Docker is intentionally not included. The project has no service process, database, queue, browser, or fragile native dependency; Python 3 and `make` are enough for local review.

No deployment target is required. GitHub is the intended review surface.

## Interview-Safe Positioning

Allowed summary:

> 공개 정책자금 도메인을 자격요건, 제외조건, 예외규칙, 근거 출처, 신청 안내 요소로 구조화하고, RAG 답변이 조건과 근거를 빠뜨리지 않는지 failure tag 기반으로 검증하는 PoC를 설계했습니다.

## Boundary

이 프로젝트는 공개 문서 기반 개인 PoC입니다. 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. 개인정보, 고객 데이터, 내부자료, live crawling, vector DB, 외부 LLM API 호출은 기본 demo와 test에 포함하지 않습니다.

## License

MIT License. See `LICENSE`.
