import sys, os
from dotenv import load_dotenv
import numpy as np
from openai import OpenAI
sys.path.append(os.path.abspath("/home/work/woojun/Capston/20242R0136COSE48002"))
from ml.llm.rag.retriever import Retriever
from ml.llm.rag.utils import (
    load_documents, 
    google_lens, 
)
from ml.llm.rag.image_similarity import ImageSimilarity

load_dotenv()
client = OpenAI()
google_api_key = os.getenv('GOOGLE_API_KEY')

# Generate candidates from user input
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
    print(analysis)

    messages = [
        {
            "role": "system", 
            "content": """
            당신은 피부과 전문의입니다. 
            질병 추측 시 "*** from symptom image ***" 아래에 등장하는 질병들을 모두 고려하되 "*** from symptom text ***" 이후의 질병 이름들만 추측에 사용해주세요.
            답변은 부연 설명 없이 오직 질병의 이름만 나열해주세요.
            """
        },
        {
            "role": "user", 
            "content": f"""--분석 결과--
            {analysis}
            숫자는 해당 질병일 확률을 나타냅니다. 가장 가능성이 높은 질병 3개만 추측해주세요."""
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
    
    # Updated OpenAI Completion API call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    return response.choices[0].message.content  # Adjusted access style


# Retrieve context for candidates
def retrieve_context(candidates):
    asan_loc = "/home/work/woojun/Capston/20242R0136COSE48002/ml/llm/data/disease_details.json"
    documents = load_documents(asan_loc)
    candidates = [line.strip() for line in candidates.strip().split("\n")]
    print(candidates)
    context = {}
    for disease in candidates:
        for entry in documents:
            name = entry['name'].split('(')[-1].replace(')', '').strip()
            if disease == name:
                context[entry['name']] = entry['details']
    return context


# Generate elimination questions
def generate_question(retrieved_context):
    messages = [
        {
            "role": "system", 
            "content": "당신은 피부과 전문의입니다. 캐주얼한 대화 방식으로 진료를 진행해주세요."
        },
        {
            "role": "user",
            "content": "후보 질병: [{\"이름\": \"땀띠(Miliaria)\", \"증상\": \"얕은 부위의 땀관이 막힌 땀띠는 1mm 정도의 물방울 모양의 투명한 물집으로 나타납니다. 이 경우 자각 증상이 없습니다. 깊은 부위의 땀관이 막힌 땀띠의 경우 붉은 구진, 농포가 발생합니다. 이 경우 심한 가려움증이 나타날 수 있습니다. 땀띠는 주로 머리, 목, 몸통 상부, 겨드랑이 등에 발생합니다.\"}, {\"이름\": \"건선(Psoriasis)\" , \"증상\": \"건선은 주로 대칭성으로 발생하는데, 사지의 폄 쪽(특히 정강이), 팔꿈치, 무릎, 엉치뼈, 두피 등 자극을 많이 받는 부위에 발생합니다. 초기에는 피부에 붉은색의 작은 좁쌀알 같은 발진(구진)이 생기고, 이것이 점점 호두나 계란 크기로 커집니다. 이후 그 주위에서 좁쌀 같은 발진이 새로 생기는데, 이것도 커지면서 서로 합쳐져서 결국 큰 계란이나 손바닥만 한 크기의 발진이 됩니다. 그 위에는 하얀 비늘과 같은 인설이 겹겹이 쌓입니다. 건선은 대체로 인설로 덮인 판의 형태를 띠며 인설을 제거하면 점상 출혈이 나타납니다. 이는 건선의 특이적인 증상입니다. 드물게 나타나는 농포성 건선의 경우 농포가 주로 나타납니다. 건선 환자의 30~50%에서 손발톱 병변이 확인됩니다. 조갑 함몰, 조갑 박리, 조갑 비후, 조갑하과각화증, 조갑하황갈색반 등 여러 가지 병변이 나타날 수 있습니다.\"}], \
            환자의 답을 들었을 때 이 중 하나를 소거할 수 있는 질문을 생성해주세요. 답은 예 또는 아니오로 할 수 있어야 합니다."
        },
        {
            "role": "assistant",
            "content": "심한 가려움증이 있으신가요?"
        },
        {
            "role": "user", 
            "content": f"후보 질병: {retrieved_context}. 후보 질병 중에서 해당되지 않을 것 같은 질병 하나를 소거하기 위해 환자에게 추가적으로 해야할 질문을 생성해주세요. 답은 예 또는 아니오로 할 수 있어야 합니다."
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    return response.choices[0].message.content

# Eliminate Disease
def eliminate_disease(context, conversation, selection):
    question = conversation[-1]
    if selection == 'O':
        answer = '네'
    elif selection == 'X':
        answer = '아니오'
    else:
        print("selection: ", selection)
    
    messages = [
        {
            "role": "system", 
            "content": "당신은 피부과 전문의입니다."
        },
        {
            "role": "assistant",
            "content": "Psoriasis"
        },
        {
            "role": "user", 
            "content": f"""
            후보 질병: {retrieved_context},
            환자에게 한 질문: {question},
            환자의 답: {answer}
            환자에게 한 질문과 환자의 답을 고려하여 후보 질병 중 환자의 질병이 아닐 가능성이 가장 큰 질병 하나를 결정해주세요.
            """
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

# Final Diagnosis
def diagnose(context):
    messages = [
        {
            "role": "system", 
            "content": "당신은 피부과 전문의입니다. 친근하고 캐주얼하게 환자와의 진료를 진행해주세요."
        },
        {
            "role": "assistant",
            "content": """
            악성 흑색종은 멜라닌 세포에서 발생하는 피부암으로, 피부뿐만 아니라 점막, 눈 등 다양한 부위에 생길 수 있는데요. 
            초기에는 작은 점이나 변색으로 보일 수 있으나 빠르게 진행하면 생명을 위협할 수 있습니다. 주요 증상으로는 
            비대칭적인 점, 경계가 불규칙한 점,  다양한 색조를 가진 점, 점의 크기 변화 등이 있어요. 
            햇빛 노출이 주요 위험 요인이므로 자외선 차단제를 사용하고 직사광선을 피하는 것이 좋아요.

            가능한 빨리 병원을 방문하여 점의 변화를 의사와 상담하고 필요한 경우 조직 검사를 받으세요. 
            진단 결과에 따라 수술, 방사선 치료, 항암 요법 등 적합한 치료법이 결정됩니다. 치료 후에도 정기적으로 
            검진을 받아 재발 여부를 확인하고, 의사의 권고를 철저히 따르세요. 기존 점이나 새로운 점의 변화를 지속적으로 관찰하며, 
            필요 시 빠르게 의료진과 상의하세요. 

            또한, 건강한 식단과 충분한 휴식을 통해 면역력을 유지하여 치료 효과를 극대화하세요. 
            악성 흑색종은 조기 발견 시 예후가 좋으니, 너무 걱정하지는 마시고 작은 변화라도 놓치지 않는 것이 중요해요 :)

            더 궁금한게 있으신가요?
            """
        },
        {
            "role": "user", 
            "content": f"""
            환자 질병에 대한 정보: {context},
            
            위의 질병을 진단 받은 환자에게 질병에 대한 간단한 설명, 간단한 행동지침, 격려를 포함해 해줘야 할 말을 해주세요.
            """
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )