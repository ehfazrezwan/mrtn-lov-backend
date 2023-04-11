import os
import base64
import requests
from io import BytesIO
from PIL import Image

def generate_image(prompt):
    model_inputs = {
        'prompt': f'(synthwve style nvinkpunk digital illustration of {prompt}, incorporating neon yellow/blue/purple/pink, blending retro and nightclub vibes, in the style of Yoji Shinkawa, trending on artstation:1.4), neon blue/yellow/purple glow background, concert stage, bright colors, Digital art, glow effects, render, 8k, octane render, cinema 4d, blender',
        'negative': 'green, logo, Glasses, Watermark, bad artist, blur, blurry, text, b&w, 3d, bad art, poorly drawn, disfigured, deformed, extra limbs, ugly hands, extra fingers, canvas frame, cartoon, 3d, disfigured, bad art, deformed, extra limbs, weird colors, blurry, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, disfigured, out of frame, ugly, extra limbs, bad anatomy, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, mutated hands, fused fingers, too many fingers, long neck, Photoshop, video game, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, mutation, mutated, extra limbs, extra legs, extra arms, disfigured, deformed, cross-eye, body out of frame, blurry, bad art, bad anatomy, 3d render',
        'num_inference_steps': 50,
        'guidance_scale': 7
    }

    payload = {
        "apiKey": "3a79eef5-7ec7-40ef-be8f-be757e58f6e0",
        "modelKey": "12267ac2-0c96-4921-9c38-1900638af167",
        "startOnly": False,
        "modelInputs": model_inputs
    }

    res = requests.post('https://api.banana.dev/start/v4', json = payload)
    
    # return res.json()
    image_byte_string = res.json()["modelOutputs"][0]["image_base64"]
    image_encoded = image_byte_string.encode('utf-8')
    image_bytes = BytesIO(base64.b64decode(image_encoded))
    ai_image = Image.open(image_bytes)

    return ai_image
    # image.save("output.jpg")

def paste_overlay(ai_image):

    frame_path = os.path.join(os.getcwd(), "assets", "images", "frame.png")
    frame = Image.open(frame_path)

    ai_bg = ai_image.convert("RGBA")
    frame_img = frame.convert("RGBA")

    width = (ai_image.width - frame_img.width) // 2
    height = (ai_image.height - frame_img.height) // 2

    ai_bg.paste(frame_img, (width, height), frame_img)
    ai_bg = ai_bg.convert("RGB")

    return ai_bg

def get_image(prompt):
    ai_image = generate_image(prompt)
    ai_image = paste_overlay(ai_image)
    
    buffered = BytesIO()
    ai_image.save(buffered,format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return {'image_base64': image_base64}