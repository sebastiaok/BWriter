# BWriter: 블로그 자동 글쓰기 에이전트

키워드 발굴부터 본문/이미지/썸네일 생성, SEO 검수, 글별 `Output` 저장까지 자동화하는 프로젝트입니다.

## 주요 기능
- `keyword-hunter`로 키워드 후보 생성
- 선택 키워드 수만큼 `topic-orchestrator` 병렬 기획
- 본문(`seo-blog-writer`) + 본문 이미지(`image-generator`) + 썸네일(`thumbnail-creator`) 생성
- `seo-optimizer`로 메타데이터/검수 리포트 생성
- 결과물을 글별 폴더로 저장: `Output/{date}_{keyword}/...`
- Streamlit 화면에서 입력/실행/결과 확인 + 개별/전체 ZIP 다운로드

## 현재 프로젝트 구조
```text
BWriter/
  app/
    agents/
      keyword_hunter.py
      topic_orchestrator.py
      seo_blog_writer.py
      image_generator.py
      thumbnail_creator.py
      seo_optimizer.py
    services/
      env_loader.py
      llm_client.py
      media_generator.py
      output_store.py
      text_utils.py
    schemas/
      models.py
    main.py
  skills/
    keyword-hunter.md
    topic-orchestrator.md
    seo-blog-writer.md
    image-generator.md
    thumbnail-creator.md
    seo-optimizer.md
  Output/
    {date}_{keyword}/
      post.md
      content-brief.md
      metadata.json
      review-report.json
      package.json
      images/*.png
      thumbnails/*.png
  streamlit_app.py
  .env
  .env.example
  requirements.txt
  tests/test_pipeline.py
```

## 환경 변수
`.env` 또는 `.env.example` 기준:

```env
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_DISABLE_PROXY=false
OPENAI_TEXT_MODEL=gpt-4o-mini
OPENAI_IMAGE_MODEL=gpt-image-1
OPENAI_IMAGE_SIZE=1024x1024
OPENAI_THUMBNAIL_SIZE=1536x1024
```

추가로 엔드포인트를 지정하려면 아래 둘 중 하나를 사용합니다.

```env
OPENAI_BASE_URL=https://api.openai.com/v1
# 또는
OPENAI_ENDPOINT=https://<your-endpoint>
```

프록시 경로가 문제일 때는 아래 옵션을 사용하세요.

```env
OPENAI_DISABLE_PROXY=true
```

- `OPENAI_API_KEY`가 없으면 텍스트/이미지는 fallback 모드로 동작합니다.
- fallback 여부와 오류는 `review-report.json`에 기록됩니다.

## 설치
`BWriter` 폴더에서 실행:

```bash
pip install -r requirements.txt
```

## 실행 방법
### 1) CLI 파이프라인 실행
`BWriter` 폴더에서:

```bash
python -m app.main
```

또는 상위 폴더에서:

```bash
PYTHONPATH="/Users/a05034/Documents/Y. AI Bootcamp/BWriter" python3 "/Users/a05034/Documents/Y. AI Bootcamp/BWriter/app/main.py"
```

실행 후 `Output/{date}_{keyword}` 폴더들이 생성됩니다.

### 2) Streamlit UI 실행
`BWriter` 폴더에서:

```bash
streamlit run streamlit_app.py
```

UI에서 가능한 작업:
- 사용자 입력값 설정 후 에이전트 실행
- 생성된 본문/브리프/메타데이터/검수 리포트 확인
- 본문 이미지/썸네일 미리보기
- 개별 결과 ZIP 다운로드
- 전체 Output ZIP 다운로드

## 스크린샷
아래 경로에 이미지를 추가하면 README에서 바로 확인할 수 있습니다.

- `BWriter/docs/screenshots/01-input-form.png`
- `BWriter/docs/screenshots/02-result-preview.png`
- `BWriter/docs/screenshots/03-zip-download.png`

![입력 화면](docs/screenshots/01-input-form.png)
![결과 미리보기](docs/screenshots/02-result-preview.png)
![ZIP 다운로드](docs/screenshots/03-zip-download.png)

## 테스트
```bash
pytest -q
```

## 참고
- 파이프라인 진입점: `app/main.py`의 `run_pipeline()`
- 결과 저장 로직: `app/services/output_store.py`
- UI: `streamlit_app.py`
