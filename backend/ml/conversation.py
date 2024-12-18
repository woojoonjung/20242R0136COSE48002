######################################################################################################
# **대화 흐름 제어 파일**                                                                                 #
#                                                                                                    #
# make_candidates: 사용자가 입력한 사진과 증상 텍스트를 기반으로 가장 유력한 후보질환 3개 추출                         #
# retrieve_context: 아산병원 질병백과로부터 해당 후보질환에 대한 상세 정보 가져와 context 라는 dictionary 구성         #
# generate_question: 후보질환을 하나씩 소거하기 위해 사용자에게 해야할 질문 생성, 단 사용자로부터 답변은 O/X 형태로 받음    #
# eliminate_disease: 환자와의 대화기록과 context를 기반으로 후보질환 중 한 개를 소거해달라 요청                      #
# reason_diagnosis: 소거 및 진단에 대한 근거를 환자와의 대화와 context를 대조하여 문구를 추출                        #
# diagnose: 최종 후보질환, 근거 문구, context에 있는 전문지식을 기반으로 환자에게 보여줄 최종 진단 텍스트 생성             #
# faq: 최종진단, 환자와의 대화, context 전문지식을 컨텍스트로 제공받은 상태에서 사용자와 자유로운 대화 진행                 #
#                                                                                                    #
# by woojoonjung at korea univ.                                                                      #
# contact: smallthingsmatter729@gmail.com                                                            #
######################################################################################################

import sys, os
import base64
from dotenv import load_dotenv
import numpy as np
from openai import OpenAI
from ml.retriever import Retriever
from ml.utils import (
    load_documents, 
    google_lens, 
)
sys.path.append(os.path.abspath("/home/work/woojun/Capston/20242R0136COSE48002"))
load_dotenv()
client = OpenAI()
google_api_key = os.getenv('GOOGLE_API_KEY')


