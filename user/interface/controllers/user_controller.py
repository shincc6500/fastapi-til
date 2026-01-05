from datetime import datetime
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from pydantic import BaseModel, EmailStr, Field

# from containers import Container
from user.application.user_service import UserService

router = APIRouter(prefix="/users") # 이 파일에 있는 모든 API는 /users 로 경로가 시작됨. 

# 데이터 검증 및 파싱을 위한 파이단틱 모델 선언. 추후 별도 파일로 분리. 
class CreateUserBody(BaseModel):
    name : str = Field(min_length=2, max_length=32)
    email : EmailStr = Field(max_length=64)
    password : str = Field(min_length=8, max_length=32)

class UpdateUser(BaseModel):
    name : str | None = Field(min_length=2, max_length=32, default=None)
    password : str | None = Field(min_length=8, max_length=32, default=None)

class UserResponse(BaseModel):
    id: str
    name : str
    email : EmailStr
    created_at: datetime
    updated_at: datetime

# /user 경로로 post 메서드를 통해 요청 받을 수 있음. 성공시 201 반환, response_model로 반환에 대한 데이터 필터링. 
@router.post("", status_code=201, response_model=UserResponse) 
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide["user_service"]),
)-> UserResponse:  # 타입 힌트 추가를 통한 문서화 기능
    """
    user 생성용 API 
    """
    
    created_user = user_service.create_user(
        name=user.name,
        email=user.email, 
        password=user.password,
    )

    return created_user

@router.put("/{user_id}")
@inject 
def update_user(
    user_id : str,
    user: UpdateUser, 
    user_service: UserService = Depends(Provide["user_service"])
):
    user= user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password,
    )

    return user


@router.get("")
@inject
def get_users(
    page: int = 1,
    items_per_page: int = 10,
    user_service: UserService = Depends(Provide["user_service"]),
):
    total_count, users = user_service.get_users(page, items_per_page)

    return {
        "total_count" : total_count, 
        "page" : page, 
        "users" : users,
    }

@router.delete("",status_code=204)
@inject
def delete_user(
    user_id: str, 
    user_service:UserService = Depends(Provide["user_service"]),
):
    # TODO: 다른 유저를 삭제할 수 없도록 토큰에서 유저 아이디를 구한다. 

    user_service.delete_user(user_id)