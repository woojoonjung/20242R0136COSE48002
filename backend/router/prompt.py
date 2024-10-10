import os
import openai
from fastapi import APIRouter , Depends
from pydantic import BaseModel

#### pydantic class

class Prompt(BaseModel):
    symptoms: str = ""
    image: str = ""
    
####

router = APIRouter(prefix="/prompt")

@router.post("/")
def process(
    request: Prompt = Depends()
):
    

    # OpenAI API 키 설정
    openai.api_key = '~~'



    # 프롬프트 설정 및 GPT-3 호출
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 사용할 모델 (davinci, gpt-3.5 등)
        messages=[
            {"role": "system", "content": "You are a kind doctor."},
            {"role": "user", "content": f"{request.symptoms}"}
        ],
        max_tokens=100,         # 생성할 토큰 수
        temperature=0.7         # 응답의 창의성 정도 (0.0 ~ 1.0)
    )

    # 생성된 텍스트 출력


    return response['choices'][0]['message']['content'].strip()

