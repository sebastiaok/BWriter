from __future__ import annotations

from app.schemas.models import ContentBrief, ThumbnailAsset, UserInput
from app.services.text_utils import slugify


class ThumbnailCreatorAgent:
    def run(self, brief: ContentBrief, user_input: UserInput) -> ThumbnailAsset:
        base = slugify(brief.keyword)
        variants = [f"{base}-thumb-v1.png", f"{base}-thumb-v2.png"]
        copy = f"{brief.keyword} 핵심만 5분 정리"
        return ThumbnailAsset(keyword=brief.keyword, copy=copy, variants=variants)
