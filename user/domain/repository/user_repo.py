from abc import ABCMeta, abstractmethod
from user.domain.user  import User

class IUserRepository(metaclass=ABCMeta):
    '''
    의존성 역전 구현을 위한 클래스
    application 또는 interface 단계에서 infra를 참조해야 할때
    의존성이 domain 단계에 있도록 하기 위한 클래스. 
    이 클래스를 상속할 경우 이 클래스에 있는 매서드의 
    상세 구현 내용을 반드시 명시 해야 함. 
    '''
    @abstractmethod
    def save(self, user: User):
        """
        Save a User entity.

        Parameters
        ----------
        self : object
           호출한 인스턴스 자신
        user : User
            저장할 User 도메인 객체

        Raises
        ------
        NotImplementedError
            하위 클래스에서 반드시 구현해야 함
        """
        raise NotImplementedError
    
    def find_by_email(self, email: str) -> User:
        """
        이메일로 유저를 검색 
        Parameters
        ----------
        self : object
           호출한 인스턴스 자신
        email : str
            검색에 사용할 유저의 이메일 주소
        Returns
        --------
        User : object
           조회된 유저 도메인 모델 객체

        Raises
        ------
        NotImplementedError
            하위 클래스에서 반드시 구현해야 함
        """
        raise NotImplementedError