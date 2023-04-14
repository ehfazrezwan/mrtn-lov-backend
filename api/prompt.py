import uuid
import json
from fastapi import APIRouter, HTTPException, status, WebSocket, FastAPI
from starlette.websockets import WebSocketState
from io import BytesIO
import base64
import asyncio
from datetime import datetime
import pytz

from services.google_sheets import GoogleSheets
from services.repository import PromptRepository
from services.banana_client import (
    start_image_generation,
    check_image_generation,
    paste_overlay,
)
from api.config import discord_client

from core.config import settings

from db.database import SessionLocal

router = APIRouter()
# Set the timezone to Bangladesh Time
bangladesh_tz = pytz.timezone("Asia/Dhaka")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    count = 0
    current_timestamp = datetime.now(bangladesh_tz)
    # Format the timestamp in "DD/MM/YYYY HH:mm:ss"
    formatted_timestamp = current_timestamp.strftime("%d/%m/%Y %H:%M:%S")
    session_uuid = str(uuid.uuid4())
    db = SessionLocal()
    pr = PromptRepository(db)
    data = {
        "uuid": session_uuid,
    }
    pr.create(session_uuid)
    prompt = ""

    while True:
        try:
            ws_data = await websocket.receive_text()
            message = json.loads(ws_data)
            action = message.get("action")

            if action == "start":
                prompt = message["prompt"]
                gs = GoogleSheets()
                pr.update_by_uuid(session_uuid, text=prompt)
                data["prompt"] = prompt
                data["timestamp"] = formatted_timestamp
                # gs.append_row(data)
                call_id = await create_prompt(prompt)
                if call_id is None:
                    start_response = {
                        "status": "error",
                        "message": "Failed to start image generation",
                    }
                    await send_json_if_open(websocket, start_response)
                    await websocket.close()
                    break
                else:
                    start_response = {"status": "started", "callID": call_id}
                await send_json_if_open(websocket, start_response)

            elif action == "check":
                count = count + 1

                if count > 10:
                    error_response = {
                        "status": "error",
                        "message": "Image generation timed out",
                    }
                    await send_json_if_open(websocket, error_response)

                    await websocket.close()
                    break

                try:
                    call_id = message["callID"]
                    image_base64 = await check_prompt(call_id)
                except Exception as e:
                    error_response = {
                        "status": "error",
                        "message": f"Unexpected error: {str(e)}",
                    }
                    await send_json_if_open(websocket, error_response)
                    await websocket.close()
                    break

                if image_base64 is None:
                    check_response = {"status": "running"}
                    await send_json_if_open(websocket, check_response)
                    continue

                pr.update_by_uuid(session_uuid, generated=True)
                pr.update_by_uuid(session_uuid, call_id=call_id)

                check_response = {"status": "completed", "image_base64": image_base64}

                await send_json_if_open(websocket, check_response)
                asyncio.create_task(
                    discord_client.send_image(
                        image_base64, prompt, settings.DISCORD_TEST_CHANNEL_ID
                    )
                )
                await websocket.close()
                break

            else:
                error_response = {"status": "error", "message": "Invalid action"}
                await send_json_if_open(websocket, error_response)
                await websocket.close()
                break
        except Exception as e:
            error_response = {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
            }
            await send_json_if_open(websocket, error_response)
            await websocket.close()
            break


async def create_prompt(prompt):
    try:
        call_id = await start_image_generation(prompt)
        return call_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def check_prompt(call_id):
    try:
        ai_image = None
        try:
            ai_image = await asyncio.wait_for(
                check_image_generation(call_id), timeout=60
            )  # Set a timeout of 60 seconds
        except asyncio.TimeoutError:
            print("Image generation timed out.")
            return None
        except Exception as e:
            print(f"Error during image generation: {str(e)}")
            return None

        if ai_image is None:
            return None

        # Only call paste_overlay if ai_image is not None
        if ai_image:
            try:
                ai_image = paste_overlay(ai_image)
            except Exception as e:
                print(f"Error during overlay pasting: {str(e)}")
                return None

        buffered = BytesIO()
        ai_image.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return image_base64
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def send_json_if_open(websocket, data):
    if (
        websocket.application_state != WebSocketState.DISCONNECTED
        and websocket.client_state != WebSocketState.DISCONNECTED
    ):
        await websocket.send_json(data)
    else:
        print("WebSocket is already closed. Cannot send message.")
