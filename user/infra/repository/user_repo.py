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