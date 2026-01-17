from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    애플리케이션 환경 설정 관리 클래스
    
    - 기본 원칙: 환경 변수 누락으로 인한 런타임 에러를 방지하기 위해 기본값 설정을 지양함 (Fail-Fast).
    - 예외: 보안과 무관하며 모든 환경에서 공통적으로 사용되는 설정(예: Port, Log Level)에만 제한적으로 기본값 부여.
    """
        
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

    # DB 설정 (타입 지정)
    DB_TYPE: str
    DB_HOST: str
    DB_PORT: int = 3306  
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # jwt 설정
    SECRET_KEY: str
    ALGORITHM: str

settings = Settings()

@lru_cache
def get_settings():
    return Settings()