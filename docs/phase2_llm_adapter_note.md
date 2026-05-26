# Phase 2 LLM Adapter Note

The default demo and tests do not call external LLM APIs. This is intentional.

## Why API Calls Are Optional

- The portfolio's core claim is evaluation-set and failure-tag design, not live model generation.
- API output can drift and makes tests less deterministic.
- A key risk in policy-fund guidance is overconfident generated text, so generated answers should be reviewed by the evaluator before being used as evidence.

## Safe Integration Boundary

Future API integration must:

- Use an environment variable for API keys.
- Keep `make demo` and `make test` network-free.
- Store generated samples only after manual review.
- Never present generated text as actual government guidance.

## Boundary

This note belongs to a 공개 문서 기반 personal PoC. 실제 정책자금 신청 자동화가 아닙니다. 실제 정부/소진공 서비스 평가가 아닙니다. The default implementation does not call an external LLM API, does not run live crawling, and does not use customer or personal data. Future generated responses would still need evaluator checks and human review before any claim is made.
