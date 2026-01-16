from typing import Annotated
from ulid import ULID
from datetime import datetime
from fastapi import HTTPException, Depends, status
from dependency_injector.wiring import inject, Provide

from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository

from utils.crypto import Crypto
from common.auth import create_access_token, Role

# from Containers import containser를 사용할 경우 컨테이너와 userservice 클래스를 순환 참조하게 되어 오류가 발생. 

class UserService:
    @inject
    def __init__(
            self,
            user_repo: IUserRepository = Depends(
                Provide["user_repo"] 
                ),
            ):
        # 현재 합성 방식으로 구현, 나중에 의존성 주입 방식으로 수정. 
        print("의존성 주입 테스트")
        self.user_repo =user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(
            self,
            name: str,
            email: str,
            password: str,
            memo: str | None= None,
        ):
        """
        새로운 유저를 생성합니다. 

        1. 이메일 중복 체크(중복시 422 에러)
        2. 비밀번호 암호화 및 ULID 기반 id 생성
        3. repository에 저장
        """

        _user = None  # 임시 변수 혹은 내부용 변수의 경우 변수 앞에 _ 를 붙이는 것이 관례. 

        try:
            _user = self.user_repo.find_by_email(email) # 입력받은 이메일 기준으로 기존 데이터 조회
        except HTTPException as e: 
            if e.status_code != 422: # 422 외의 오류가 발생할 경우 오류 출력  
                raise e
            
        if _user: # _user 가 있는 경우 422 에러 반환
            raise HTTPException(status_code=422)

        now = datetime.now() # 현재 시간
        # 입력받은 값을 이용하여 생성한 User 객체를 변수 user에 할당. 
        user: User = User(
            id = self.ulid.generate(),  # ulid 생성
            name = name,                
            email = email,
            password=self.crypto.encrypt(password),
            memo=memo,
            created_at= now, 
            updated_at= now,
        )
        self.user_repo.save(user) # user_repo의 save 매서드를 이용하여 user 변수에 할당된 객체를 저장. 

        return user
    
    def update_user(
            self,
            user_id: str, 
            name: str | None = None,
            password: str | None= None,
    ):
        user = self.user_repo.find_by_id(user_id)

        if name:
            user.name = name
        if password:
            user.password=self.crypto.encrypt(password)
        user.updated_at = datetime.now()

        self.user_repo.update(user)

        return user
    
    def get_users(self, page, items_per_page) -> tuple[int, list[User]]:
        users = self. user_repo.get_users(page, items_per_page)
        return users
    
    def delete_user(self, user_id: str):
        #TODO: 유저 존재 여부 확인 후 없으면 오류 출력 코드 추가. 

        self.user_repo.delete(user_id)

    def login(self, email: str, password: str):
        user = self.user_repo.find_by_email(email) #이메일을 로그인 아이디로 사용

        # DB에서 통과 하지 못할 시 에러 반환
        if not self.crypto.verify(password, user.password):
            raise HTTPException(statue_code=status.HTTP_401_UNAUTHORIZED)
            
        # id 기준으로 엑세스 토큰 발행
        access_token = create_access_token(
            payload={"user_id": user.id},
            role = Role.USER, 
            )
        
        return access_token

        