import numpy as np
import sys, os
sys.path.append(os.path.abspath("/workspace"))
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras import layers, models
from ml.llm.rag.utils import download_image, preprocess_image
from PIL import Image

class ImageSimilarity:
    def __init__(self):
        base_model = EfficientNetB3(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False

        self.model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation="relu"),
            layers.Dropout(0.5),
            layers.Dense(23, activation="softmax")
        ])
        self.model.load_weights(
            "/home/work/woojun/Capston/20242R0136COSE48002/ml/cv/best_model.weights.h5",
            by_name=True
        )

    def extract_features(self,image):
        image = preprocess_image(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)
        features = self.model.predict(image)
        return features.flatten()

    def calculate_similarity(self, embedding1, embedding2):
        similarity = np.dot(embedding1, embedding2.T) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        return similarity

    def compare_images(self, query_image, retrieved_imgs):
        query_embedding = self.extract_features(query_image)
        similarities = []
        for img_url in retrieved_imgs:
            img = download_image(img_url)
            if img:
                retrieved_embedding = self.extract_features(img)
                similarity = self.calculate_similarity(query_embedding, retrieved_embedding)
                similarities.append((img_url, similarity))
        return sorted(similarities, key=lambda x: x[1], reverse=True)

