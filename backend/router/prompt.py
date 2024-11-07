import os, sys
sys.path.append(os.path.abspath("/workspace/capston"))
import openai
from fastapi import APIRouter , File, UploadFile, Form
from pydantic import BaseModel
from ml.llm.rag.main import main
from ml.llm.rag.retriever import Retriever
from ml.llm.rag.utils import load_documents, google_image_search
from ml.llm.rag.image_similarity import ImageSimilarity

#### pydantic class

class Prompt(BaseModel):
    symptoms: str = ""
    
####

router = APIRouter(prefix="/prompt")

@router.post("/retriever")
async def process(
    query: str = Form(...),
    query_img: UploadFile = File(None)
):
    
    asan_loc = "/workspace/capston/ml/llm/data/disease_details.json"

    documents = load_documents(asan_loc)
    documents = str(documents)
    retriever = Retriever(documents)
    #generator = Generator()

    retriever.index_documents()

    # query = "피부가 붉고, 기름진 각질이 생겨 간지러워요."
    # query_img = load_image("workspace/ml/llm/data/test.png")
    # image_sim = ImageSimilarity()

    retrieved_docs = retriever.retrieve(query)
    return retrieved_docs

@router.post("/google_search")
async def process(
    query: str = Form(...),
    query_img: UploadFile = File(None)
):
    asan_loc = "/workspace/capston/ml/llm/data/disease_details.json"

    documents = load_documents(asan_loc)
    documents = str(documents)
    # print("!!!!!!!!!!!!!!!!!!!!!!!!",documents)
    # Initialize Retriever and Generator
    retriever = Retriever(documents)
    #generator = Generator()

    retriever.index_documents(documents)

    # query = "피부가 붉고, 기름진 각질이 생겨 간지러워요."
    # query_img = load_image("workspace/ml/llm/data/test.png")
    image_sim = ImageSimilarity()

    retrieved_docs = retriever.retrieve(query)
    retrieved_imgs = []
    pairs = []

    for disease in retrieved_docs:
        google_query = disease[0]
        api_key = os.getenv("API_KEY")
        cse_id = os.getenv("CSE_ID")
        retrieved_imgs += google_image_search(google_query, api_key, cse_id)
        pairs += [(disease, img_url) for img_url in retrieved_imgs]
    
    results = image_sim.compare_images(query_img, retrieved_imgs)
    diagnosis = next(pair[0] for pair in pairs if pair[1] == results[0])

    context = find_entity_by_name(documents, diagnosis)
    context = str(context)

    # Generate response based on retrieved documents
    response = generator.generate_response(context, query)


    
@router.post("/main")
async def process(
    query: str = Form(...),
    query_img: UploadFile = File(None)
):
    message_content = main(query,query_img)
    return {message_content}
    # else:
    #     # OpenAI API 키 설정
    #     openai.api_key = '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'



    #     # 프롬프트 설정 및 GPT-3 호출
    #     response = openai.chat.completions.create(
    #         model="gpt-3.5-turbo",  # 사용할 모델 (davinci, gpt-3.5 등)
    #         messages=[
    #             {"role": "system", "content": "You are a kind doctor."},
    #             {"role": "user", "content": f"{symptoms}"}
    #         ],
    #         max_tokens=400,         # 생성할 토큰 수
    #         temperature=0.7         # 응답의 창의성 정도 (0.0 ~ 1.0)
    #     )

    #     # 생성된 텍스트 출력

    #     message_content = response.choices[0].message.content.strip()
    #     print(message_content)

    #     return message_content




@router.post("/message")
async def process(
    symptoms: str = Form(...),
    image: UploadFile = File(None)
):
    if image:
        image_content = await image.read()  # 이미지 파일 읽기


    if symptoms == "피부가 간지럽고 붉은게 올라왔어 이게 뭘까?":
        message_content = """

        간지럽고 붉은 발진은 여러 가지 원인이 있을 수 있습니다. 
        피부염, 알레르기 반응, 습진, 건선 등 다양한 피부 질환의 증상일 수 있습니다. 
        특히, 새로운 화장품이나 세제를 사용하거나, 음식 알레르기가 있는 경우에도 발생할 수 있습니다. 
        특정한 진단을 위해서는 진료를 받아야 하지만, 일단 냉소자극을 피하고 쿨링 젤이나 스킨로션을 바르는 것이 도움이 될 수 있습니다. 
        만약 증상이 계속되거나 심해진다면 피부과 전문의를 찾아 상담하는 것이 좋습니다.
        """
        return {message_content}

    elif symptoms == "피부에 작은 혹처럼 부어오르고 고름이 생겼는데 이게 뭘까요?":
        message_content = """
        죄송합니다, 저는 의사가 아니기 때문에 진단을 내릴 수는 없지만, 당신이 설명한 증상은 여러 가지 원인이 있을 수 있습니다. 
        이런 증상이 나타나면 피부과 전문의를 방문하여 전문적인 진단과 치료를 받는 것이 좋습니다. 
        특히 그 부위가 발적인 곳에 있거나 통증이 심하다면 빠른 치료가 필요할 수 있습니다. 
        건강을 우선으로 생각하여 전문의의 도움을 받는 것이 좋을 것입니다.
        """
        return {message_content}
    else:
        # OpenAI API 키 설정
        openai.api_key = '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'



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
