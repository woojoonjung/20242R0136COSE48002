import sys, os
from retriever import Retriever
from utils import load_documents, load_image, google_lens
from dotenv import load_dotenv

### queries
# query = '목과 팔꿈치 안쪽에 피부가 건조하고 심하게 가렵습니다. 긁다 보니 피부가 갈라지고 염증도 생겼어요.' # 아토피 피부염
# query = '손가락에 딱딱한 융기된 병변이 생겼는데, 표면이 울퉁불퉁합니다.' # 사마귀
query = '등에 크고 어두운 점이 있는데 점점 커지고 가장자리가 불규칙해졌습니다.' # 흑색종
asan_loc = "/home/work/woojun/Capston/20242R0136COSE48002/ml/llm/data/disease_details.json"
documents = load_documents(asan_loc)

symptom_texts = []
for entry in documents:
    if len(entry["details"].get("증상", "").split()) > 1:
        symptom_texts.append((entry["name"], entry["details"].get("증상", "")))

retriever = Retriever(symptom_texts)
retriever.index_documents()
retrieved_docs = retriever.retrieve(query)
for i in retrieved_docs:
    print("\n",i)

# load_dotenv()
# google_api_key = os.getenv('GOOGLE_API_KEY')
# image_path = os.path.abspath("/home/work/woojun/Capston/20242R0136COSE48002/ml/llm/data/skincancer.jpg")
# results = google_lens(image_path, google_api_key)
# for i in results:
#     print("\n",i)