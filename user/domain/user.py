from dataclasses import dataclass
from datetime import datetime

@dataclass 
class User: 
    id : str
    name : str
    email: str
    password : str
    memo: str | None
    created_at: datetime
    updated_at : datetime

''' 
도메인 클래스를 다루기 쉽도록 dataclass로 선언
데이터 구조 정의를 간결하게 만들고, 유지보수를 쉬워지게 하는 자동화 도구.
특히 DTO(Data Transfer Object), 값 객체, 설정 객체에 강력한 장점을 가진다.
'''