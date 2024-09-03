import requests
import io
from PIL import Image
import uuid
import os
import time

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": "Bearer hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}

def generate_image(prompt, retries=3, delay=5):
    print(f"Generating image with prompt: {prompt}")  # Debugging

    def query(payload):
        attempts = 0
        while attempts < retries:
            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                response.raise_for_status()  # Raise an exception for HTTP errors
                return response.content
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err} - Attempt {attempts + 1} of {retries}")  # Debugging
            except Exception as err:
                print(f"Other error occurred: {err} - Attempt {attempts + 1} of {retries}")  # Debugging
            
            attempts += 1
            if attempts < retries:
                print(f"Retrying in {delay} seconds...")  # Debugging
                time.sleep(delay)
        return None

    image_bytes = query({
        "inputs": prompt,
    })

    if image_bytes is None:
        print("Failed to generate image after multiple attempts.")  # Debugging
        return None

    try:
        # Open the image with PIL
        image = Image.open(io.BytesIO(image_bytes))

        # Generate a unique name using uuid
        unique_filename = f"{uuid.uuid4()}.png"
        print(f"Generated filename: {unique_filename}")  # Debugging

        # Define the path where the image will be saved
        save_path = os.path.join("uploads", unique_filename)

        # Save the image with the unique name at the specified path
        image.save(save_path)

        # Return the path to the saved image
        return save_path
    except Exception as e:
        print(f"Error opening or saving image: {e}")  # Debugging
        return None

# Example usage
image_path = generate_image("A futuristic cityscape at sunset")
if image_path:
    print(f"Image saved at: {image_path}")
else:
    print("Image generation failed.")
