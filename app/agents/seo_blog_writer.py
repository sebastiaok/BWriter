from __future__ import annotations

from typing import List

from app.schemas.models import ContentBrief, GeneratedPost, UserInput
from app.services.llm_client import LlmClient


class SeoBlogWriterAgent:
    def __init__(self, llm_client: LlmClient | None = None) -> None:
        self.llm_client = llm_client or LlmClient()
        self.last_generation_mode: str = "template"
        self.last_error: str | None = None

    def run(self, brief: ContentBrief, user_input: UserInput) -> GeneratedPost:
        self.last_generation_mode = "template"
        self.last_error = None
        prompt = (
            f"다음 조건으로 한국어 SEO 블로그 글을 markdown으로 작성해줘.\n"
            f"- 제목: {brief.title}\n"
            f"- 메인 키워드: {brief.keyword}\n"
            f"- 타깃 독자: {brief.persona}\n"
            f"- 톤: {user_input.tone}\n"
            f"- 분량: {user_input.length}\n"
            f"- 섹션: {', '.join(brief.sections)}\n"
            "- 필수: H2/H3 구조, 결론, FAQ 2개\n"
        )
        llm_markdown = self.llm_client.generate_markdown(prompt)
        if llm_markdown:
            self.last_generation_mode = "llm"
            faq = [
                {"q": f"{brief.keyword}는 초보자도 가능한가요?", "a": "가능합니다. 핵심 단계를 나눠 진행하면 됩니다."},
                {"q": "어떤 지표를 먼저 봐야 하나요?", "a": "클릭률, 체류시간, 전환 관련 지표를 우선 확인하세요."},
            ]
            return GeneratedPost(keyword=brief.keyword, title=brief.title, markdown=llm_markdown, faq=faq)
        self.last_error = self.llm_client.last_error

        body: List[str] = [f"# {brief.title}", ""]
        body.append(f"> 타깃 독자: {brief.persona} | 톤: {user_input.tone} | 길이: {user_input.length}")
        body.append("")
        for idx, section in enumerate(brief.sections, start=1):
            body.append(f"## {idx}. {section}")
            body.append(
                f"{brief.keyword}를 중심으로 실제 적용 포인트를 설명합니다. "
                f"{user_input.product_info} 맥락에서 즉시 활용 가능한 실무 팁을 포함합니다."
            )
            body.append("")
        body.append("## 결론")
        body.append("핵심은 작은 단위로 실행하고 성과를 기록하며 반복 개선하는 것입니다.")
        body.append("")
        body.append("## FAQ")
        faq = [
            {"q": f"{brief.keyword}는 초보자도 가능한가요?", "a": "네, 체크리스트 중심으로 시작하면 충분합니다."},
            {"q": "성과는 얼마나 빨리 나오나요?", "a": "보통 2~4주 내 초기 지표 변화를 확인할 수 있습니다."},
        ]
        for item in faq:
            body.append(f"- **Q. {item['q']}**")
            body.append(f"  - A. {item['a']}")
        return GeneratedPost(keyword=brief.keyword, title=brief.title, markdown="\n".join(body), faq=faq)
