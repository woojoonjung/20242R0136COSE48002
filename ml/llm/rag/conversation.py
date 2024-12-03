import sys, os
from dotenv import load_dotenv
import numpy as np
import openai
sys.path.append(os.path.abspath("/home/work/woojun/Capston/20242R0136COSE48002"))
from ml.llm.rag.retriever import Retriever
from ml.llm.rag.utils import (
    load_documents, 
    google_lens, 
)
from ml.llm.rag.image_similarity import ImageSimilarity

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

# Make candidates considering the first query and the image from the user
def make_candidates(query, image):
    asan_loc = "/home/work/woojun/Capston/20242R0136COSE48002/ml/llm/data/disease_details.json"
    documents = load_documents(asan_loc)

    symptom_texts = []
    for entry in documents:
        if len(entry["details"].get("증상", "").split()) > 1:
            symptom_texts.append((entry["name"], entry["details"].get("증상", "")))

    retriever = Retriever(symptom_texts)
    retriever.index_documents()

    retrieved_from_query = retriever.retrieve(query)
    retrieved_from_img = google_lens(image, google_api_key)

    from_text = ""
    from_image = ""
    for i in range(10):
        from_text += f"{retrieved_from_query[i]} \n"
        from_image += f"{retrieved_from_img[i]} \n"

    analysis = f"""
    *** from symptom image ***
    {from_image}
    ---
    *** from symptom text ***
    {from_text}

    """
    messages = [
        {
            "role": "system", 
            "content": """
            당신은 피부과 전문의입니다. 
            분석 결과에서 *** from symptom image ***, *** from symptom text *** 모두 고려하되 나열하는 질병의 이름은 *** from symptom text *** 에서 언급된 것만 사용해주세요.
            답변은 부연 설명 없이 오직 질병의 이름만 나열해주세요."""
        },
        {
            "role": "user", 
            "content": f"""--분석 결과--
            {analysis}
            숫자는 해당 질병일 확률을 나타냅니다. 가장 가능성이 높은 질병 3개를 추측해주세요."""
        },
        {
            "role": "assistant",
            "content": """
            Malignant melanoma
            Nevus flammeus
            Skin cancer
            """
        }
    ]

    response = openai.Completion.create(
        model="gpt-4o",
        messages=messages
    )
    
    return response['choices'][0]['message']['content']


# Retrieve context
def retrieve_context(candidates):
    asan_loc = "/home/work/woojun/Capston/20242R0136COSE48002/ml/llm/data/disease_details.json"
    documents = load_documents(asan_loc)
    candidates = [line.strip() for line in candidates.strip().split("\n")]
    context = {}
    for disease in candidates:
        for entry in documents:
            name = entry['name'].split('(')[-1].replace(')', '').strip()
            if disease == name:
                context[entry['name']] = entry['details']
                break
            else:
                context[entry['name']] = "No details found"
    return context


# Generate questions for eliminating candidates
def generate_question(retrieved_context):
    messages = [
        {
            "role": "system", 
            "content": "당신은 피부과 전문의입니다. 캐주얼한 대화 방식으로 진료를 진행해주세요."
        },
        #### 1-shot ICL ####
        {
            "role": "user",
            "content": "후보 질병: [{\"이름\": \"땀띠(Miliaria)\", \"증상\": \"얕은 부위의 땀관이 막힌 땀띠는 1mm 정도의 물방울 모양의 투명한 물집으로 나타납니다. 이 경우 자각 증상이 없습니다. 깊은 부위의 땀관이 막힌 땀띠의 경우 붉은 구진, 농포가 발생합니다. 이 경우 심한 가려움증이 나타날 수 있습니다. 땀띠는 주로 머리, 목, 몸통 상부, 겨드랑이 등에 발생합니다.\"}, {\"이름\": \"건선(Psoriasis)\" , \"증상\": \"건선은 주로 대칭성으로 발생하는데, 사지의 폄 쪽(특히 정강이), 팔꿈치, 무릎, 엉치뼈, 두피 등 자극을 많이 받는 부위에 발생합니다. 초기에는 피부에 붉은색의 작은 좁쌀알 같은 발진(구진)이 생기고, 이것이 점점 호두나 계란 크기로 커집니다. 이후 그 주위에서 좁쌀 같은 발진이 새로 생기는데, 이것도 커지면서 서로 합쳐져서 결국 큰 계란이나 손바닥만 한 크기의 발진이 됩니다. 그 위에는 하얀 비늘과 같은 인설이 겹겹이 쌓입니다. 건선은 대체로 인설로 덮인 판의 형태를 띠며 인설을 제거하면 점상 출혈이 나타납니다. 이는 건선의 특이적인 증상입니다. 드물게 나타나는 농포성 건선의 경우 농포가 주로 나타납니다. 건선 환자의 30~50%에서 손발톱 병변이 확인됩니다. 조갑 함몰, 조갑 박리, 조갑 비후, 조갑하과각화증, 조갑하황갈색반 등 여러 가지 병변이 나타날 수 있습니다.\"}], \
            환자의 답을 들었을 때 이 중 하나를 소거할 수 있는 질문을 생성해주세요. 답은 예 또는 아니오로 할 수 있어야 합니다."
        },
        {
            "role": "assistant",
            "content": "심한 가려움증이 있으신가요?"
        },
        ####################
        {
            "role": "user", 
            "content": f"후보 질병: {retrieved_context}. 환자의 답을 들었을 때 이 중 하나를 소거할 수 있는 질문을 생성해주세요. 답은 예 또는 아니오로 할 수 있어야 합니다."
        }
    ]
    
    response = openai.Completion.create(
        model="gpt-4o",
        messages=messages
    )
    
    return response['choices'][0]['message']['content']

# Eliminate Disease
def eliminate_disease(context, conversation, selection):
    question = conversation[-1]
    ## TBD