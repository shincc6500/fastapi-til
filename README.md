# fastapi-til
FastAPI 기반의 '오늘 배운 내용(TIL)' 기록 시스템입니다. 클린 아키텍처를 준수하여 유지보수와 확장이 용이하게 설계되었습니다.

## 🛠 기술 스택
- **Framework:** FastAPI
- **Dependency Management:** Poetry
- **ORM:** SQLAlchemy (with MySQL)
- **Architecture:** Clean Architecture (Domain-Driven Design)

# 1. 주요기능

# 2. 시작 개요

# 3. 프로젝트 구조
fastapi-til/
├── user/               # 사용자 관리 모듈 (회원가입, 인증 등)
├── utils/              # 프로젝트 전역에서 사용되는 공용 유틸리티
──────────────────────────────────────────────────────────────
├── main.py             # FastAPI 애플리케이션 진입점
├── poetry.lock         # 종속성 잠금 파일
├── pyproject.toml      # Poetry 설정 및 의존성 관리
├── .gitignore          # Git 제외 파일 설정
└── README.md           # 프로젝트 문서

모든 도메인 모듈은 유지보수 및 테스트 용이성을 위해 클린아키텍처 기반 4단계 구조를 가짐. 
의존성은 기술 세부 사항(Infra/Interface)에서 핵심 비즈니스(Domain) 방향으로만 흐릅니다.

Domain      : 핵심 비즈니스 모델(Entity) 및 추상 인터페이스(Repository Interface) 정의
Application	: 비즈니스 로직의 흐름 제어 및 유즈케이스(Service) 구현
Interface   : 외부(브라우저, 클라이언트)와의 접점. FastAPI Router 및 DTO(Pydantic) 정의
Infra       : 데이터베이스 구현체(SQLAlchemy) 및 외부 시스템 연동 등 기술 세부 사항 구현

# 4. API 문서 확인 방법

