from __future__ import annotations

from typing import List

from app.schemas.models import ContentBrief, ImageAsset, UserInput
from app.services.text_utils import slugify


class ImageGeneratorAgent:
    def run(self, brief: ContentBrief, user_input: UserInput) -> List[ImageAsset]:
        assets: List[ImageAsset] = []
        for idx, section in enumerate(brief.sections[:2], start=1):
            file_name = f"{slugify(brief.keyword)}-section{idx}.png"
            prompt = (
                f"{user_input.image_style} 스타일, 블로그 섹션 '{section}'를 설명하는 시각 자료, "
                "텍스트 최소화, 고해상도 배너 비율"
            )
            assets.append(
                ImageAsset(
                    keyword=brief.keyword,
                    section=section,
                    prompt=prompt,
                    file_name=file_name,
                    alt_text=f"{section}를 설명하는 이미지",
                )
            )
        return assets
