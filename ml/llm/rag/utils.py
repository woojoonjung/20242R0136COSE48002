import os, json, io
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
    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            return [item['link'] for item in data['items']]
        else:
            print("No items found in response. Full response data:", data)
            return []
    else:
        print("Error:", response.status_code, response.text)
        return []

def load_image(file_path):
    img = Image.open(file_path)
    img_array = np.array(img)
    return img_array

def download_image(url):
    try:
        response = requests.get(url, timeout=10)  # Set a timeout to avoid long waits
        # Check if the response is successful and is an image
        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            img = Image.open(BytesIO(response.content))
            return img
        else:
            print(f"Failed to download image from {url}: Received status code {response.status_code} or invalid content type {response.headers.get('Content-Type')}")
            return None
    except Exception as e:
        print(f"Failed to download image from {url}: {e}")
        return None

def preprocess_image(image, size=(224, 224)):
    if isinstance(image, np.ndarray):
        image = (image).astype(np.uint8) if image.dtype == np.float64 else image.astype(np.uint8)
        if image.shape[-1] == 4:
            image = Image.fromarray(image[:, :, :3])
        else:
            image = Image.fromarray(image)
    elif isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))
        print("바이너리")
    elif hasattr(image, 'file'):
        image = Image.open(io.BytesIO(image.file.read()))
        print("file object")
    elif isinstance(image, str):
        image = Image.open(image)
        print("string")
        
    image = image.resize(size)
    image = np.array(image)
    return image