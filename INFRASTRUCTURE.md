
# INFRASTRUCTURE.md  
**Dadly 프로젝트 인프라 설계 및 운영 가이드**

## 아키텍처 개요

```mermaid
flowchart TD
    User[👨‍👩‍👧 User Browser] -->|Auth/Login| Streamlit
    Streamlit[Streamlit Frontend<br>Cloud Run] -->|API Call| FastAPI
    FastAPI[FastAPI Backend<br>Cloud Run] -->|JWT Verify| Supabase[(Supabase<br>Auth & Postgres)]
    FastAPI -->|Store Metadata| Supabase
    FastAPI -->|Vector Embedding| Qdrant[(Qdrant Cloud)]
    FastAPI -->|File Upload| R2[(Cloudflare R2)]
    FastAPI -->|LLM Requests| OpenAI[(OpenAI API)]
    FastAPI -->|Prompt Logs| LangSmith[(LangSmith)]
````

* **Frontend**: Streamlit (UI, 사용자 상호작용)
* **Backend API**: FastAPI (비즈니스 로직, LLM 파이프라인)
* **Database**: Supabase (Postgres + Auth)
* **VectorDB**: Qdrant Cloud (검색/임베딩)
* **Storage**: Cloudflare R2 (이미지/오디오 등 파일)
* **LLM**: OpenAI API (텍스트 요약, 태깅, 검색 응답)
* **Observability**: LangSmith + Cloud Logging
* **Deployment**: GCP Cloud Run (컨테이너)

## 데이터 관리

### Supabase (Postgres)

* **Users/Auth**: Supabase Auth (JWT 인증, 소셜 로그인 가능)
* **Entries**: 기록 원문 및 메타데이터
* **Entry Insights**: 요약/태깅/임베딩 ID 관리
* **Time Capsules**: 개봉일이 설정된 메시지

> RLS(Row Level Security) 활성화 → 사용자별 데이터 접근 제어

### Qdrant Cloud

* Collection: `entries_v1`

  * Vector Size: OpenAI Embedding 모델 크기(예: 3072)
  * Distance Metric: cosine
  * Payload: `{ entry_id, owner_id, member_id, topics, emotions }`

### Cloudflare R2

* Private bucket 사용
* 사전서명 URL(Presigned URL)로 접근 제어
* 저장 데이터: 이미지, 오디오 파일

## 보안/비밀 관리

* **GCP Secret Manager** → Cloud Run 환경 변수 주입

* 저장 대상:

  * `OPENAI_API_KEY`
  * `SUPABASE_SERVICE_KEY`
  * `QDRANT_API_KEY`
  * `R2_ACCESS_KEY`, `R2_SECRET_KEY`
  * `LANGCHAIN_API_KEY`

* **원칙**:

  * API 키는 **백엔드(FastAPI)** 에서만 사용
  * 프론트엔드(Streamlit)에는 Supabase `anon` 키만 제공

## 배포 (Cloud Run)

### FastAPI 서비스

* Memory: 1GiB / CPU: 1
* Min Instances: 0 (비용 절감)
* Max Instances: 5 (MVP 기준)
* Autoscaling: 요청 지연 80% 시 scale-out
* URL 예시: `https://dadly-api-xxxx.run.app`

### Streamlit 서비스

* Memory: 512MiB / CPU: 1
* Min Instances: 0
* Max Instances: 3
* URL 예시: `https://dadly-app-xxxx.run.app`

### CI/CD (GitHub Actions)

* main 브랜치 → Docker Build → Artifact Registry Push → Cloud Run Deploy
* 환경변수는 GitHub Secrets → GCP Secret Manager 연동

## 비동기 처리 (확장 시)

* **Cloud Tasks** + FastAPI Worker

  * 작업 예: 음성 전사, 이미지 분석, 대용량 임베딩
* **Pub/Sub** (대규모 이벤트 처리 시 확장 가능)

## 모니터링 & 로깅

* **LangSmith**: Prompt/Chain/Agent 실행 로깅 및 품질 평가
* **Cloud Logging**: Cloud Run 로그 수집
* **Cloud Monitoring**: API 지연/에러율 알람
* **Sentry** (선택): 프론트/백엔드 예외 모니터링

## 비용 관리 (MVP 기준 추정)

* **Cloud Run**: 무부하 시 \$0, 요청 기반 과금 (월 수천\~수만 원 수준)
* **Supabase**: Free → Pro 전환 시 \$25\~\$50/월
* **Qdrant Cloud**: Starter 플랜(약 \$15/월)
* **Cloudflare R2**: 저장량 기반(수 GB → 저렴)
* **OpenAI**: 사용량 기반 (Embedding + GPT 호출량 모니터링 필수)
* **LangSmith**: 로깅량 기반 플랜 확인 필요

## 확장 로드맵 (인프라 관점)

* Phase 2:

  * Cloud Tasks 기반 비동기 파이프라인
  * Cloud SQL(Postgres)로 Supabase DB 마이그레이션 고려
* Phase 3:

  * 글로벌 배포(Fly.io, Multi-region Cloud Run)
  * 캐시 계층(Redis or MemoryStore)
* Phase 4:

  * 멀티 테넌트 구조 지원
  * 벡터 DB → 관리형 대규모 서비스(Pinecone, Weaviate Cloud) 전환

## 체크리스트

* [x] Cloud Run 배포 파이프라인 설정
* [x] Secret Manager 연동
* [ ] Cloud Tasks Worker 설계
* [ ] Observability 지표 설계 (LangSmith + Cloud Monitoring 대시보드)
* [ ] 데이터 보존/삭제 정책 수립 (자녀 만 14세 이후 삭제권 포함)
