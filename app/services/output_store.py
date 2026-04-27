from __future__ import annotations

import json
import os
import shutil
from dataclasses import asdict
from datetime import date
from pathlib import Path

from app.schemas.models import FinalPackage
from app.services.media_generator import MediaGenerator
from app.services.text_utils import slugify


class OutputStore:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.media = MediaGenerator()

    def save(self, package: FinalPackage) -> Path:
        image_size = os.getenv("OPENAI_IMAGE_SIZE", "1024x1024")
        thumbnail_size = os.getenv("OPENAI_THUMBNAIL_SIZE", "1536x1024")
        generation_failures: list[str] = []

        day = date.today().isoformat()
        keyword_slug = slugify(package.keyword)
        root = self.base_dir / "Output" / f"{day}_{keyword_slug}"
        if root.exists():
            shutil.rmtree(root)
        images_dir = root / "images"
        thumbs_dir = root / "thumbnails"
        images_dir.mkdir(parents=True, exist_ok=True)
        thumbs_dir.mkdir(parents=True, exist_ok=True)

        if package.post:
            (root / "post.md").write_text(package.post.markdown, encoding="utf-8")
        if package.brief:
            brief_text = (
                f"# {package.brief.title}\n\n"
                f"- keyword: {package.brief.keyword}\n"
                f"- persona: {package.brief.persona}\n"
                f"- goal: {package.brief.goal}\n"
                f"- unique_angle: {package.brief.unique_angle}\n\n"
                "## sections\n"
                + "\n".join([f"- {s}" for s in package.brief.sections])
                + "\n"
            )
            (root / "content-brief.md").write_text(brief_text, encoding="utf-8")

        for image in package.images:
            image_bytes = self.media.generate_png(image.prompt, size=image_size)
            (images_dir / image.file_name).write_bytes(image_bytes)
            if self.media.last_used_fallback:
                generation_failures.append(
                    f"image:{image.file_name} fallback used ({self.media.last_error})"
                )
            (images_dir / f"{Path(image.file_name).stem}.meta.txt").write_text(
                f"ALT={image.alt_text}\nSECTION={image.section}\nPROMPT={image.prompt}\n",
                encoding="utf-8",
            )

        if package.thumbnail:
            for name in package.thumbnail.variants:
                thumb_prompt = (
                    f"블로그 썸네일 배너, 문구 '{package.thumbnail.copy}', "
                    "클릭 유도형 구성, 고대비 컬러, 가독성 높은 타이포그래피"
                )
                thumb_bytes = self.media.generate_png(thumb_prompt, size=thumbnail_size)
                (thumbs_dir / name).write_bytes(thumb_bytes)
                if self.media.last_used_fallback:
                    generation_failures.append(
                        f"thumbnail:{name} fallback used ({self.media.last_error})"
                    )
                (thumbs_dir / f"{Path(name).stem}.meta.txt").write_text(
                    f"THUMBNAIL_COPY={package.thumbnail.copy}\nSTYLE_VARIANT={name}\nPROMPT={thumb_prompt}\n",
                    encoding="utf-8",
                )

        package.review_report["image_size"] = image_size
        package.review_report["thumbnail_size"] = thumbnail_size
        package.review_report["media_api_key_present"] = str(self.media.enabled).lower()
        if generation_failures:
            package.review_report["media_generation"] = "fallback_used"
            package.review_report["media_failures"] = " | ".join(generation_failures)
        else:
            package.review_report["media_generation"] = "api_success_or_key_unchecked"

        (root / "metadata.json").write_text(
            json.dumps(package.metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (root / "review-report.json").write_text(
            json.dumps(package.review_report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (root / "package.json").write_text(
            json.dumps(asdict(package), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return root
