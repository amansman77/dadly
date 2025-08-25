# DEVELOPMENT.md
**Dadly 프로젝트 개발 가이드**

## 프로젝트 구조

```plaintext
dadly/
 ├── app/                 # Streamlit 프론트엔드
 │   ├── main.py
 │   ├── pages/           # 페이지 단위 구성
 │   └── components/      # UI 컴포넌트
 │
 ├── backend/             # FastAPI 백엔드
 │   ├── main.py
 │   ├── api/             # 엔드포인트 모듈
 │   ├── models/          # DB 모델 정의
 │   ├── services/        # 비즈니스 로직, LangChain 파이프라인
 │   └── workers/         # 비동기 잡 (Cloud Tasks)
 │
 ├── infra/               # IaC, 배포 스크립트
 │   ├── Dockerfile.api
 │   ├── Dockerfile.app
 │   └── github-actions/  # CI/CD 워크플로우
 │
 ├── docs/                # 아키텍처/설계 문서
 │
 └── DEVELOPMENT.md
````

## 기술 스택

* **Frontend**: Streamlit
* **Backend**: FastAPI
* **LLM Layer**: LangChain + OpenAI
* **Vector DB**: Qdrant Cloud
* **Database**: Supabase (Postgres)
* **Storage**: Cloudflare R2
* **Auth**: Supabase Auth
* **Observability**: LangSmith + Cloud Logging
* **Deployment**: GCP Cloud Run

## 로컬 개발 환경

### 1. 필수 도구

* Python 3.11+
* Docker & Docker Compose
* Supabase CLI (옵션: 로컬 테스트 시)

### 2. 환경 변수 설정

루트 디렉토리에 `.env` 파일 생성:

```ini
# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_KEY=xxx

# OpenAI
OPENAI_API_KEY=sk-...

# Qdrant
QDRANT_URL=https://xxx.qdrant.cloud
QDRANT_API_KEY=xxx

# Cloudflare R2
R2_ENDPOINT=https://<accountid>.r2.cloudflarestorage.com
R2_ACCESS_KEY=xxx
R2_SECRET_KEY=xxx
R2_BUCKET=dadly

# LangSmith
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=xxx
LANGCHAIN_PROJECT=dadly
```

## 실행 방법

### 1. 백엔드 (FastAPI)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

* API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
* 주요 엔드포인트:

  * `POST /api/entries`
  * `GET /api/entries`
  * `POST /api/search`
  * `POST /api/time-capsules`

### 2. 프론트엔드 (Streamlit)

```bash
cd app
streamlit run main.py
```

* 기본 실행 URL: [http://localhost:8501](http://localhost:8501)

### 3. 로컬 Docker 실행 (통합)

```bash
docker-compose up --build
```

## 데이터 흐름 (MVP)

1. **기록 업로드**

   * 사용자가 텍스트/이미지/오디오 업로드
   * 메타데이터는 Supabase DB 저장
   * 파일은 Cloudflare R2 업로드

2. **AI 처리**

   * FastAPI Worker가 LangChain 파이프라인 실행
   * 요약/태깅/임베딩 생성 → Qdrant 저장
   * 결과는 `entry_insights` 테이블에 반영

3. **검색**

   * 질의 → 임베딩 → Qdrant 검색 → 컨텍스트 기반 요약
   * 결과 + 출처(entry\_id, snippet) 반환

4. **타임캡슐**

   * 메시지 + 개봉일 DB 저장
   * 개봉일 도달 시 클라이언트에서 열람 가능

## 테스트

* 단위 테스트: `pytest`
* E2E 테스트: Cypress (Streamlit UI) 예정
* LangChain 프롬프트: LangSmith Experiments 활용

## 보안 모범 사례

* Supabase RLS(Row Level Security) → 사용자 데이터 격리
* Cloudflare R2: 프라이빗 버킷 + 사전서명 URL
* OpenAI/Qdrant API Key는 **백엔드에서만** 사용
* 비밀키는 `.env` 대신 **Secret Manager**를 통해 주입 (운영 시)

## 배포 (Cloud Run)

### 빌드 & 푸시

```bash
# FastAPI
docker build -t asia-northeast3-docker.pkg.dev/<PROJECT_ID>/dadly/fastapi:v1 -f infra/Dockerfile.api .
docker push asia-northeast3-docker.pkg.dev/<PROJECT_ID>/dadly/fastapi:v1

# Streamlit
docker build -t asia-northeast3-docker.pkg.dev/<PROJECT_ID>/dadly/app:v1 -f infra/Dockerfile.app .
docker push asia-northeast3-docker.pkg.dev/<PROJECT_ID>/dadly/app:v1
```

### 배포

```bash
gcloud run deploy dadly-api \
  --image=asia-northeast3-docker.pkg.dev/<PROJECT_ID>/dadly/fastapi:v1 \
  --region=asia-northeast3 --platform=managed --allow-unauthenticated

gcloud run deploy dadly-app \
  --image=asia-northeast3-docker.pkg.dev/<PROJECT_ID>/dadly/app:v1 \
  --region=asia-northeast3 --platform=managed --allow-unauthenticated
```

## 향후 작업

* [ ] Cloud Tasks 기반 비동기 잡 처리
* [ ] Whisper 기반 오디오 전사 추가
* [ ] 감정 히트맵 분석 기능
* [ ] 가족 공유/코멘트 기능
