import os
from fastapi import APIRouter

router = APIRouter(prefix="/prompt")

@router.get("/{message:str}")
async def process(
    message:str
):
    return message