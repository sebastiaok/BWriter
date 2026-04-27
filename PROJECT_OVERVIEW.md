# 블로그 자동 글쓰기 자동화 에이전트 프로젝트 개요 (구조도 반영본)

## 1) 프로젝트 목표
- 사용자 입력 1회로 키워드 발굴부터 본문/이미지/썸네일 생성, 최종 SEO 검수까지 자동화한다.
- 구조도와 동일하게 다중 오케스트레이터 병렬 실행으로 처리 속도와 품질을 동시에 확보한다.
- 산출물은 바로 게시 가능한 패키지(본문, 본문 이미지, 썸네일, 메타데이터) 형태로 제공한다.

## 2) 전체 실행 구조 (Flow)
1. `User Input`
2. `keyword-hunter.md` 실행
   - 키워드 10~20개 발굴 + 상품/주제 매칭
3. `사용자 선택`
   - 후보 중 키워드 3~5개 선택
4. `병렬 실행: topic-orchestrator.md x N`
   - 선택 키워드별로 오케스트레이터 1개씩 부여
   - 각 오케스트레이터가 기획 후 `content-briefs.md` 생성
5. `병렬 실행: 제작 Skills`
   - `seo-blog-writer.md`: 블로그 본문 작성
   - `image-generator.md`: 본문 내 이미지 생성
   - `thumbnail-creator.md`: 썸네일 배너 이미지 생성
6. `seo-optimizer.md` 최종 통합 검수/메타데이터 정리
7. 최종 산출물을 `Output` 폴더에 글별로 정리 저장 후 게시 준비 완료

## 3) 에이전트/스킬 역할 정의
### A. 탐색/선정 단계
- `keyword-hunter.md`
  - 트렌드/검색의도 기반 키워드 후보군 생성
  - 키워드-상품(또는 서비스) 연결 근거 제시

### B. 기획 단계 (병렬)
- `topic-orchestrator.md` (#1, #2, #3 ...)
  - 키워드별 독립 기획 수행
  - 독자 페르소나, 글 목표, 차별화 포인트 정의
  - 키워드별 `content-briefs.md` 생성

### C. 제작 단계 (병렬)
- `seo-blog-writer.md`
  - `content-briefs.md`를 바탕으로 SEO 본문 생성
- `image-generator.md`
  - 본문 문맥에 맞는 이미지 프롬프트 생성 및 이미지 생성
  - 섹션 매칭 정보와 ALT 초안 생성
- `thumbnail-creator.md`
  - 대표 썸네일 카피/레이아웃 생성
  - 플랫폼 노출을 고려한 배너형 썸네일 제작

### D. 통합 검수 단계
- `seo-optimizer.md`
  - 본문, 이미지, 썸네일, 메타데이터 일괄 검수
  - 제목/설명/H태그/내부링크/FAQ/ALT 텍스트 정합성 점검

## 4) 병렬 처리 원칙
- 키워드 선택 수(3~5개)만큼 `topic-orchestrator.md`를 병렬 실행한다.
- 기획 완료 후 제작 단계(`seo-blog-writer.md`, `image-generator.md`, `thumbnail-creator.md`)는 산출물 타입별 병렬 실행을 기본으로 한다.
- 병렬 처리 결과는 `seo-optimizer.md`에서 단일 게시 패키지로 통합한다.

## 5) 입출력 명세
### 입력
- 원주제/목표
- 키워드 후보 선택값(3~5개)
- 타깃 독자
- 글 톤/길이
- 상품/서비스 정보
- 이미지 스타일 가이드
- 썸네일 가이드(톤, 금지문구, 금지색상)

### 출력
- 키워드별 `content-briefs.md`
- SEO 최적화 본문 (`.md`)
- 본문 이미지 에셋 + 이미지 맵핑/ALT 데이터
- 썸네일 배너 이미지 (1~3안)
- 메타데이터 패키지(타이틀, 디스크립션, 태그, FAQ)
- 최종 검수 리포트

## 6) 폴더/파일 구조 제안 (글별 Output 저장)
```text
Bwriter/
  PROJECT_OVERVIEW.md
  briefs/
    content-briefs-keyword1.md
    content-briefs-keyword2.md
    content-briefs-keyword3.md
  Output/
    2026-04-24_keyword1/
      post.md
      content-brief.md
      metadata.json
      review-report.json
      images/
        section1.png
        section2.png
      thumbnails/
        thumb-v1.png
        thumb-v2.png
    2026-04-24_keyword2/
      post.md
      content-brief.md
      metadata.json
      review-report.json
      images/
      thumbnails/
  skills/
    keyword-hunter.md
    topic-orchestrator.md
    seo-blog-writer.md
    image-generator.md
    thumbnail-creator.md
    seo-optimizer.md
```

## 7) KPI (구조도 적용 버전)
- 키워드 후보 제안 정확도: 사용자 선택률 40% 이상
- 기획 품질: `content-briefs.md` 승인율 80% 이상
- 본문 품질: 수정 없는 1차 통과율 70% 이상
- 이미지 정합성: 본문-이미지 맥락 일치율 90% 이상
- 썸네일 성능: 기존 대비 CTR 15% 이상 개선
- End-to-End 처리 시간: 1건 10분 이내 (목표)

## 8) 운영 규칙
- 각 단계 산출물은 다음 단계의 입력 스키마를 반드시 충족해야 한다.
- 특정 병렬 노드 실패 시 해당 노드만 재실행하고, 성공 노드는 재사용한다.
- 최종 게시 전 `seo-optimizer.md` 검수 통과를 배포 게이트로 사용한다.
- 최종 단계에서 글마다 `Output/{date}_{keyword}/` 폴더를 생성해 산출물을 분리 저장한다.
- 저장 파일명은 고정 규칙(`post.md`, `metadata.json`, `review-report.json`)을 사용한다.
- 이미지/썸네일은 각 글 폴더 내부의 `images/`, `thumbnails/` 하위 폴더에 저장한다.

## 9) 구현 우선순위 (MVP -> 고도화)
1. `keyword-hunter.md` + `topic-orchestrator.md` + `seo-blog-writer.md` 기본 파이프라인
2. `image-generator.md` 연동 (본문 이미지 자동 생성)
3. `thumbnail-creator.md` 연동 (썸네일 자동 생성)
4. `seo-optimizer.md` 기반 최종 통합 검수
5. A/B 테스트 루프(썸네일/제목) 및 성능 리포팅 자동화

## 10) 완료 기준 (Definition of Done)
- 구조도에 명시된 6개 스킬/에이전트가 순서/병렬 규칙대로 실행된다.
- 키워드별 `content-briefs.md`, 본문, 본문 이미지, 썸네일, 메타데이터가 모두 생성된다.
- `seo-optimizer.md` 검수 통과 결과가 생성되고 게시 가능한 상태로 저장된다.
- 모든 결과물은 글별 `Output/{date}_{keyword}/` 폴더에 자동 정리되어 저장된다.
