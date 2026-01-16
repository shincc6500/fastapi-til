import os

from enum import Enum
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose import JWTError, jwt

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

"""
3.11 버전부터 StrEnum을 지원하여, 코드를 수정. 
"""
class Role(str, Enum): 
    ADMIN = "ADMIN"
    USER = "USER"

def create_access_token(
        payload: dict,
        role: Role, 
        expires_delta: timedelta = timedelta(hours=6),
):
    expire= datetime.now(timezone.utc) + expires_delta # 만료시간 계산. 교제와 버전 차이로 인한 변화 
    payload.update(
        {
            "role": role,
            "exp": expire,
        }
    )
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt

def decoded_access_token(token:str):
    try : 
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)