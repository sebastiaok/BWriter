from __future__ import annotations

from app.schemas.models import ContentBrief, GeneratedPost, ImageAsset, ThumbnailAsset


class SeoOptimizerAgent:
    def run(
        self,
        brief: ContentBrief,
        post: GeneratedPost,
        images: list[ImageAsset],
        thumbnail: ThumbnailAsset,
    ) -> tuple[dict[str, str], dict[str, str]]:
        metadata = {
            "title": post.title[:60],
            "description": f"{brief.keyword}를 빠르게 이해하고 실행하는 방법을 정리한 글",
            "primary_keyword": brief.keyword,
            "thumbnail_copy": thumbnail.copy,
            "image_count": str(len(images)),
        }
        review = {
            "status": "pass",
            "seo": "pass",
            "readability": "pass",
            "brand_tone": "pass",
            "notes": "기본 자동 검수 통과",
        }
        return metadata, review
