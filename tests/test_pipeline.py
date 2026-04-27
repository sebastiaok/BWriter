import json
from pathlib import Path

from app.main import run_pipeline
from app.schemas.models import UserInput


def test_pipeline_saves_output_per_keyword(tmp_path: Path) -> None:
    user_input = UserInput(
        topic="테스트 주제",
        target_audience="개발자",
        tone="친근함",
        length="Short",
        product_info="테스트 솔루션",
        image_style="flat",
        thumbnail_style="bold",
        candidate_keywords=5,
        selected_keywords_count=2,
    )
    saved = run_pipeline(user_input, base_dir=tmp_path)
    assert len(saved) == 2
    for path in saved:
        assert path.exists()
        assert (path / "post.md").exists()
        assert (path / "metadata.json").exists()
        assert (path / "review-report.json").exists()
        assert (path / "images").exists()
        assert (path / "thumbnails").exists()
        report = json.loads((path / "review-report.json").read_text(encoding="utf-8"))
        assert "text_generation_mode" in report
        assert "image_size" in report
        assert "thumbnail_size" in report
