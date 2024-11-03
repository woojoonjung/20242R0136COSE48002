import os, json
import requests
from PIL import Image
from io import BytesIO
import numpy as np

def load_documents(directory_path):
    # Load all documents from a specified directory
    with open(directory_path, 'r') as file:
        data = json.load(file)
    return data

def google_image_search(query, api_key, cse_id, num_results=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": cse_id,
        "key": api_key,
        "searchType": "image",
        "num": num_results
    }
    response = requests.get(url, params=params)
    data = response.json()
    return [item['link'] for item in data.get('items', [])]

def load_image(path):
    return Image.open(path)

def download_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        print(f"Failed to download image from {url}: {e}")
        return None

def preprocess_image(image, size=(224, 224)):
    image = image.resize(size)
    image = np.array(image) / 255.0  # Normalize pixel values
    return image