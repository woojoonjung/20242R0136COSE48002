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
        "q": query + "lesion",
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
    # Debugging: Print the initial shape
    if isinstance(image, np.ndarray):
        print(f"Initial image shape: {image.shape}, dtype: {image.dtype}")
    
    # Check if the input is a NumPy array
    if isinstance(image, np.ndarray):
        # Remove batch dimension if present
        if len(image.shape) == 4 and image.shape[0] == 1:
            image = image[0]
        # Fix cases where height and width are swapped
        if image.shape[0] == 1 and image.shape[1] == 1 and len(image.shape) == 4:
            image = np.squeeze(image, axis=(0, 1))  # Remove redundant dimensions
        # Ensure the array is uint8 and handle RGBA
        if image.dtype != np.uint8:
            image = (image * 255).astype(np.uint8)
        if image.shape[-1] == 4:
            image = Image.fromarray(image[:, :, :3])  # Convert RGBA to RGB
        else:
            image = Image.fromarray(image)

    elif isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))
    elif hasattr(image, 'file'):
        image = Image.open(io.BytesIO(image.file.read()))
    elif isinstance(image, str):
        image = Image.open(image)
    
    # Ensure the image is in RGB format
    image = image.convert("RGB")
    
    # Resize the image to the target size
    image = image.resize(size)
    
    # Convert back to NumPy array and normalize
    image = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    print(f"Final preprocessed image shape: {image.shape}")
    return image