# Generate candidates from user input
def make_candidates(query, image):
    asan_loc = "/home/work/woojun/Capston/20242R0136COSE48002/backend/ml/data/disease_details.json"
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
    for i in range(len(retrieved_from_img)):
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
            질병 3개 추측 시 분석 결과에 등장하는 질병들을 모두 고려해주세요. 
            답변에는 "*** from symptom text ***" 이후의 질병 이름들만 사용해주세요.
            답변은 부연 설명 없이 오직 질병의 이름만 나열해주세요.
            """
        },
        {
            "role": "user", 
            "content": f"""
            --분석 결과--
            *** from symptom image ***
            ('Genital herpes', 0.7341) 
            ('Herpes simplex virus', 0.7286) 
            ('Shingles', 0.7228) 
            ('Skin rash', 0.7043) 
            ('Vesicle', 0.7028) 
            ('Virus', 0.6984) 
            ('Infection', 0.6894) 
            ('Sexually transmitted infection', 0.6761) 
            ('Skin condition', 0.6654) 
            ('Genital sores', 0.6182) 
            ---
            *** from symptom text ***
            ('Impetigo', 0.7506076) 
            ('Pemphigus', 0.7113795) 
            ('Hand Eczema', 0.70565295) 
            ('Acute vesiculobullous hand eczema', 0.7052216) 
            ('Eczema', 0.705003) 
            ('Erythema intertrigo', 0.6996006) 
            ('Herpes Simplex', 0.6950346) 
            ('Postzoster neuralgia', 0.67210853) 
            ('Pityriasis versicolor', 0.6627843) 
            ('Wart', 0.658268) 
            숫자는 해당 질병일 가능성을 나타냅니다. 가장 가능성이 높은 질병 3개만 추측해주세요."""
        },
        {
            "role": "assistant",
            "content": """
            Herpes Simplex
            Impetigo
            Pemphigus
            """
        },
        {
            "role": "user", 
            "content": f"""--분석 결과--
            {analysis}
            숫자는 해당 질병일 가능성을 나타냅니다. 가장 가능성이 높은 질병 3개만 추측해주세요."""
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
    asan_loc = "/home/work/woojun/Capston/20242R0136COSE48002/backend/ml/data/disease_details.json"
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
def generate_question(retrieved_context, conversation):
    messages = [
        {
            "role": "system", 
            "content": f"""
            당신은 피부과 전문의입니다. 
            캐주얼한 대화 방식으로 진료를 진행해주세요. 
            환자와의 대화: {conversation}, 
            환자와의 대화에 이미 질문이 있다면 비슷한 내용의 질문은 피해주세요."""
        },
        {
            "role": "user",
            "content": "후보 질병: [{\"이름\": \"땀띠(Miliaria)\", \"증상\": \"얕은 부위의 땀관이 막힌 땀띠는 1mm 정도의 물방울 모양의 투명한 물집으로 나타납니다. 이 경우 자각 증상이 없습니다. 깊은 부위의 땀관이 막힌 땀띠의 경우 붉은 구진, 농포가 발생합니다. 이 경우 심한 가려움증이 나타날 수 있습니다. 땀띠는 주로 머리, 목, 몸통 상부, 겨드랑이 등에 발생합니다.\"}, {\"이름\": \"건선(Psoriasis)\" , \"증상\": \"건선은 주로 대칭성으로 발생하는데, 사지의 폄 쪽(특히 정강이), 팔꿈치, 무릎, 엉치뼈, 두피 등 자극을 많이 받는 부위에 발생합니다. 초기에는 피부에 붉은색의 작은 좁쌀알 같은 발진(구진)이 생기고, 이것이 점점 호두나 계란 크기로 커집니다. 이후 그 주위에서 좁쌀 같은 발진이 새로 생기는데, 이것도 커지면서 서로 합쳐져서 결국 큰 계란이나 손바닥만 한 크기의 발진이 됩니다. 그 위에는 하얀 비늘과 같은 인설이 겹겹이 쌓입니다. 건선은 대체로 인설로 덮인 판의 형태를 띠며 인설을 제거하면 점상 출혈이 나타납니다. 이는 건선의 특이적인 증상입니다. 드물게 나타나는 농포성 건선의 경우 농포가 주로 나타납니다. 건선 환자의 30~50%에서 손발톱 병변이 확인됩니다. 조갑 함몰, 조갑 박리, 조갑 비후, 조갑하과각화증, 조갑하황갈색반 등 여러 가지 병변이 나타날 수 있습니다.\"}], \
            후보 질병 중에서 해당되지 않을 것 같은 질병 하나를 소거하기 위해 환자에게 추가적으로 해야할 질문을 생성해주세요. 답은 예 또는 아니오로 할 수 있어야 합니다."
        },
        {
            "role": "assistant",
            "content": "심한 가려움증이 있으신가요?"
        },
        {
            "role": "user", 
            "content": f"""후보 질병: {retrieved_context}, 
            후보 질병 중에서 해당되지 않을 것 같은 질병 하나를 소거하기 위해 환자에게 추가적으로 해야할 질문을 생성해주세요. 
            질문은 후보 질병들 간의 차이점을 중심으로 생성하고, 답은 예 또는 아니오로 할 수 있어야 합니다.
            """
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    return response.choices[0].message.content

# Eliminate Disease
def eliminate_disease(context, conversation):    
    messages = [
        {
            "role": "system", 
            "content": "당신은 피부과 전문의입니다. 답변은 부연 설명 없이 질병의 영문 이름만 있어야 합니다."
        },
        {
            "role": "assistant",
            "content": "Psoriasis"
        },
        {
            "role": "user", 
            "content": f"""
            후보 질병: {context},
            환자와의 대화: {conversation},
            환자와의 대화를 고려하여 후보 질병 중 환자의 질병이 아닐 가능성이 가장 큰 질병 하나를 결정해주세요.
            """
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    print(response.choices[0].message.content)

    return response.choices[0].message.content

# Reason for Diagnosis
def reason_diagnosis(context, conversation):    
    messages = [
        {
            "role": "system", 
            "content": """당신은 피부과 전문의입니다. 문구는 짧고 간결해야 합니다. "1. ~"와 같은 numbering 또는 "- ~"와 같은 itemizing 은 배제해주세요."""
        },
        {
            "role": "assistant",
            "content": "저녁에 심한 가려움 \n 아토피성 피부염 가족력 \n 긁어서 생긴 피부의 습진성 변화"
        },
        {
            "role": "user", 
            "content": f"""
            후보 질병: {context},
            환자의 증상: {conversation},
            환자의 증상 중 후보 질병의 정보에 해당되는 문구가 있으면 추출 후 간결한 문구로 재구성해주세요. 추출한 문구의 개수와 생성하는 문구의 개수가 같아야 합니다.
            """
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    print(response.choices[0].message.content)

    return response.choices[0].message.content

# Final Diagnosis
def diagnose(context):
    messages = [
        {
            "role": "system", 
            "content": """당신은 피부과 전문의입니다. 
            친근하고 캐주얼하게 환자와의 진료를 진행해주세요. 
            답변 중 이야기의 내용(e.g. 설명, 행동지침, 격려)이 바뀌면 Enter를 통해 줄 바꿈을 해주세요.
            항목화(itemization, e.g.: **피부관리**) 없이 답변을 작성해주세요.
            "~를 진단 받으셨군요."와 같은 멘트 없이 바로 질병에 대한 설명을 적어주세요.
            """
        },
        {
            "role": "assistant",
            "content": """
            악성 흑색종은 멜라닌 세포에서 발생하는 피부암으로, 피부뿐만 아니라 점막, 눈 등 다양한 부위에 생길 수 있는데요.
            초기에는 작은 점이나 변색으로 보일 수 있으나 빠르게 진행하면 생명을 위협할 수 있습니다. 

            가능한 빨리 병원을 방문하여 점의 변화를 의사와 상담하고 필요한 경우 조직 검사를 받으세요.
            진단 결과에 따라 수술, 방사선 치료, 항암 요법 등 적합한 치료법이 결정됩니다. 치료 후에도 정기적으로
            검진을 받아 재발 여부를 확인하고, 의사의 권고를 철저히 따르세요. 기존 점이나 새로운 점의 변화를 지속적으로 관찰하며,
            필요 시 빠르게 의료진과 상의하세요.

            악성 흑색종은 조기 발견 시 예후가 좋으니 걱정마시고 작은 변화라도 놓치지 않는 것이 중요해요 :)
            """
        },
        {
            "role": "user", 
            "content": f"""
            환자 질병에 대한 정보: {context},
            
            위 질병에 대한 2 문장 이내의 간단한 설명, 위 질병을 진단받은 환자가 취해야할 행동지침 그리고 2 문장 이내의 짧은 격려를 해주세요.
            """
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    print(response.choices[0].message.content)

    return response.choices[0].message.content


# Further FAQ
def faq(query, context, conversation, image):

    messages = [
        {
            "role": "system", 
            "content": """당신은 피부과 전문의입니다. 
            친근하고 캐주얼하게 환자와의 진료를 진행해주세요.
            당신은 현재 환자와 말로 대화하고 있음을 인지하세요.
            자세한 설명이 필요하지 않은 경우엔 답변을 짧고 간결하게 해주세요.
            '안녕하세요'와 같은 인사는 생략해도 됩니다.
            """
        }
    ]

    task = f"""
        환자 질병에 대한 정보: {context},
        환자와의 대화: {conversation}
        위의 정보를 참고하셔도 좋습니다.
        다음에 대해 답변해주세요.
        {query}
        """

    if image:
        try:
            image_content = image.read()
            image_base64 = base64.b64encode(image_content).decode("utf-8")
            image_type = image.content_type

            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": task},
                    {"type": "image_url", "image_url": f"data:{image_type};base64,{image_base64}"}
                ]
            })
        except Exception as e:
            return {"error": f"Error processing the image: {e}"}
    else:
        messages.append({
            "role": "user",
            "content": task
        })
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    print(response.choices[0].message.content)

    return response.choices[0].message.content