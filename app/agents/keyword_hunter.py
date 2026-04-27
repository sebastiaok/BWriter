from __future__ import annotations

from typing import List

from app.schemas.models import KeywordBundle, UserInput


class KeywordHunterAgent:
    intents = ["정보형", "비교형", "문제해결형", "구매검토형"]

    def run(self, user_input: UserInput) -> List[KeywordBundle]:
        seed = user_input.topic.strip()
        bundles: List[KeywordBundle] = []
        for i in range(1, user_input.candidate_keywords + 1):
            keyword = f"{seed} 가이드 {i}"
            intent = self.intents[i % len(self.intents)]
            bundles.append(
                KeywordBundle(
                    topic=user_input.topic,
                    keyword=keyword,
                    matched_product=user_input.product_info,
                    search_intent=intent,
                    reason=f"{intent} 독자 니즈를 직접 해결하는 롱테일 키워드",
                )
            )
        return bundles
