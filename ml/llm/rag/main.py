import sys ,  os
sys.path.append(os.path.abspath("/workspace"))

from ml.llm.rag.retriever import Retriever
from ml.llm.rag.generator import Generator
from ml.llm.rag.utils import load_documents, google_image_search
from ml.llm.rag.image_similarity import ImageSimilarity
from dotenv import load_dotenv


load_dotenv()



def find_entity_by_name(data, name):
    for entity in data:
        if name in entity.get('name'):
            return entity
    return None


def main(query,query_img):
    # Load or define your dataset for retrieval
    
    asan_loc = "/workspace/capston/ml/llm/data/disease_details.json"

    documents = load_documents(asan_loc)
    documents = str(documents)
    # print("!!!!!!!!!!!!!!!!!!!!!!!!",documents)
    # Initialize Retriever and Generator
    retriever = Retriever(documents)
    generator = Generator()

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
        retrieved_imgs += utils.google_image_search(google_query, api_key, cse_id)
        pairs += [(disease, img_url) for img_url in retrieved_imgs]
    
    results = image_sim.compare_images(query_img, retrieved_imgs)
    diagnosis = next(pair[0] for pair in pairs if pair[1] == results[0])

    context = find_entity_by_name(documents, diagnosis)
    context = str(context)

    # Generate response based on retrieved documents
    response = generator.generate_response(context, query)
    return response

# if __name__ == "__main__":
#     main()