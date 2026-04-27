from __future__ import annotations

from app.schemas.models import ContentBrief, KeywordBundle, UserInput


class TopicOrchestratorAgent:
    def run(self, bundle: KeywordBundle, user_input: UserInput) -> ContentBrief:
        title = f"{bundle.keyword}: {user_input.target_audience}를 위한 실전 가이드"
        return ContentBrief(
            keyword=bundle.keyword,
            title=title,
            persona=user_input.target_audience,
            goal="검색 유입 + 문제 해결 + 신뢰 확보",
            unique_angle=f"{bundle.matched_product} 관점의 적용 사례 중심 설명",
            sections=[
                f"{bundle.keyword}가 중요한 이유",
                "핵심 개념 3가지",
                "실행 단계별 체크리스트",
                "자주 하는 실수와 해결법",
                "결론 및 다음 액션",
            ],
        )
