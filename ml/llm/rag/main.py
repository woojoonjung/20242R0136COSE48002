from retriever import Retriever
from generator import Generator
import utils
from image_similarity import ImageSimilarity
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # Initialize Retriever and Generator
    retriever = Retriever()
    generator = Generator()

    # Load or define your dataset for retrieval
    asan_loc = "/Users/woojunjung/drsnap/ml/llm/data/asan_details.json"
    documents = utils.load_documents(asan_loc)
    retriever.index_documents(documents)

    query = "피부가 붉고, 기름진 각질이 생겨 간지러워요."
    query_img = utils.load_image("/Users/woojunjung/drsnap/ml/llm/data/test.png")
    image_sim = ImageSimilarity()

    retrieved_docs = retriever.retrieve(query)
    retrieved_imgs = []
    pairs = []

    for disease in retrieved_docs:
        google_query = disease[0]
        api_key = os.getenv("API_KEY")
        cse_id = os.getenv("CSE_ID")
        retrieved_imgs += utils.google_image_search(google_query, api_key, cse_id)
        pairs += [(disease, img_url) for img_url in retrieved_imgs]
    
    results = image_sim.compare_images(query_img, retrieved_imgs)
    diagnosis = next(pair[0] for pair in pairs if pair[1] == results[0])

    context = find_entity_by_name(documents, diagnosis)
    context = str(context)

    # Generate response based on retrieved documents
    response = generator.generate_response(context, query)
    print("Generated Response:", response)

def find_entity_by_name(data, name):
    for entity in data:
        if name in entity.get('name'):
            return entity
    return None

if __name__ == "__main__":
    main()