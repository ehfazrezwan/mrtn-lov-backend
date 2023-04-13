import os
import base64
import requests
from io import BytesIO
from PIL import Image
import json
import asyncio
import httpx

from core.config import settings

async def start_image_generation(prompt: str):
    model_inputs = _prepare_model_inputs(prompt)
    
    payload = {
        "apiKey": settings.BANANA_API_KEY,
        "modelKey": settings.BANANA_MODEL_KEY,
        "startOnly": True,
        "modelInputs": model_inputs
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post('https://api.banana.dev/start/v4', json=payload)
        res_data = res.json()
        call_id = res_data.get("callID")
    except Exception as e:
        print(f"Error in start_image_generation: {str(e)}")
        call_id = None

    return call_id

async def check_image_generation(call_id: str):
    payload = {
        "apiKey": settings.BANANA_API_KEY,
        "callID": call_id,
        "longPoll": False
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post('https://api.banana.dev/check/v4', json=payload)
        res_data = res.json()
    except Exception as e:
        print(f"Error in check_image_generation: {str(e)}")
        return None

    if res_data["message"] == "running":
        return None

    image_byte_string = res_data["modelOutputs"][0]["image_base64"]
    image_encoded = image_byte_string.encode('utf-8')
    image_bytes = BytesIO(base64.b64decode(image_encoded))
    ai_image = Image.open(image_bytes)

    return ai_image

def _prepare_model_inputs(prompt):
    model_inputs = {
        'prompt': f'digital illustration of ({prompt}:1.6) trending on artstation, incorporating neon yellow/blue/purple/pink, blending retro and nightclub vibes',
        'negative': 'green, logo, Glasses, Watermark, bad artist, blur, blurry, text, b&w, 3d, bad art, poorly drawn, disfigured, deformed, extra limbs, ugly hands, extra fingers, canvas frame, cartoon, 3d, disfigured, bad art, deformed, extra limbs, weird colors, blurry, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, disfigured, out of frame, ugly, extra limbs, bad anatomy, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, mutated hands, fused fingers, too many fingers, long neck, Photoshop, video game, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, mutation, mutated, extra limbs, extra legs, extra arms, disfigured, deformed, cross-eye, body out of frame, blurry, bad art, bad anatomy, 3d render',
        'num_inference_steps': 50,
        'guidance_scale': 7
    }

    return model_inputs

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