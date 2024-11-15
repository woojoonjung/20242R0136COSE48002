from retriever import Retriever
from utils import load_documents, load_image, google_image_search
from image_similarity import ImageSimilarity

query = '피부에 작은 붉은 반점이 생기고 각질이 일어나요.'
query_img = load_image("/home/work/woojun/Capston/20242R0136COSE48002/ml/llm/data/건선.png")

asan_loc = "/home/work/woojun/Capston/20242R0136COSE48002/ml/llm/data/disease_details.json"

documents = load_documents(asan_loc)

symptom_texts = []

for entry in documents:
    if len(entry["details"].get("증상", "").split()) > 1:
        symptom_texts.append((entry["name"], entry["details"].get("증상", "")))

retriever = Retriever(symptom_texts)

retriever.index_documents()
retrieved_docs = retriever.retrieve(query)
print(retrieved_docs)

# image_sim = ImageSimilarity()