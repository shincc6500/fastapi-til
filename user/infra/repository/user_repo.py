from fastapi import HTTPException
from database.database import SessionLocal
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserV0
from user.infra.db_models.user import User
from utils.db_utils import row_to_dict

class UserRepository(IUserRepository):
    """
    User 데이터 영속화를 위한 인프라 단계 클래스 
    IUserRepository에서 정의된 메서드를 상세 구현 하는 클래스 
    """
    def save(self, user: UserV0):
        """
        신규 유저 저장용 매서드
        """
        new_user = User(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            memo=user.memo,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        with SessionLocal() as db:
            try:
                db.add(new_user)
                db.commit()
            finally:
                db.close()
     
    def find_by_email(self, email:str) -> User:
        """
        이메일 기반 유저 조회 매서드
        """
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
        
        if not user: 
            raise HTTPException(status_code=422)
                
        return UserV0(**row_to_dict(user))
    
    def find_by_id(self, id:str) -> User:
        """
        ID 기반 유저 조회 매서드
        """
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()

        # 유저를 조회하지 못한 경우 422 에러 반환
        if not user:
            raise HTTPException(status_code=422)
        
        return UserV0(**row_to_dict(user))
    
    def update(self, user_v0: UserV0):
        '''
        [주의] 유저 정보 갱신 메서드
    
        - 문제점: Session Detached 오류 회피를 위해 DB에서 객체를 재조회(Select)함.
        - 리스크: Application 계층에서 가공(예: 암호화)한 객체 정보를 Infra 계층에서 
                다시 수동으로 덮어쓰는 과정에서 데이터 누락이나 평문 저장 사고 발생 가능.
        - 개선 방향: 실무에서는 객체의 상태를 그대로 반영하는 db.merge()나 
                Unit of Work 패턴을 활용하여 계층 간 데이터 일관성을 유지함.
        '''
        with SessionLocal() as db: 
            # id 기준으로 DB에서 유저정보 호출
            user = db.query(User).filter(User.id == user_v0.id).first()

            # 유저를 조회하지 못한 경우 422 에러 반환
            if not user:
                raise HTTPException(status_code=422)
            
            # 입력받은 유저 정보로 db에서 조회한 user 객체 정보 갱신. 
            user.name = user_v0.name
            user.password = user_v0.password
            db.add(user)
            db.commit()

        return user
    
    def get_users(self) -> list[UserV0]:
        with SessionLocal() as db:
            users = db.query(User).all()

        return [UserV0(**row_to_dict(user)) for user in users]