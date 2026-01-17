import os

from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

"""
3.11 버전부터 StrEnum을 지원하여, 코드를 수정. 
확장성을 고려하면, int, Enum 구조로 하여 권한마다 등급 지정. 
"""
class Role(str, Enum): 
    ADMIN = "ADMIN"
    USER = "USER"

@dataclass
class CurrentUser:
    id : str
    role: Role

# TODO: 단일 책임 위해 리팩토링
def create_access_token(
        payload: dict,
        role: Role, 
        expires_delta: timedelta = timedelta(hours=6),
):
    expire= datetime.now(timezone.utc) + expires_delta # 만료시간 계산. 교제와 버전 차이로 인한 변화 
    payload.update(
        {
            "role": role.value,
            "exp": int(expire.timestamp()),
        }
    )
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt

def decoded_access_token(token:str):
    try : 
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token error: {str(e)}"
        )
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decoded_access_token(token)

    user_id = payload.get("user_id")
    role = payload.get("role")

    if not user_id  or not role or role != Role.USER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return CurrentUser(user_id, Role(role))

def get_admin_user(token:Annotated[str, Depends(oauth2_scheme)]):
    payload = decoded_access_token(token)

    role = payload.get("role")
    if not role or role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="관리자 계정이 아닙니다.")
    # 정책 결정 전의 id 임시 부여
    return CurrentUser("ADMIN_USER_ID", role)