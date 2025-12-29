from fastapi import APIRouter
from pydantic  import BaseModel

from user.application.user_service import UserService

router = APIRouter(prefix="/users") # 이 파일에 있는 모든 API는 /users 로 경로가 시작됨. 

# 데이터 검증 및 파싱을 위한 파이단틱 모델 선언. 추후 별도 파일로 분리. 
class CreateUserBody(BaseModel):
    name : str
    email : str
    password : str


@router.post("", status_code=201) # /user 경로로 post 메서드를 통해 요청 받을 수 있음. 성공시 201 반환
def create_user(user: CreateUserBody):
    """
    user 생성용 API 
    """
    user_service = UserService()
    created_user = user_service.create_user(
        name=user.name,
        email=user.email, 
        password=user.password,
    )

    return created_user