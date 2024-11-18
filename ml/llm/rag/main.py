import sys ,  os
import numpy as np
sys.path.append(os.path.abspath("/workspace"))

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
    retrieved_imgs = []
    pairs = []

    for disease in retrieved_docs:
        google_query = disease[0].split("(")[1].strip(")")
        # api_key = os.getenv("API_KEY")
        # cse_id = os.getenv("CSE_ID")
        retrieved_imgs = google_image_search(google_query, "AIzaSyDzcdrkz6K4F-zo6WSDD9muIE6kf5MmWRU", "2338e6025cd394266")
        print("\n The disease is " + google_query + "\n")
        pairs += [(disease[0], img_url) for img_url in retrieved_imgs]

    print("Retrieved images: \n")
    for pair in pairs:
        print(pair)
        print("\n")
    print("start comparing image similarity ")
    results = image_sim.compare_images(query_img, retrieved_imgs)
    print(" comparing image similarity finished completely ")
    print(results)
    diagnosis = next(pair[0] for pair in pairs if pair[1] == results[0][0])
    print("--------------------------------------------------")
    print("The diagnosis is " + diagnosis)
    print("\n")

    context = find_entity_by_name(documents, diagnosis)
    context = str(context)
    print ("Context: " + context)

    # Generate response based on retrieved documents
    response = generator.generate_response(diagnosis)
    print("--------------------------------------------------")
    print("/* Response */")
    print(response)
    return response

if __name__ == "__main__":

    query = '갑자기 허벅지에 이런게 생겼는데 표면이 딱딱하고 까칠까칠해요.'

    query_img = load_image("/home/work/woojun/Capston/20242R0136COSE48002/ml/llm/data/skincancer.jpg")
    print(f"Loaded image shape: {query_img.shape}")
    query_img = preprocess_image(query_img, size=(224, 224))
    print(f"Preprocessed query image shape: {query_img.shape}")

    main(query, query_img)