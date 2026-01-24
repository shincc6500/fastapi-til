from fastapi import FastAPI, Request

from common.auth import CurrentUser, decoded_access_token
from common.logger import logger
from context_vars import user_context

"""
요청이 발생했을 시 해당 요청동안 context 변수에 요청한 유저 정보를 기록하는 미들웨어
"""
def create_middlewares(app: FastAPI):
    @app.middleware("http")
    def get_current_user_middleware(request: Request, call_next):
        authorization = request.headers.get("Authorization")
        if authorization:
            splits = authorization.split(" ")
            if splits[0] == "Bearer" :
                token = splits[1]
                payload = decoded_access_token(token)
                user_id = payload.get("user_id")
                user_role = payload.get("role")

                user_context.set(CurrentUser(user_id, user_role))

        logger.info(request.url)
        
        response = call_next(request)

        return response