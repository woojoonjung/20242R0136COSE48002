import faiss
import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import utils

class Retriever:
    def __init__(self, documents):
        # Initialize FAISS index and model
        self.tokenizer = AutoTokenizer.from_pretrained('jhgan/ko-sroberta-multitask')
        self.model = AutoModel.from_pretrained('jhgan/ko-sroberta-multitask').to("cuda")
        self.documents = documents
        self.embedded_documents = self.embed_text(self.documents)
        d = self.embedded_documents[0].shape[0]
        self.index = faiss.IndexFlatL2(d)

    def embed_text(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to("cuda")
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)
        return embeddings.squeeze().cpu().numpy()

    def index_documents(self):
        self.index.add(self.embedded_documents)

    def retrieve(self, query, top_k=5):
        query_embedding = self.embed_text(query).reshape(1,-1).astype('float32')
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.documents[i] for i in indices[0]]

