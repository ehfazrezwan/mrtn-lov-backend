import base64
import requests
from io import BytesIO
from PIL import Image

def generate_image(prompt):
    model_inputs = {
        'prompt': prompt,
        'negative': '',
        'num_inference_steps': 25,
        'guidance_scale': 7
    }

    payload = {
        "apiKey": "3a79eef5-7ec7-40ef-be8f-be757e58f6e0",
        "modelKey": "fe7e5072-dccb-47a5-a24e-d42b21596877",
        "startOnly": False,
        "modelInputs": model_inputs
    }

    res = requests.post('https://api.banana.dev/start/v4', json = payload)
    
    return res.json()
    # image_byte_string = res.json()["image_base64"]
    # image_encoded = image_byte_string.encode('utf-8')
    # image_bytes = BytesIO(base64.b64decode(image_encoded))
    # image = Image.open(image_bytes)
    # image.save("output.jpg")
