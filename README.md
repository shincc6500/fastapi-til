# fastapi-til
FastAPI 기반의 '오늘 배운 내용(TIL)' 기록 시스템입니다. 클린 아키텍처를 준수하여 유지보수와 확장이 용이하게 설계되었습니다.
교제 제공 예제 깃허브 : https://github.com/dextto/fastapi-ca

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
├── database/           # database 관련 모듈
├── migrations/         # database 마이그래이션 정보 관리 폴더
├── .env                # DB 접속 정보 등 민감한 환경 변수 파일
──────────────────────────────────────────────────────────────
├── __init__.py         # 패키지 초기화 파일
├── main.py             # FastAPI 애플리케이션 진입점
├── containers.py       # Dependency Injection (의존성 주입) 설정
├── alembic.ini         # Alembic 마이그레이션 구성 파일
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



# trouble shooting
1. 의존성 주입 실패: 객체 대신 Provide 객체가 그대로 반환되는 문제 
현상 : dependency-injector 패키지를 이용한 의존성 주입 과정에서, 실제 등록된 객체(Service, Repo 등)가 주입되지 않고 Provide 객체가 그대로 참조되는 문제 발생. 결과적으로 메서드 호출 시 AttributeError 등이 발생함.
원인 : dependency-injector의 wiring 기능은 명시적인 파이썬 패키지 구조를 기반으로 스캔을 진행합니다. __init__.py 파일이 없는 폴더는 정식 패키지로 인식되지 않아, 와이어링 대상에서 누락되었고 결과적으로 의존성 교체가 일어나지 않았습니다
해결 : 모든 폴더에 빈 __init__.py 파일을 생성하여, 해당 디렉토리가 명시적인 파이썬 패키지임을 정의하였으며, 추후 폴더를 생성할 때 빈 __init__.py 를 같이 생성함. 

2. 유저 정보 업데이트시 password 암호화 실패
현상 : 유저 정보 업데이트 API를 호출시, password가 암호화되지 않고 평문으로 저장되는 현상이 발생함
원인 : 
    1. application 계층에서 update를 수행하는 매서드에서 user의 객체의 password 값에 저장이 아니라 password 변수에 암호화된 값을 입력
    2. Application 계층에서 가공한 객체 정보를 Infra 계층에서 다시 수동으로 덮어쓰는 과정에서 평문으로 저장되는 문제가 발생함.
해결 : 
    1. application 계층의 update 매서드에서 user객체의 password 값에 수정할 값을 할당하여 암호화된 값을 저장함. 
    2. (향후 계획) Infra 계층의 수동 대입 로직을 제거하고, db.merge() 방식을 도입하여 Application 계층에서 완성된 객체 상태가 DB에 그대로 반영되도록 구조를 개선할 예정.