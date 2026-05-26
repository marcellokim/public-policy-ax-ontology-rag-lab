import os
import unittest

from policy_ax.llm_adapter import build_prompt, generate_sample_response


class LLMAdapterTests(unittest.TestCase):
    def test_build_prompt_contains_question_and_boundary(self):
        prompt = build_prompt("정책자금 가능 여부를 알려주세요.", ["src_semas_fund_overview"])
        self.assertIn("정책자금 가능 여부", prompt)
        self.assertIn("src_semas_fund_overview", prompt)
        self.assertIn("실제 신청 승인처럼 단정하지 마세요", prompt)

    def test_sample_response_requires_no_api_key(self):
        os.environ.pop("OPENAI_API_KEY", None)
        response = generate_sample_response("질문", ["src"])
        self.assertIn("샘플 응답", response)
        self.assertIn("외부 LLM API를 호출하지 않았습니다", response)


if __name__ == "__main__":
    unittest.main()
