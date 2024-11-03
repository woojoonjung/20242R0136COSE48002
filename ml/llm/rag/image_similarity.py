import numpy as np
import sys, os
sys.path.append(os.path.abspath("/workspace/capston"))
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from ml.llm.rag.utils import download_image, preprocess_image

class ImageSimilarity:
    def __init__(self):
        self.model = VGG16(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

    def extract_features(image):
        image = preprocess_image(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)
        features = self.model.predict(image)
        return features.flatten()

    def calculate_similarity(self, embedding1, embedding2):
        similarity = np.dot(embedding1, embedding2.T) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        return similarity

    def compare_images(self, query_image, retrieved_images):
        query_embedding = self.extract_features(query_image)
        similarities = []
        for img_url in retrieved_images:
            img = download_image(img_url)
            if img:
                retrieved_embedding = self.get_embedding(img)
                similarity = self.calculate_similarity(query_embedding, retrieved_embedding)
                similarities.append((img_url, similarity))
        return sorted(similarities, key=lambda x: x[1], reverse=True)
