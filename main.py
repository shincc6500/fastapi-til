
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import uvicorn

from containers import Container
from user.interface.controllers import user_controller

container = Container()

# FastAPI와 느슨한 결합 구조를 위한 와이어링 제어
container.wire(packages=["user"]) 

app = FastAPI()
app.container= container

app.include_router(user_controller.router)


@app.exception_handler(RequestValidationError) # RequestValidationError 발생시 에러 핸들러 등록
async def validation_exception_handler(
    request: Request,
    exe : RequestValidationError
):
    return JSONResponse(
        status_code=400, # 응답 코드를 400으로 변경
        content=exe.errors() # 예외 객체의 에러를 응답 본문으로 전달. 
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)