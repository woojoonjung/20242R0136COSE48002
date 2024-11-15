import sys ,  os
sys.path.append(os.path.abspath("/workspace"))

# __main__.py로 실행하실때 이거 주석 푸시면 됩니다.
# 이미지나 파일 패스 맞추셔야 할거에요!

# from ml.llm.rag.retriever import Retriever
# from ml.llm.rag.generator import Generator
# from ml.llm.rag.utils import load_documents, google_image_search
# from ml.llm.rag.image_similarity import ImageSimilarity
from retriever import Retriever
from generator import Generator
from utils import load_documents, load_image, google_image_search, preprocess_image
from image_similarity import ImageSimilarity
from dotenv import load_dotenv


load_dotenv()

def find_entity_by_name(data, name):
    for entity in data:
        if name in entity.get('name'):
            return entity
    return None


def main(query,query_img):
    # Load or define your dataset for retrieval
    
    asan_loc = "/home/work/woojun/Capston/20242R0136COSE48002/ml/llm/data/disease_details.json"
    documents = load_documents(asan_loc)
    print("!!!!!!!!!!!!!success document!!!!!!!!!!!")
    
    generator = Generator()
    print("!!!!!!!!!!!!!success generator!!!!!!!!!!!")

    image_sim = ImageSimilarity()
    print("similarity class's object is built completely")

    symptom_texts = []
    for entry in documents:
        if len(entry["details"].get("증상", "").split()) > 1:
            symptom_texts.append((entry["name"], entry["details"].get("증상", "")))
    retriever = Retriever(symptom_texts)
    retriever.index_documents()
    print("!!!!!!!!!!!!!success retriever!!!!!!!!!!!")

    retrieved_docs = retriever.retrieve(query)
    # print(retrieved_docs)
    retrieved_imgs = []
    pairs = []

    for disease in retrieved_docs:
        google_query = disease[0]
        # api_key = os.getenv("API_KEY")
        # cse_id = os.getenv("CSE_ID")
        retrieved_imgs += google_image_search(google_query, "AIzaSyDzcdrkz6K4F-zo6WSDD9muIE6kf5MmWRU", "2338e6025cd394266")
        print("\n The disease is " + google_query + "\n")
        print(retrieved_imgs)
        pairs += [(disease, img_url) for img_url in retrieved_imgs]
    print("start comparing image similarity ")
    results = image_sim.compare_images(query_img, retrieved_imgs)
    print(" comparing image similarity finished completely ")
    # diagnosis = next(pair[0] for pair in pairs if pair[1] == results[0])

    # context = find_entity_by_name(documents, diagnosis)
    # context = str(context)

    # # Generate response based on retrieved documents
    # response = generator.generate_response(context, query)
    # return response

if __name__ == "__main__":
    query = '피부에 작은 붉은 반점이 생기고 각질이 일어나요.'
    query_img = load_image("/home/work/woojun/Capston/20242R0136COSE48002/ml/llm/data/test.jpg")
    query_img = preprocess_image(query_img, size=(224,224))
    main(query, query_img)
