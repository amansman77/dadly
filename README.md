# Dadly

**Where dad's love becomes memory.**

## 슬로건
**Dadly — Where dad's love becomes memory.**

## 프로젝트 개요
**Dadly**는 아빠가 남긴 기록과 이야기를 가족과 함께 나누고, 시간이 흘러도 잊히지 않도록 보존하는 서비스입니다.  
단순한 일기 앱을 넘어, **사랑의 흔적을 기억으로 전환하는 플랫폼**을 지향합니다.  

## 기획 방향성
1. **가족 중심의 기록 아카이브**
   - 아빠의 일기, 음성, 사진, 영상 등을 남기고 자녀와 연결  
   - 단순 저장이 아니라, **가족이 함께 접근하고 공유**할 수 있는 구조  

2. **AI 기반의 스토리텔링**
   - 기록을 자동으로 **요약, 태깅, 감정 분석**  
   - 검색과 타임라인을 통해 **빠르게 맥락을 되살릴 수 있는 경험** 제공  

3. **시간과 감정의 연결**
   - 자녀의 성장 시점에 맞춰 기록을 묶어주는 **타임라인**  
   - 특정 시기에 남겨진 기록을 미래에 열람할 수 있는 **타임캡슐 기능**  

4. **따뜻함과 신뢰**
   - "아빠의 사랑이 기억이 된다"는 철학을 기반으로 **정서적 가치를 최우선**  
   - 데이터 보안과 가족 프라이버시를 존중하는 설계  

## 기술 스택 (AI Lean Stack)

- **Frontend**: Streamlit  
- **Backend API**: FastAPI (Auth, Entries, Search, Capsule)  
- **LLM Layer**: LangChain + OpenAI  
- **VectorDB**: Qdrant Cloud  
- **Database**: Supabase (Postgres)  
- **Storage**: Cloudflare R2  
- **Auth**: Supabase Auth  
- **Observability**: LangSmith (프롬프트/질답 로깅), Cloud Logging  

**Deployment**: GCP Cloud Run (컨테이너 기반)

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd dadly

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
# env.example을 복사하여 .env 파일 생성
cp env.example .env

# .env 파일을 편집하여 실제 API 키들을 입력
# 특히 OPENAI_API_KEY는 필수입니다
```

### 3. 애플리케이션 실행

#### 백엔드 (FastAPI) 실행
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### 프론트엔드 (Streamlit) 실행
```bash
cd app
streamlit run main.py
```

### 4. 접속
- **FastAPI**: http://localhost:8000 (API 문서: http://localhost:8000/docs)
- **Streamlit**: http://localhost:8501

## 💬 채팅 기능

현재 구현된 채팅 기능:

- **AI 어시스턴트**: 가족 기록과 추억에 대한 따뜻한 대화
- **대화 기억**: 세션 동안의 대화 내용 유지
- **새 대화 시작**: 언제든지 새로운 대화 시작 가능
- **한국어 지원**: 한국어로 자연스러운 대화

### 채팅 API 엔드포인트

- `POST /api/chat/` - 채팅 메시지 전송
- `GET /api/chat/conversations/{id}/history` - 대화 기록 조회
- `DELETE /api/chat/conversations/{id}` - 대화 기록 삭제
- `GET /api/chat/health` - 서비스 상태 확인

## MVP 기능
- **기록 업로드**: 텍스트/이미지/오디오 기록 저장 (R2 스토리지 연동)  
- **자동 요약·태깅**: AI 기반 요약, 감정·주제 태깅, 벡터 임베딩 저장  
- **타임라인 뷰**: 연/월/자녀 나이별로 기록 탐색  
- **검색 (RAG)**: 자연어 질의로 과거 기록을 빠르게 찾아 요약 제공  
- **타임캡슐**: 미래 개봉일을 설정하여 메시지 저장  
- **가족 초대**: Supabase Auth 기반의 초대/권한 관리  

## 확장 로드맵
- **Phase 2: 운영 안정화**  
  - Cloud Tasks 기반 비동기 처리  
  - 이미지/오디오 전사(Whisper) 프로덕션화  
  - Sentry & 성능 모니터링 강화  

- **Phase 3: 가족 경험 확장**  
  - 협업 코멘트/하이라이트  
  - 감정 히트맵(월별·연도별)  
  - PDF/포토북 생성  

- **Phase 4: 스케일링 & 최적화**  
  - 관리형 VectorDB 최적화  
  - 캐시 및 비용 최적화  
  - 프롬프트 버전 관리 & 실험 (LangSmith Experiments)  

## 개발 가이드

자세한 개발 가이드는 다음 문서들을 참조하세요:

- [DEVELOPMENT.md](DEVELOPMENT.md) - 개발 환경 설정 및 실행 방법
- [CODING_STANDARDS.md](CODING_STANDARDS.md) - 코딩 표준 및 베스트 프랙티스
- [INFRASTRUCTURE.md](INFRASTRUCTURE.md) - 인프라 설계 및 배포 가이드
- [AGENTS.md](AGENTS.md) - AI 에이전트 개발 규칙

## 철학
> **Dadly는 단순한 기록 앱이 아닙니다.**  
> 아빠가 남긴 작은 글과 말 속에 담긴 **사랑과 배움**을,  
> 시간이 지나도 가족이 **다시 느끼고 공감할 수 있는 기억**으로 전환하는 플랫폼입니다.  

## 라이선스

이 프로젝트는 [Apache License 2.0](LICENSE) 하에 배포됩니다.

## 슬로건
**Dadly — Where dad's love becomes memory.**
