
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from pydantic import BaseModel

# from containers import Container
from user.application.user_service import UserService

router = APIRouter(prefix="/users") # 이 파일에 있는 모든 API는 /users 로 경로가 시작됨. 

# 데이터 검증 및 파싱을 위한 파이단틱 모델 선언. 추후 별도 파일로 분리. 
class CreateUserBody(BaseModel):
    name : str
    email : str
    password : str

class UpdateUser(BaseModel):
    name : str | None = None    
    password : str | None = None


@router.post("", status_code=201) # /user 경로로 post 메서드를 통해 요청 받을 수 있음. 성공시 201 반환
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide["user_service"]),
):
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
    user_service: UserService = Depends(Provide["user_service"]),
):
    users = user_service.get_users()

    return {
        "users" : users,
    }
