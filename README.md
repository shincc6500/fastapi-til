# fastapi-til
FastAPI 기반의 '오늘 배운 내용(TIL)' 기록 시스템입니다. 클린 아키텍처를 준수하여 유지보수와 확장이 용이하게 설계되었습니다.
교제 제공 예제 깃허브 : https://github.com/dextto/fastapi-ca

## 🛠 기술 스택
- **Framework:** FastAPI
- **Dependency Management:** Poetry
- **ORM:** SQLAlchemy (with MySQL)
- **Architecture:** Clean Architecture (Domain-Driven Design)
- **DI Container:** Dependency Injector

# 1. 주요기능

### 유저 관리 (UserCRUD)
- 유저 생성 : 비밀번호 암호화 로직 적용
- 유저 조회 : 유저 목록 조회 및 Offset 기반 페이징 처리 적용
- 유저 수정  
- 유저 삭제  
- TODO: 권한 등급 추가

# 2. 시작 개요
프로젝트를 로컬 환경에서 실행하기 위한 절차입니다. 
본 프로젝트는 'Poetry'를 사용하여 의존성을 관리합니다. 

### 2-1. 사전준비
- **python:** 3.10 이상
- **Poetry:** 설치 필요
- **MySQL Server:** 8.0 이상 설치 필요
  - 설치 후, 프로젝트에서 사용할 데이터베이스를 미리 생성해야 합니다.
  ```sql
  CREATE DATABASE your_db_name;
  ```

### 2-2. 의존성 설치
다음 코드를 터미널에 입력하여 poetry.lock 및 pyproject.toml에 저장된 의존성 목록을 설치하니다
```bash
poetry install
```
### 2-3. 환경변수 설정(.env)
루트 디렉토리에 .env 파일을 생성하고 필요한 설정값을 입력합니다. 필요한 설정값은 아래의 .env 파일에 대한 정보를 참조하십시오

### 2-4. 프로젝트 실행
루트 디렉토리에서 터미널을 열어 다음 코드를 입력하십시오. 그 후 [127.0.0.1:8000](http://127.0.0.1:8000) 주소를 web에 입력하여 프로젝트에 진입하십시오
```bash
python main.py
```


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
서버 실행 후 브라우저에서 아래 주소로 접속하십시오.

- Swagger UI: http://127.0.0.1:8000/docs


# trouble shooting

### 1. 의존성 주입 실패: 객체 대신 Provide 객체가 그대로 반환되는 문제

**현상**
- `dependency-injector`를 이용한 의존성 주입 시, 실제 객체가 아닌 `Provide` 객체가 그대로 참조됨.
- 이로 인해 메서드 호출 시 `AttributeError`가 발생하며 서버가 정상 작동하지 않음.

**원인 및 해결**
1. **패키지 인식 불가능으로 인한 Wiring 누락**
   - **원인**: `dependency-injector`의 wiring은 명시적인 파이썬 패키지 구조를 기반으로 스캔함. `__init__.py`가 없는 폴더는 정식 패키지로 인식되지 않아 의존성 교체가 일어나지 않음.
   - **해결**: 모든 소스 폴더에 빈 `__init__.py` 파일을 생성하여 명시적인 파이썬 패키지로 정의함.
   - **향후 계획**: 새로운 디렉토리 생성 시 반드시 `__init__.py`를 포함하도록 작업 규칙을 정립함.

### 2. 유저 정보 업데이트 시 password 암호화 실패

**현상**
- 유저 정보 업데이트 API 호출 시, 패스워드가 암호화되지 않고 평문으로 저장됨.

**원인 및 해결**
1. **Application 계층의 할당 오류**
   - **원인**: `update` 메서드 내에서 `user.password` 필드가 아닌 일반 변수에 암호화 값을 할당함.
   - **해결**: `user.password` 객체 필드에 직접 암호화된 값을 할당하도록 수정함.
2. **Infra 계층의 수동 덮어쓰기 문제**
   - **원인**: Application에서 가공한 객체를 Infra 계층에서 다시 수동으로 매핑하며 평문 데이터가 유입됨.
   - **해결**: (단기) 매핑 로직을 암호화 필드 중심으로 수정함.
   - **향후 계획**: `db.merge()` 방식을 도입하여 객체 상태가 DB에 그대로 반영되도록 구조 개선 예정.