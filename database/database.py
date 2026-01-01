import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base # 최신 버전에서는 orm에서 가져오는것이 표준. 
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# TODO: 현재 세션을 직접 생성중. get_db를 사용하여 의존성 주입 구조로 수정

load_dotenv()

# 환경 변수 읽기
DB_TYPE = os.getenv("DB_TYPE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1") # 기본값 설정
DB_NAME = os.getenv("DB_NAME")

# URL 구성. 
SQLALCHEMY_DATABASE_URL = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
"""
mysql+mysqldb : 데이터 베이스 종류 + 데이터 베이스 드라이버
mysqldb는 mysqlclient 드라이버를 사용한다는 의미
pymysql은 PyMySQL 드라이버를 사용 -> 순수 파이썬으로 설치가 간편. 
"""

#엔진 및 세션 설정
engine= create_engine(SQLALCHEMY_DATABASE_URL) # 데이터 베이스와 연결 통로
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 테이터베이스에 데이터를 넣고 뺄때 쓰는 도구
'''
autocommit=False : 별도 커밋 명령이 없으면 커밋 실행 X
autoflush=False : 데이터를 DB에 자동으로 보내지 않음.
'''

# 베이스 클래스 생성. 
Base = declarative_base() # 파이썬 클래스를 DB 테이블로 변환하는 기준