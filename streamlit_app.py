from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import streamlit as st

from app.main import run_pipeline
from app.schemas.models import UserInput


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Output"


def build_user_input() -> UserInput:
    with st.form("blog_input_form", clear_on_submit=False):
        topic = st.text_input("주제", value="블로그 자동 글쓰기")
        target_audience = st.text_input("타깃 독자", value="마케터")
        tone = st.selectbox("글 톤", ["전문적", "친근함", "분석형"], index=0)
        length = st.selectbox("글 길이", ["Short", "Medium", "Long"], index=1)
        product_info = st.text_input("상품/서비스 정보", value="AI 콘텐츠 자동화 솔루션")
        image_style = st.text_input("이미지 스타일", value="미니멀 일러스트")
        thumbnail_style = st.text_input("썸네일 스타일", value="정보형")
        candidate_keywords = st.slider("키워드 후보 개수", min_value=5, max_value=20, value=10)
        selected_keywords_count = st.slider("선택 키워드 수", min_value=1, max_value=5, value=3)
        submitted = st.form_submit_button("에이전트 실행")

    if not submitted:
        return None  # type: ignore[return-value]

    return UserInput(
        topic=topic,
        target_audience=target_audience,
        tone=tone,
        length=length,
        product_info=product_info,
        image_style=image_style,
        thumbnail_style=thumbnail_style,
        candidate_keywords=candidate_keywords,
        selected_keywords_count=selected_keywords_count,
    )


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def make_zip_bytes(folder: Path) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in folder.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(folder)
                zf.write(file_path, arcname=str(arcname))
    buffer.seek(0)
    return buffer.read()


def render_output_folder(folder: Path) -> None:
    st.subheader(folder.name)
    zip_data = make_zip_bytes(folder)
    st.download_button(
        label="이 결과 폴더 ZIP 다운로드",
        data=zip_data,
        file_name=f"{folder.name}.zip",
        mime="application/zip",
        key=f"download-{folder.name}",
    )

    post_path = folder / "post.md"
    brief_path = folder / "content-brief.md"
    meta_path = folder / "metadata.json"
    report_path = folder / "review-report.json"
    images_dir = folder / "images"
    thumbs_dir = folder / "thumbnails"

    with st.expander("본문 미리보기", expanded=True):
        post = read_text(post_path)
        if post:
            st.markdown(post)
        else:
            st.info("본문 파일이 없습니다.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**콘텐츠 브리프**")
        brief = read_text(brief_path)
        st.text_area(
            "content-brief.md",
            value=brief if brief else "브리프 파일이 없습니다.",
            height=240,
            key=f"brief-{folder.name}",
            disabled=True,
        )
    with col2:
        st.markdown("**검수/메타데이터**")
        st.json({"metadata": read_json(meta_path), "review": read_json(report_path)})

    st.markdown("**본문 이미지**")
    image_files = sorted(images_dir.glob("*.png")) if images_dir.exists() else []
    if image_files:
        st.image([str(p) for p in image_files], caption=[p.name for p in image_files], width=240)
    else:
        st.info("이미지 파일이 없습니다.")

    st.markdown("**썸네일 이미지**")
    thumb_files = sorted(thumbs_dir.glob("*.png")) if thumbs_dir.exists() else []
    if thumb_files:
        st.image([str(p) for p in thumb_files], caption=[p.name for p in thumb_files], width=260)
    else:
        st.info("썸네일 파일이 없습니다.")


def render_saved_outputs() -> None:
    st.header("저장된 결과물")
    if not OUTPUT_DIR.exists():
        st.info("아직 생성된 Output 폴더가 없습니다.")
        return

    folders = sorted([p for p in OUTPUT_DIR.iterdir() if p.is_dir()], reverse=True)
    if not folders:
        st.info("표시할 글 결과가 없습니다.")
        return

    all_zip_data = make_zip_bytes(OUTPUT_DIR)
    st.download_button(
        label="전체 Output ZIP 다운로드",
        data=all_zip_data,
        file_name="BWriter-Output-All.zip",
        mime="application/zip",
        key="download-all-output",
    )

    selected = st.selectbox("확인할 결과 폴더 선택", options=folders, format_func=lambda p: p.name)
    render_output_folder(selected)


def main() -> None:
    st.set_page_config(page_title="BWriter Agent Console", layout="wide")
    st.title("BWriter 자동 글쓰기 에이전트")
    st.caption("사용자 입력 -> 에이전트 실행 -> Output 글별 결과 확인")

    user_input = build_user_input()
    if user_input is not None:
        with st.spinner("에이전트 실행 중입니다..."):
            saved_paths = run_pipeline(user_input=user_input, base_dir=BASE_DIR)
        st.success(f"완료: {len(saved_paths)}개 글이 생성되었습니다.")
        st.write("저장 경로")
        for path in saved_paths:
            st.code(str(path))

    render_saved_outputs()


if __name__ == "__main__":
    main()
