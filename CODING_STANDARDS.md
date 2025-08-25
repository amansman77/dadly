# CODING_STANDARDS.md
Dadly — Engineering Coding Standards  
(Last updated: 2025-08-25, KST)

본 문서는 Dadly 프로젝트의 일관성과 품질을 보장하기 위한 코딩 표준입니다.  
대상: **Python(FastAPI, LangChain), Streamlit(Frontend), 인프라 스크립트**.  
참고: 향후 Node/TS 코드가 추가될 경우 별 부록으로 관리합니다.

## 1. 공통 철학
- **가독성 > 마이크로 성능 최적화** (성능은 측정 후 최적화)
- **명시적(Explicit) > 암묵적(Implicit)** — 타입힌트/명명/예외 처리
- **테스트 우선** — 회귀 방지, LLM 호출은 모킹/샘플 기반
- **보안/개인정보 최우선** — 비밀키/민감정보는 절대 코드에 하드코딩 금지
- **작게 PR, 자주 배포** — 리뷰 가능 단위로 쪼개기

## 2. 언어/스타일 가이드

### 2.1 Python
- 버전: **3.11+**
- 포매터: **black** (라인 길이 100)
- 임포트 정렬: **isort**
- 린트: **ruff**
- 정적 타입체커: **mypy** (strict 모드 권장)
- 스타일: **PEP8** 기반, 독스트링은 **Google style** 사용
- 파일 인코딩: UTF-8, **.editorconfig** 준수

**`pyproject.toml` 권장 값**
```toml
[tool.black]
line-length = 100
target-version = ["py311"]

[tool.isort]
profile = "black"
line_length = 100

[tool.ruff]
line-length = 100
select = ["E","F","I","UP","B","SIM","PL","TID","C90"]
ignore = ["E203"]  # black과 충돌
target-version = "py311"

[tool.mypy]
python_version = "3.11"
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
strict_optional = true
