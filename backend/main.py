import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from router.prompt import router as prompt_router

app = FastAPI()

router = APIRouter()
router.include_router(prompt_router)
app.include_router(router)


# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (원하는 도메인으로 제한 가능)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (POST, GET 등)
    allow_headers=["*"],  # 모든 헤더 허용
)