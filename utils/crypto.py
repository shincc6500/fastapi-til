from passlib.context import CryptContext

'''
3.2.2 기준으로 사용. 현재 최신 버전의 경우 지금 방식처럼 구현할 경우 버그 발생으로 인해 동작이 불가능함. 
schemes에 "bcrypt_sha256"를 추가하거나, passlib를 삭제하고 직접 검증 로직을 구현하는 방식으로 해결함. 
하단에 passlib 삭제시 구조를 생성. 
'''


class Crypto:
    def __init__(self):
        # 암호화 방식 설정 객체 저장
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt(self, secret):
        return self.pwd_context.hash(secret)
    
    def verify(self, secret, hash):
        return self.pwd_context.verify(secret, hash)
    
# import bcrypt

# class Crypto:
#     def encrypt(self, password: str) -> str:
#         # 비밀번호를 바이트로 변환
#         password_bytes = password.encode('utf-8')
#         # 솔트 생성 및 해싱
#         salt = bcrypt.gensalt()
#         hashed = bcrypt.hashpw(password_bytes, salt)
#         # DB 저장을 위해 문자열로 반환
#         return hashed.decode('utf-8')

#     def verify(self, password: str, hashed_password: str) -> bool:
#         return bcrypt.checkpw(
#             password.encode('utf-8'), 
#             hashed_password.encode('utf-8')
#         )