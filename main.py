from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import uvicorn

from user.interface.controllers.user_controller import router as user_routers

app = FastAPI()
app.include_router(user_routers)

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