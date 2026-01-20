from dependency_injector import containers, providers

from user.infra.repository.user_repo import UserRepository
from note.infra.repository.note_repo import NoteRepository

from user.application.user_service import UserService
from note.application.note_service import NoteService

class Container(containers.DeclarativeContainer):
    # 의존성 주입(DI) 대상을 자동으로 찾기 위한 와이어링 설정
    wiring_config = containers.WiringConfiguration(
        # @inject 데코레이터를 스캔할 패키지 범위 지정
        packages=[
            "user",
            "note",
            ],        
    )

    # Factory: 주입 요청 시마다 새로운 객체 인스턴스 생성
    # Singleton: 앱 생명주기 동안 단 하나의 객체 인스턴스만 생성 및 공유
    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)
    note_repo = providers.Factory(NoteRepository)
    note_service = providers.Factory(NoteService, note_repo=note_repo)
    