import os
import openai
from fastapi import APIRouter , File, UploadFile, Form
from pydantic import BaseModel

#### pydantic class

class Prompt(BaseModel):
    symptoms: str = ""
    
####

router = APIRouter(prefix="/prompt")




@router.post("/message")
async def process(
    symptoms: str = Form(...),
    image: UploadFile = File(None)
):
    if image:
        image_content = await image.read()  # 이미지 파일 읽기


    if symptoms == "피부가 간지럽고 붉은게 올라왔어 이게 뭘까?":
        message_content = """

        안녕하세요. 
        피부가 간지럽고 붉은 반점이 올라온 것은 여러 가지 원인이 있을 수 있습니다. 
        일단 제가 직접 확인하지는 못하니 정확한 진단을 내리기는 어렵지만, 
        일반적으로 피부염, 알레르기 반응, 수두, 건선 등이 그 원인일 수 있습니다. 
        가능하다면 피부과 전문의를 방문하여 상세한 진단을 받는 것이 좋습니다. 
        특히 피부 상태의 변화나 증상의 심각성이 높아진다면 더 빨리 진
        """
        return {message_content}

    else:
        # OpenAI API 키 설정
        openai.api_key = '~~'



        # 프롬프트 설정 및 GPT-3 호출
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # 사용할 모델 (davinci, gpt-3.5 등)
            messages=[
                {"role": "system", "content": "You are a kind doctor."},
                {"role": "user", "content": f"{symptoms}"}
            ],
            max_tokens=400,         # 생성할 토큰 수
            temperature=0.7         # 응답의 창의성 정도 (0.0 ~ 1.0)
        )

        # 생성된 텍스트 출력

        message_content = response.choices[0].message.content.strip()
        print(message_content)

        return message_content
