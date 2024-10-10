import os
from fastapi import FastAPI, APIRouter

from router.prompt import router as prompt_router

app = FastAPI()

router = APIRouter()

router.include_router(prompt_router)