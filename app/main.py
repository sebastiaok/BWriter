from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from app.agents.image_generator import ImageGeneratorAgent
from app.agents.keyword_hunter import KeywordHunterAgent
from app.agents.seo_blog_writer import SeoBlogWriterAgent
from app.agents.seo_optimizer import SeoOptimizerAgent
from app.agents.thumbnail_creator import ThumbnailCreatorAgent
from app.agents.topic_orchestrator import TopicOrchestratorAgent
from app.schemas.models import FinalPackage, UserInput
from app.services.env_loader import load_project_env
from app.services.output_store import OutputStore


def run_pipeline(user_input: UserInput, base_dir: Path | None = None) -> list[Path]:
    base_dir = base_dir or Path.cwd()
    load_project_env(base_dir)
    store = OutputStore(base_dir)

    keyword_hunter = KeywordHunterAgent()
    topic_orchestrator = TopicOrchestratorAgent()
    writer = SeoBlogWriterAgent()
    image_agent = ImageGeneratorAgent()
    thumbnail_agent = ThumbnailCreatorAgent()
    optimizer = SeoOptimizerAgent()

    bundles = keyword_hunter.run(user_input)
    selected = bundles[: user_input.selected_keywords_count]

    with ThreadPoolExecutor(max_workers=max(1, len(selected))) as pool:
        briefs = list(pool.map(lambda b: topic_orchestrator.run(b, user_input), selected))

    saved_paths: list[Path] = []
    for brief in briefs:
        post = writer.run(brief, user_input)
        with ThreadPoolExecutor(max_workers=2) as pool:
            images_future = pool.submit(image_agent.run, brief, user_input)
            thumb_future = pool.submit(thumbnail_agent.run, brief, user_input)
            images = images_future.result()
            thumbnail = thumb_future.result()

        metadata, review = optimizer.run(brief, post, images, thumbnail)
        review["text_generation_mode"] = writer.last_generation_mode
        review["text_api_key_present"] = str(writer.llm_client.enabled).lower()
        if writer.last_error:
            review["text_generation_error"] = writer.last_error
        package = FinalPackage(
            keyword=brief.keyword,
            brief=brief,
            post=post,
            images=images,
            thumbnail=thumbnail,
            metadata=metadata,
            review_report=review,
        )
        saved_paths.append(store.save(package))
    return saved_paths


if __name__ == "__main__":
    demo_input = UserInput(
        topic="블로그 자동 글쓰기",
        target_audience="마케터",
        tone="전문적",
        length="Medium",
        product_info="AI 콘텐츠 자동화 솔루션",
        image_style="미니멀 일러스트",
        thumbnail_style="정보형",
        candidate_keywords=10,
        selected_keywords_count=3,
    )
    paths = run_pipeline(demo_input, base_dir=Path(__file__).resolve().parents[1])
    print("Saved outputs:")
    for path in paths:
        print(f"- {path}")
