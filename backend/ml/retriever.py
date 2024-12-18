######################################################################################################
# **문서 임베딩과 색인 등 Retrieval과 관련있는 기능들을 관리하는 파일**                                            #
#                                                                                                    #
#                                                                                                    #
# by woojoonjung at korea univ.                                                                      #
# contact: smallthingsmatter729@gmail.com                                                            #
######################################################################################################

import faiss
import torch
import numpy as np
import re
from transformers import AutoTokenizer, AutoModel

class Retriever:
    def __init__(self, documents):
        self.tokenizer = AutoTokenizer.from_pretrained('jhgan/ko-sroberta-multitask')
        self.model = AutoModel.from_pretrained('jhgan/ko-sroberta-multitask').to("cuda")
        self.documents = documents
        # self.knowledge_base, self.all_sentences, self.sentence_to_doc_map = self.preprocess_documents(documents)
        self.index = faiss.IndexFlatIP(768)

    def embed_text(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to("cuda")
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)
        return embeddings.cpu().numpy()

    def index_documents(self):
        # Old method
        embedded_documents = self.embed_text(self.documents)
        faiss.normalize_L2(embedded_documents)
        self.index.add(embedded_documents)

        # # Sentece to a Single Sentence Comparison
        # embedded_documents = self.embed_text(self.all_sentences)
        # embeddings_np = np.vstack(embedded_documents).astype('float32')
        # faiss.normalize_L2(embedded_documents)
        # self.index.add(embedded_documents)

        # # Sentece to Mean pooled embedding of doc sentences Comparison
        # document_embeddings = []
        # for disease in self.knowledge_base.keys():
        #     sentence_embeddings = []
        #     for sentence in self.knowledge_base[disease]:
        #         sentence_embeddings.append(self.embed_text(sentence))
        #     document_embedding = np.mean(sentence_embeddings, axis=0)
        #     faiss.normalize_L2(document_embedding)
        #     document_embeddings.append(document_embedding)
        # document_embeddings = np.vstack(document_embeddings).astype("float32")
        # self.index.add(document_embeddings)

    def retrieve(self, query, top_k=10):
        # Old method
        query_embedding = self.embed_text(query).reshape(1,-1).astype('float32')
        faiss.normalize_L2(query_embedding)
        distances, indices = self.index.search(query_embedding, top_k)
        result = []
        for idx, similarity in zip(indices.flatten(), distances.flatten()):
            result.append((self.documents[idx][0].split("(")[1].strip(")"), similarity))
        return result

        # query_embedding = self.embed_text([query])
        # faiss.normalize_L2(query_embedding)
        # distances, indices = self.index.search(query_embedding, top_k)
        # results = []
        # for idx, similarity in zip(indices.flatten(), distances.flatten()):
        #     # disease = self.sentence_to_doc_map[idx] # sen to sen
        #     disease = list(self.knowledge_base.keys())[idx]
        #     tmp = (disease, similarity)
        #     results.append(tmp)
        # return results

        ## Custom Metric
        # threshold = 0.65
        # doc_scores = {}
        # for idx, similarity in zip(indices.flatten(), distances.flatten()):
        #     doc_id = self.sentence_to_doc_map[idx]
        #     if doc_id not in doc_scores:
        #         doc_scores[doc_id] = 0
        #     if similarity > threshold:
        #         doc_scores[doc_id] += 1
        # doc_ratios = {doc_id: score / len(self.knowledge_base[doc_id]) for doc_id, score in doc_scores.items()}
        # sorted_doc_ratios = sorted(doc_ratios.items(), key=lambda x: x[1], reverse=True)
        # top_documents = sorted_doc_ratios[:top_k]

    def split_document_into_sentences(self, document):
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!|:|\)|\n|·|①|②|③|④|⑤|⑥)', document)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        return sentences

    def preprocess_documents(self, documents):
        knowledge_base = {}
        print(len(documents))
        for entry in documents:
            if len(entry["details"].get("증상", "").split()) > 1 and len(entry["details"].get("진단", "").split()) > 1:
                document = entry["details"]["증상"] + entry["details"]["진단"]
                sentences = self.split_document_into_sentences(document)
                knowledge_base[entry['name']] = sentences
        print(len(knowledge_base))
        all_sentences = []
        for disease in knowledge_base.keys():
            all_sentences += [sentence for sentence in knowledge_base[disease]]
        sentence_to_doc_map = []
        for disease, sentences in knowledge_base.items():
            sentence_to_doc_map.extend([disease] * len(sentences))
        return knowledge_base, all_sentences, sentence_to_doc_map